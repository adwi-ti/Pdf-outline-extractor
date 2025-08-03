import streamlit as st
import tempfile
import os
import json
from pathlib import Path
import pandas as pd
from pdf_outline_extractor import PDFOutlineExtractor, process_pdf_file
import time


def main():
    st.set_page_config(
        page_title="PDF Outline Extractor",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .outline-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        border-left: 4px solid;
    }
    .h1-item {
        background-color: #e3f2fd;
        border-left-color: #1976d2;
        font-weight: bold;
    }
    .h2-item {
        background-color: #f3e5f5;
        border-left-color: #7b1fa2;
        margin-left: 1rem;
    }
    .h3-item {
        background-color: #e8f5e8;
        border-left-color: #388e3c;
        margin-left: 2rem;
    }
    .page-badge {
        background-color: #ff9800;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📄 PDF Outline Extractor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Extract structured outlines from PDF documents using advanced text analysis and OCR</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Features")
        st.markdown("""
        - **Layout-based extraction** using PyMuPDF
        - **OCR fallback** for image-based PDFs
        - **Smart heading detection** (H1, H2, H3)
        - **Title extraction** from first page
        - **Page number tracking**
        - **Real-time processing**
        """)
        
        st.header("🔧 Settings")
        extraction_method = st.selectbox(
            "Extraction Method",
            ["Auto (Layout + OCR fallback)", "Layout only", "OCR only"],
            help="Choose the extraction method. Auto tries layout first, then falls back to OCR if needed."
        )
        
        st.header("📊 Statistics")
        if 'processed_files' not in st.session_state:
            st.session_state.processed_files = 0
        st.metric("Files Processed", st.session_state.processed_files)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload PDF")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF file to extract its outline"
        )
        
        if uploaded_file is not None:
            # Display file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.1f} KB",
                "File type": uploaded_file.type
            }
            st.json(file_details)
            
            # Process button
            if st.button("🚀 Extract Outline", type="primary"):
                with st.spinner("Processing PDF..."):
                    try:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        # Extract outline
                        extractor = PDFOutlineExtractor()
                        
                        if extraction_method == "Layout only":
                            outline = extractor._extract_layout_based(tmp_path)
                        elif extraction_method == "OCR only":
                            outline = extractor._extract_ocr_based(tmp_path)
                        else:
                            outline = extractor.extract_outline(tmp_path)
                        
                        # Clean up temp file
                        os.unlink(tmp_path)
                        
                        # Store results in session state
                        st.session_state.outline_result = {
                            "title": outline.title,
                            "outline": outline.outline
                        }
                        st.session_state.processed_files += 1
                        
                        st.success("✅ Outline extracted successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error processing PDF: {str(e)}")
    
    with col2:
        st.header("📋 Results")
        
        if 'outline_result' in st.session_state:
            result = st.session_state.outline_result
            
            # Display title
            st.markdown(f"### 📖 Document Title")
            st.markdown(f"**{result['title']}**")
            
            # Display outline
            st.markdown(f"### 📑 Outline ({len(result['outline'])} headings)")
            
            if result['outline']:
                for item in result['outline']:
                    level = item['level']
                    text = item['text']
                    page = item['page']
                    
                    # Determine CSS class based on heading level
                    if level == "H1":
                        css_class = "h1-item"
                    elif level == "H2":
                        css_class = "h2-item"
                    else:
                        css_class = "h3-item"
                    
                    # Create the HTML for the outline item
                    html_content = f"""
                    <div class="outline-item {css_class}">
                        <strong>{level}:</strong> {text}
                        <span class="page-badge">Page {page}</span>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.info("No headings found in the document.")
            
            # Download JSON button
            json_str = json.dumps(result, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"{uploaded_file.name.replace('.pdf', '')}_outline.json",
                mime="application/json"
            )
            
            # Display as table
            if result['outline']:
                st.markdown("### 📊 Table View")
                df = pd.DataFrame(result['outline'])
                st.dataframe(df, use_container_width=True)
        else:
            st.info("👆 Upload a PDF file and click 'Extract Outline' to see results here.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Built with ❤️ using Streamlit, PyMuPDF, and Tesseract OCR</p>
        <p>Supports both text-based and image-based PDF documents</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main() 