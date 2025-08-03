# PDF Outline Extractor

A powerful Python tool that extracts structured outlines from PDF documents using advanced text analysis and OCR capabilities. The system can detect document titles, headings (H1, H2, H3), and track page numbers for each heading.

## 🚀 Features

- **Layout-based extraction** using PyMuPDF for text-based PDFs
- **OCR fallback** using Tesseract for image-based PDFs
- **Smart heading detection** with font size, boldness, and alignment analysis
- **Title extraction** from the first page
- **Page number tracking** for each heading
- **Beautiful Streamlit web interface** for real-time processing
- **JSON output** for easy integration
- **Offline operation** - no internet required

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Tesseract OCR engine (for OCR functionality)

### Installing Tesseract OCR

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Set environment variable: `TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata`

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

## 🛠️ Installation

1. **Clone or download this repository**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Command Line Interface

1. **Create input folder:**
   ```bash
   mkdir input
   ```

2. **Place PDF files in the input folder**

3. **Run the extractor:**
   ```bash
   python pdf_outline_extractor.py
   ```

4. **Results will be saved in the `output` folder as JSON files**

### Streamlit Web Interface

1. **Launch the web app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser** and go to the provided URL (usually http://localhost:8501)

3. **Upload a PDF file** and click "Extract Outline"

4. **View results in real-time** and download the JSON output

## 📊 Output Format

The system generates JSON output with the following structure:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Main Heading",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Sub Heading",
      "page": 2
    },
    {
      "level": "H3",
      "text": "Sub-sub Heading", 
      "page": 3
    }
  ]
}
```

## 🔧 How It Works

### Layout-based Extraction (Primary Method)
1. **Text Analysis:** Uses PyMuPDF to extract text with layout information
2. **Font Analysis:** Analyzes font size, boldness, and text positioning
3. **Heading Detection:** Identifies headings based on:
   - Font size (larger = higher level)
   - Bold formatting
   - Center alignment
   - Text length and patterns
4. **Classification:** Categorizes headings into H1, H2, H3 levels

### OCR Fallback (Secondary Method)
1. **Image Conversion:** Converts PDF pages to high-resolution images
2. **Text Recognition:** Uses Tesseract OCR to extract text
3. **Pattern Matching:** Applies heuristics to identify headings:
   - ALL CAPS text
   - Numbered headings
   - Title case formatting
4. **Classification:** Assigns heading levels based on text characteristics

## 🎯 Heading Detection Criteria

### Layout-based Detection
- **H1:** Large font (>14pt), bold, centered
- **H2:** Medium font (10-14pt), bold or centered
- **H3:** Smaller font (<10pt), with heading characteristics

### OCR-based Detection
- **H1:** ALL CAPS text, short length
- **H2:** Numbered headings (1., 2., etc.)
- **H3:** Title case text with heading patterns

## 📁 Project Structure

```
PDF-Outline-Extractor/
├── pdf_outline_extractor.py    # Main extraction logic
├── streamlit_app.py           # Web interface
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── input/                    # Place PDF files here
└── output/                   # Generated JSON files
```

## 🔍 Example Usage

### Processing a Single File
```python
from pdf_outline_extractor import PDFOutlineExtractor

extractor = PDFOutlineExtractor()
outline = extractor.extract_outline("document.pdf")

print(f"Title: {outline.title}")
print(f"Found {len(outline.outline)} headings")
```

### Batch Processing
```python
from pathlib import Path
from pdf_outline_extractor import process_input_folder

# Process all PDFs in input folder
process_input_folder()
```

## ⚙️ Configuration

### Extraction Method Selection
In the Streamlit interface, you can choose:
- **Auto:** Tries layout first, falls back to OCR
- **Layout only:** Uses only PyMuPDF extraction
- **OCR only:** Uses only Tesseract OCR

### Customization
You can modify the heading detection criteria in `pdf_outline_extractor.py`:
- Font size thresholds
- Bold detection methods
- Center alignment tolerance
- OCR pattern matching rules

## 🐛 Troubleshooting

### Common Issues

1. **Tesseract not found:**
   - Ensure Tesseract is installed and in PATH
   - Set `TESSDATA_PREFIX` environment variable

2. **OCR quality issues:**
   - Use higher resolution images
   - Ensure good image quality
   - Try different OCR configurations

3. **Missing headings:**
   - Check if headings use standard formatting
   - Try OCR fallback for image-based PDFs
   - Adjust detection thresholds

4. **Streamlit not starting:**
   - Check if port 8501 is available
   - Try: `streamlit run streamlit_app.py --server.port 8502`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **PyMuPDF** for PDF processing capabilities
- **Tesseract OCR** for text recognition
- **Streamlit** for the web interface
- **Pillow** for image processing

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue on GitHub

---

**Built with ❤️ for efficient PDF document analysis** 