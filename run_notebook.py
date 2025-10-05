#!/usr/bin/env python3
"""
Script to run the image captioning notebook with proper environment setup.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Main function to set up and run the notebook."""
    print("🚀 Setting up Image Captioning Environment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("demo_01_ImageCaptioningWithoutAttention.ipynb").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if uv is available
    if not run_command("which uv", "Checking if uv is installed"):
        print("❌ uv is not installed. Please install it first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    if not Path(".venv").exists():
        if not run_command("uv venv", "Creating virtual environment"):
            sys.exit(1)
    
    # Install dependencies
    if not run_command("source .venv/bin/activate && uv pip install -r requirements.txt", 
                      "Installing dependencies"):
        sys.exit(1)
    
    # Test imports
    if not run_command('source .venv/bin/activate && python -c "import torch, torchtext, torchvision; print(\'✅ All imports successful!\')"', 
                      "Testing imports"):
        sys.exit(1)
    
    print("\n🎉 Environment setup complete!")
    print("\n📝 To run the notebook:")
    print("   1. Activate the virtual environment: source .venv/bin/activate")
    print("   2. Start Jupyter: jupyter lab")
    print("   3. Open demo_01_ImageCaptioningWithoutAttention.ipynb")
    print("\n🐳 To run with Docker:")
    print("   1. Build the image: docker build -t attention-captioning .")
    print("   2. Run the container: docker run -p 8888:8888 attention-captioning")
    print("   3. Open http://localhost:8888 in your browser")

if __name__ == "__main__":
    main()