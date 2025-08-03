# 🚀 Quick Start Guide

## ✅ Current Status
- **PyMuPDF**: ✅ Installed and working
- **Streamlit**: ✅ Installed and working  
- **Tesseract OCR**: ❌ Not installed (OCR fallback won't work)

## 🌐 Web Interface (Recommended)

### Method 1: Using Python module (Recommended)
```bash
python -m streamlit run streamlit_app.py
```

### Method 2: Using batch file (Windows)
Double-click `run_app.bat` or run:
```bash
run_app.bat
```

### Method 3: Direct streamlit command
```bash
streamlit run streamlit_app.py
```

The app will open at: **http://localhost:8501**

1. **Open your browser** and go to the URL above
2. **Upload a PDF file** using the file uploader
3. **Click "Extract Outline"** to process the document
4. **View results** in real-time and download JSON output

## 💻 Command Line Usage
1. **Place PDF files** in the `input` folder
2. **Run the extractor**:
   ```bash
   python pdf_outline_extractor.py
   ```
3. **Find results** in the `output` folder as JSON files

## 🔧 Installing Tesseract OCR (Optional)
For OCR fallback functionality (image-based PDFs):

### Windows:
1. **Download** from: https://github.com/UB-Mannheim/tesseract/wiki
2. **Install** the Windows installer
3. **Add to PATH** during installation
4. **Set environment variable**:
   ```cmd
   set TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
   ```

### macOS:
```bash
brew install tesseract
```

### Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr
```

## 📁 Project Structure
```
Adobe/
├── pdf_outline_extractor.py    # Main extraction logic
├── streamlit_app.py           # Web interface  
├── requirements.txt           # Dependencies
├── README.md                 # Full documentation
├── input/                    # Place PDFs here
└── output/                   # Generated JSON files
```

## 🎯 What Works Now
- ✅ Layout-based PDF extraction (text-based PDFs)
- ✅ Heading detection (H1, H2, H3)
- ✅ Title extraction
- ✅ Page number tracking
- ✅ Beautiful web interface
- ✅ JSON output

## ⚠️ What Needs Tesseract
- ❌ OCR fallback for image-based PDFs
- ❌ Processing scanned documents

## 🆘 Troubleshooting
- **Web app not loading**: Check if port 8501 is available
- **Import errors**: Run `pip install -r requirements.txt`
- **No headings found**: Try different PDFs or adjust detection settings

## 📞 Next Steps
1. **Test with a PDF** using the web interface
2. **Install Tesseract** if you need OCR functionality
3. **Customize settings** in the web interface
4. **Check the full README.md** for advanced usage 