import fitz  # PyMuPDF (fitz is the correct import)
import json
import os
import re
from typing import List, Dict, Optional, Tuple
import pytesseract
from PIL import Image
import numpy as np
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HeadingInfo:
    level: str  # "H1", "H2", "H3"
    text: str
    page: int
    font_size: float
    is_bold: bool
    is_centered: bool


@dataclass
class DocumentOutline:
    title: str
    outline: List[Dict[str, any]]


class PDFOutlineExtractor:
    def __init__(self):
        self.doc = None
        self.page_width = 0
        self.page_height = 0
        
    def extract_outline(self, pdf_path: str) -> DocumentOutline:
        """Main method to extract outline from PDF"""
        try:
            # Try layout-based extraction first
            return self._extract_layout_based(pdf_path)
        except Exception as e:
            print(f"Layout-based extraction failed: {e}")
            print("Falling back to OCR extraction...")
            return self._extract_ocr_based(pdf_path)
    
    def _extract_layout_based(self, pdf_path: str) -> DocumentOutline:
        """Extract outline using PyMuPDF layout analysis"""
        self.doc = fitz.open(pdf_path)
        
        if len(self.doc) == 0:
            raise ValueError("PDF is empty or corrupted")
        
        # Get page dimensions from first page
        first_page = self.doc[0]
        self.page_width = first_page.rect.width
        self.page_height = first_page.rect.height
        
        # Extract title from first page
        title = self._extract_title(first_page)
        
        # Extract headings from all pages
        headings = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            page_headings = self._extract_headings_from_page(page, page_num + 1)
            headings.extend(page_headings)
        
        # Classify headings into H1, H2, H3
        classified_headings = self._classify_headings(headings)
        
        # Convert to output format
        outline = [
            {
                "level": h.level,
                "text": h.text,
                "page": h.page
            }
            for h in classified_headings
        ]
        
        self.doc.close()
        return DocumentOutline(title=title, outline=outline)
    
    def _extract_title(self, first_page) -> str:
        """Extract title from the first page"""
        title_candidates = []
        
        # Get text blocks from first page
        blocks = first_page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                            
                        font_size = span["size"]
                        is_bold = "bold" in span["font"].lower() or span["flags"] & 2**4
                        is_centered = self._is_text_centered(span["bbox"], self.page_width)
                        
                        # Title criteria: large font, bold, centered
                        if font_size > 14 and is_bold and is_centered:
                            title_candidates.append((text, font_size))
        
        # Return the largest title candidate
        if title_candidates:
            title_candidates.sort(key=lambda x: x[1], reverse=True)
            return title_candidates[0][0]
        
        return "Untitled Document"
    
    def _extract_headings_from_page(self, page, page_num: int) -> List[HeadingInfo]:
        """Extract potential headings from a single page"""
        headings = []
        
        # Get text blocks
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text or len(text) < 3:
                            continue
                        
                        # Skip very long text (likely body text)
                        if len(text) > 100:
                            continue
                        
                        font_size = span["size"]
                        is_bold = "bold" in span["font"].lower() or span["flags"] & 2**4
                        is_centered = self._is_text_centered(span["bbox"], self.page_width)
                        
                        # Potential heading criteria
                        if font_size >= 10 and (is_bold or is_centered):
                            headings.append(HeadingInfo(
                                level="",  # Will be classified later
                                text=text,
                                page=page_num,
                                font_size=font_size,
                                is_bold=is_bold,
                                is_centered=is_centered
                            ))
        
        return headings
    
    def _is_text_centered(self, bbox, page_width: float, tolerance: float = 0.1) -> bool:
        """Check if text is centered on the page"""
        text_x = (bbox[0] + bbox[2]) / 2
        page_center = page_width / 2
        return abs(text_x - page_center) < (page_width * tolerance)
    
    def _classify_headings(self, headings: List[HeadingInfo]) -> List[HeadingInfo]:
        """Classify headings into H1, H2, H3 based on font size and formatting"""
        if not headings:
            return []
        
        # Sort by font size to establish hierarchy
        sorted_headings = sorted(headings, key=lambda h: h.font_size, reverse=True)
        
        # Get font size statistics
        font_sizes = [h.font_size for h in sorted_headings]
        max_size = max(font_sizes)
        min_size = min(font_sizes)
        size_range = max_size - min_size
        
        if size_range == 0:
            # All same size, classify by formatting
            for h in sorted_headings:
                if h.is_bold and h.is_centered:
                    h.level = "H1"
                elif h.is_bold:
                    h.level = "H2"
                else:
                    h.level = "H3"
        else:
            # Classify by font size ranges
            for h in sorted_headings:
                normalized_size = (h.font_size - min_size) / size_range
                
                if normalized_size > 0.7:
                    h.level = "H1"
                elif normalized_size > 0.4:
                    h.level = "H2"
                else:
                    h.level = "H3"
        
        # Sort by page number and then by level
        sorted_headings.sort(key=lambda h: (h.page, {"H1": 1, "H2": 2, "H3": 3}[h.level]))
        
        return sorted_headings
    
    def _extract_ocr_based(self, pdf_path: str) -> DocumentOutline:
        """Extract outline using OCR as fallback"""
        self.doc = fitz.open(pdf_path)
        
        if len(self.doc) == 0:
            raise ValueError("PDF is empty or corrupted")
        
        all_text = []
        title = "Untitled Document"
        
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            
            # Convert page to image
            mat = fitz.Matrix(2, 2)  # Higher resolution for better OCR
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Perform OCR
            try:
                ocr_text = pytesseract.image_to_string(img)
                lines = ocr_text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 2:
                        all_text.append({
                            "text": line,
                            "page": page_num + 1
                        })
                
                # Extract title from first page
                if page_num == 0 and lines:
                    # Find the first substantial line as title
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 3 and len(line) < 100:
                            title = line
                            break
                            
            except Exception as e:
                print(f"OCR failed on page {page_num + 1}: {e}")
                continue
        
        # Simple heading detection for OCR text
        outline = self._detect_headings_from_ocr(all_text)
        
        self.doc.close()
        return DocumentOutline(title=title, outline=outline)
    
    def _detect_headings_from_ocr(self, text_lines: List[Dict]) -> List[Dict]:
        """Detect headings from OCR text using simple heuristics"""
        outline = []
        
        for line_info in text_lines:
            text = line_info["text"]
            page = line_info["page"]
            
            # Simple heading detection rules
            if self._looks_like_heading(text):
                level = self._classify_ocr_heading(text)
                outline.append({
                    "level": level,
                    "text": text,
                    "page": page
                })
        
        return outline
    
    def _looks_like_heading(self, text: str) -> bool:
        """Check if text looks like a heading"""
        # Remove common non-heading patterns
        if re.match(r'^\d+$', text):  # Just numbers
            return False
        if len(text) < 3 or len(text) > 80:
            return False
        if text.lower() in ['page', 'continued', '...']:
            return False
        
        # Check for heading patterns
        heading_patterns = [
            r'^[A-Z][A-Z\s]+$',  # ALL CAPS
            r'^\d+\.\s+[A-Z]',   # Numbered headings
            r'^[A-Z][a-z]+(\s+[A-Z][a-z]+)*$',  # Title Case
        ]
        
        return any(re.match(pattern, text) for pattern in heading_patterns)
    
    def _classify_ocr_heading(self, text: str) -> str:
        """Classify OCR heading level"""
        # Simple classification based on text characteristics
        if text.isupper() and len(text) < 30:
            return "H1"
        elif re.match(r'^\d+\.\s+', text):
            return "H2"
        else:
            return "H3"


def process_pdf_file(input_path: str, output_path: str) -> None:
    """Process a single PDF file and save the outline as JSON"""
    extractor = PDFOutlineExtractor()
    
    try:
        outline = extractor.extract_outline(input_path)
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "title": outline.title,
                "outline": outline.outline
            }, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully processed {input_path}")
        print(f"Title: {outline.title}")
        print(f"Found {len(outline.outline)} headings")
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")


def process_input_folder():
    """Process all PDF files in the input folder"""
    input_folder = Path("input")
    output_folder = Path("output")
    
    # Create output folder if it doesn't exist
    output_folder.mkdir(exist_ok=True)
    
    # Find all PDF files
    pdf_files = list(input_folder.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in the input folder")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    for pdf_file in pdf_files:
        output_file = output_folder / f"{pdf_file.stem}_outline.json"
        process_pdf_file(str(pdf_file), str(output_file))


if __name__ == "__main__":
    # Create input folder if it doesn't exist
    Path("input").mkdir(exist_ok=True)
    
    # Process files
    process_input_folder() 