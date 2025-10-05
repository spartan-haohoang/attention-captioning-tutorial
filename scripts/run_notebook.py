#!/usr/bin/env python3
"""
Notebook runner script for Attention-Based Neural Networks project.
This script helps run and manage Jupyter notebooks programmatically.
"""

import os
import sys
import argparse
import subprocess
import nbformat
from nbconvert import PythonExporter
from nbconvert.preprocessors import ExecutePreprocessor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def setup_environment():
    """Set up the environment for running notebooks."""
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.insert(0, project_root)
    
    # Set environment variables
    os.environ['PYTHONPATH'] = project_root


def list_notebooks():
    """List all available notebooks in the project."""
    notebooks = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):
                notebooks.append(os.path.join(root, file))
    return notebooks


def convert_notebook_to_python(notebook_path, output_path=None):
    """Convert a Jupyter notebook to a Python script."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        exporter = PythonExporter()
        (body, resources) = exporter.from_notebook_node(notebook)
        
        if output_path is None:
            output_path = notebook_path.replace('.ipynb', '.py')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(body)
        
        logger.info(f"Converted {notebook_path} to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error converting notebook {notebook_path}: {e}")
        return None


def execute_notebook(notebook_path, timeout=600):
    """Execute a Jupyter notebook and return the results."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Configure the execution preprocessor
        ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
        
        # Execute the notebook
        ep.preprocess(notebook, {'metadata': {'path': os.path.dirname(notebook_path)}})
        
        # Save the executed notebook
        output_path = notebook_path.replace('.ipynb', '_executed.ipynb')
        with open(output_path, 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f)
        
        logger.info(f"Executed notebook {notebook_path} and saved to {output_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error executing notebook {notebook_path}: {e}")
        return False


def start_jupyter_server(port=8888, ip='0.0.0.0', no_browser=True):
    """Start a Jupyter server."""
    cmd = [
        'jupyter', 'lab',
        f'--ip={ip}',
        f'--port={port}',
        '--no-browser' if no_browser else '',
        '--allow-root',
        '--NotebookApp.token=""',
        '--NotebookApp.password=""'
    ]
    
    # Remove empty strings
    cmd = [arg for arg in cmd if arg]
    
    try:
        logger.info(f"Starting Jupyter server on {ip}:{port}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error starting Jupyter server: {e}")
    except KeyboardInterrupt:
        logger.info("Jupyter server stopped by user")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Notebook runner for Attention-Based Neural Networks')
    parser.add_argument('--list', action='store_true', help='List all available notebooks')
    parser.add_argument('--convert', type=str, help='Convert notebook to Python script')
    parser.add_argument('--execute', type=str, help='Execute a notebook')
    parser.add_argument('--server', action='store_true', help='Start Jupyter server')
    parser.add_argument('--port', type=int, default=8888, help='Port for Jupyter server')
    parser.add_argument('--ip', type=str, default='0.0.0.0', help='IP for Jupyter server')
    parser.add_argument('--timeout', type=int, default=600, help='Timeout for notebook execution')
    
    args = parser.parse_args()
    
    # Set up environment
    setup_environment()
    
    if args.list:
        notebooks = list_notebooks()
        print("Available notebooks:")
        for notebook in notebooks:
            print(f"  - {notebook}")
    
    elif args.convert:
        output_path = convert_notebook_to_python(args.convert)
        if output_path:
            print(f"Converted to: {output_path}")
    
    elif args.execute:
        success = execute_notebook(args.execute, args.timeout)
        if success:
            print(f"Successfully executed: {args.execute}")
        else:
            print(f"Failed to execute: {args.execute}")
            sys.exit(1)
    
    elif args.server:
        start_jupyter_server(args.port, args.ip)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
