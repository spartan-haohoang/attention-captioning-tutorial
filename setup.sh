#!/bin/bash

# Quick setup script - calls the main setup script
echo "🚀 Quick setup for Attention-Based Neural Networks"
echo "Running main setup script..."

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Run the main setup script
bash scripts/setup.sh

echo "✅ Quick setup completed!"
