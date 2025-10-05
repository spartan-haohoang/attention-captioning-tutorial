#!/bin/bash

# Setup script for Attention-Based Neural Networks project
# This script sets up the development environment

set -e  # Exit on any error

echo "🚀 Setting up Attention-Based Neural Networks development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    else
        print_error "pip3 is not installed. Please install pip3."
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install production dependencies
    pip install -r requirements.txt
    
    # Install development dependencies
    pip install -r requirements-dev.txt
    
    print_success "Dependencies installed"
}

# Install pre-commit hooks
install_pre_commit() {
    print_status "Installing pre-commit hooks..."
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        print_success "Pre-commit hooks installed"
    else
        print_warning "pre-commit not found, skipping hook installation"
    fi
}

# Download dataset
download_dataset() {
    print_status "Checking dataset..."
    if [ ! -d "flickr8k" ]; then
        print_status "Downloading Flickr8K dataset..."
        if [ -f "datasets/flickr8k.zip" ]; then
            cd datasets
            unzip -o flickr8k.zip
            cd ..
            print_success "Dataset extracted"
        else
            print_warning "Dataset zip file not found. Please download it manually."
        fi
    else
        print_success "Dataset already exists"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating project directories..."
    mkdir -p data models notebooks tests docs
    print_success "Directories created"
}

# Set up environment file
setup_env() {
    print_status "Setting up environment file..."
    if [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            cp env.example .env
            print_success "Environment file created from template"
        else
            print_warning "No env.example file found"
        fi
    else
        print_success "Environment file already exists"
    fi
}

# Main setup function
main() {
    echo "=========================================="
    echo "  Attention-Based Neural Networks Setup  "
    echo "=========================================="
    echo
    
    check_python
    check_pip
    create_venv
    activate_venv
    install_dependencies
    install_pre_commit
    create_directories
    setup_env
    download_dataset
    
    echo
    echo "=========================================="
    print_success "Setup completed successfully!"
    echo "=========================================="
    echo
    echo "Next steps:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Start JupyterLab: make lab"
    echo "3. Open the notebooks and start learning!"
    echo
    echo "Available commands:"
    echo "- make help          # Show all available commands"
    echo "- make test          # Run tests"
    echo "- make format        # Format code"
    echo "- make lint          # Lint code"
    echo "- make docker-run    # Run with Docker"
    echo
}

# Run main function
main "$@"
