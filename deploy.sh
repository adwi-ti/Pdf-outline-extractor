#!/bin/bash

# PDF Outline Extractor Deployment Script
# This script helps deploy the application to different platforms

echo "🚀 PDF Outline Extractor Deployment Script"
echo "=========================================="

# Function to deploy to Streamlit Cloud
deploy_streamlit_cloud() {
    echo "📋 Deploying to Streamlit Cloud..."
    echo ""
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Select repository: adwi-ti/Pdf-outline-extractor"
    echo "4. Set file path to: streamlit_app.py"
    echo "5. Click Deploy"
    echo ""
    echo "Your app will be available at: https://your-app-name.streamlit.app"
}

# Function to deploy with Docker
deploy_docker() {
    echo "🐳 Building Docker image..."
    docker build -t pdf-outline-extractor .
    
    echo "🚀 Running Docker container..."
    docker run -p 8080:8080 pdf-outline-extractor
    
    echo "✅ App is running at: http://localhost:8080"
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "☁️ Deploying to Heroku..."
    
    # Create Procfile if it doesn't exist
    if [ ! -f "Procfile" ]; then
        echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
    fi
    
    # Create setup.sh if it doesn't exist
    if [ ! -f "setup.sh" ]; then
        cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
EOF
        chmod +x setup.sh
    fi
    
    echo "📋 Next steps:"
    echo "1. Install Heroku CLI"
    echo "2. Run: heroku login"
    echo "3. Run: heroku create your-app-name"
    echo "4. Run: git push heroku main"
}

# Function to deploy to Railway
deploy_railway() {
    echo "🚂 Deploying to Railway..."
    echo ""
    echo "1. Go to https://railway.app"
    echo "2. Connect your GitHub repository"
    echo "3. Select the repository: adwi-ti/Pdf-outline-extractor"
    echo "4. Railway will automatically deploy your app"
    echo "5. Set environment variables if needed:"
    echo "   - STREAMLIT_SERVER_PORT=8080"
    echo "   - STREAMLIT_SERVER_ADDRESS=0.0.0.0"
}

# Main menu
echo "Choose deployment option:"
echo "1. Streamlit Cloud (Recommended - Easiest)"
echo "2. Docker (Local/Cloud)"
echo "3. Heroku"
echo "4. Railway"
echo "5. All options"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        deploy_streamlit_cloud
        ;;
    2)
        deploy_docker
        ;;
    3)
        deploy_heroku
        ;;
    4)
        deploy_railway
        ;;
    5)
        echo "📋 All deployment options:"
        echo ""
        deploy_streamlit_cloud
        echo ""
        echo "---"
        echo ""
        deploy_docker
        echo ""
        echo "---"
        echo ""
        deploy_heroku
        echo ""
        echo "---"
        echo ""
        deploy_railway
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment instructions completed!"
echo "📖 For more details, see DEPLOYMENT.md" 