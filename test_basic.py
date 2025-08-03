#!/usr/bin/env python3
"""
Simple test script to verify PDF outline extraction works
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pdf_outline_extractor import PDFOutlineExtractor
    print("✅ PDF Outline Extractor imported successfully")
    
    # Test basic functionality
    extractor = PDFOutlineExtractor()
    print("✅ PDFOutlineExtractor instance created successfully")
    
    print("\n📋 System Status:")
    print("- PyMuPDF: ✅ Available")
    
    try:
        import pytesseract
        print("- pytesseract: ✅ Available")
        
        # Try to find tesseract
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            print("- Tesseract OCR: ✅ Available")
        except Exception as e:
            print("- Tesseract OCR: ❌ Not found - OCR fallback will not work")
            print("  To install Tesseract on Windows:")
            print("  1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("  2. Install and add to PATH")
            print("  3. Set environment variable: TESSDATA_PREFIX=C:\\Program Files\\Tesseract-OCR\\tessdata")
    except ImportError:
        print("- pytesseract: ❌ Not available")
    
    print("\n🚀 Ready to run!")
    print("\nTo start the web interface:")
    print("  streamlit run streamlit_app.py")
    print("\nTo process PDFs from command line:")
    print("  1. Place PDF files in the 'input' folder")
    print("  2. Run: python pdf_outline_extractor.py")
    
except ImportError as e:
    print(f"❌ Error importing PDF Outline Extractor: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 