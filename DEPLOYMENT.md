# 🚀 Deployment Guide

This guide covers different ways to deploy your PDF Outline Extractor.

## 📋 Prerequisites

- Python 3.8 or higher
- Git installed
- GitHub account

## 🌐 Local Development

### Quick Start
```bash
# Clone the repository
git clone https://github.com/adwi-ti/Pdf-outline-extractor.git
cd Pdf-outline-extractor

# Install dependencies
pip install -r requirements.txt

# Run the web interface
python -m streamlit run streamlit_app.py
```

## ☁️ Cloud Deployment Options

### 1. Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy your app:

1. **Fork or push** your code to GitHub
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Sign in** with GitHub
4. **Select your repository** and branch
5. **Set the file path** to `streamlit_app.py`
6. **Click Deploy**

Your app will be available at a public URL like: `https://your-app-name.streamlit.app`

### 2. Heroku

1. **Install Heroku CLI**
2. **Create `Procfile`**:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. **Create `setup.sh`**:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```
4. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### 3. Railway

1. **Connect** your GitHub repository to Railway
2. **Set environment variables** if needed
3. **Deploy automatically** on push

### 4. Google Cloud Platform

1. **Create a Cloud Run service**
2. **Use Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8080
   CMD streamlit run streamlit_app.py --server.port=8080 --server.address=0.0.0.0
   ```

### 5. AWS

1. **Use AWS App Runner** or **ECS**
2. **Set up CI/CD** with GitHub Actions
3. **Configure environment variables**

## 🔧 Environment Variables

Set these in your deployment platform:

```bash
# For OCR functionality (optional)
TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata

# Streamlit configuration
STREAMLIT_SERVER_PORT=8080
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 📦 Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t pdf-outline-extractor .
docker run -p 8080:8080 pdf-outline-extractor
```

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Test
      run: |
        python test_basic.py
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port conflicts**: Change the port in deployment settings
2. **Memory limits**: Optimize for cloud deployment
3. **File upload limits**: Configure for your platform
4. **OCR not working**: Install Tesseract on the server

### Performance Optimization

1. **Use caching** for processed PDFs
2. **Implement file size limits**
3. **Add progress indicators**
4. **Optimize image processing**

## 📊 Monitoring

- **Streamlit Cloud**: Built-in analytics
- **Custom logging**: Add logging to track usage
- **Error tracking**: Integrate with Sentry or similar

## 🔒 Security Considerations

1. **File validation**: Validate uploaded PDFs
2. **Rate limiting**: Prevent abuse
3. **Authentication**: Add user authentication if needed
4. **Data privacy**: Don't store sensitive documents

## 📞 Support

For deployment issues:
1. Check the platform's documentation
2. Review error logs
3. Test locally first
4. Check environment variables 