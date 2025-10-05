#!/usr/bin/env python3
"""
Data validation script for Attention-Based Neural Networks project.
This script validates the Flickr8K dataset and ensures data integrity.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
import pandas as pd
from PIL import Image
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate_image_files(image_dir, expected_count=None):
    """Validate image files in the dataset."""
    logger.info(f"Validating images in {image_dir}")
    
    if not os.path.exists(image_dir):
        logger.error(f"Image directory {image_dir} does not exist")
        return False
    
    image_files = []
    invalid_files = []
    
    for file_path in Path(image_dir).glob('*.jpg'):
        try:
            # Try to open and validate the image
            with Image.open(file_path) as img:
                img.verify()
            
            # Check if image has reasonable dimensions
            with Image.open(file_path) as img:
                width, height = img.size
                if width < 50 or height < 50:
                    logger.warning(f"Image {file_path} has very small dimensions: {width}x{height}")
            
            image_files.append(file_path)
            
        except Exception as e:
            logger.error(f"Invalid image file {file_path}: {e}")
            invalid_files.append(file_path)
    
    logger.info(f"Found {len(image_files)} valid images")
    if invalid_files:
        logger.warning(f"Found {len(invalid_files)} invalid images")
    
    if expected_count and len(image_files) != expected_count:
        logger.warning(f"Expected {expected_count} images, found {len(image_files)}")
    
    return len(invalid_files) == 0


def validate_captions_file(captions_file):
    """Validate the captions file."""
    logger.info(f"Validating captions file {captions_file}")
    
    if not os.path.exists(captions_file):
        logger.error(f"Captions file {captions_file} does not exist")
        return False
    
    try:
        # Read captions file
        with open(captions_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        captions_data = {}
        invalid_lines = []
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            # Parse the line (format: image_name#caption_number caption_text)
            if '#' not in line:
                logger.warning(f"Invalid format in line {line_num}: {line}")
                invalid_lines.append(line_num)
                continue
            
            parts = line.split('#', 1)
            if len(parts) != 2:
                logger.warning(f"Invalid format in line {line_num}: {line}")
                invalid_lines.append(line_num)
                continue
            
            image_name = parts[0]
            caption_part = parts[1]
            
            # Split caption number and text
            if ' ' not in caption_part:
                logger.warning(f"Invalid caption format in line {line_num}: {line}")
                invalid_lines.append(line_num)
                continue
            
            caption_num, caption_text = caption_part.split(' ', 1)
            
            # Validate caption number
            try:
                caption_num = int(caption_num)
            except ValueError:
                logger.warning(f"Invalid caption number in line {line_num}: {line}")
                invalid_lines.append(line_num)
                continue
            
            # Validate caption text
            if len(caption_text.strip()) < 5:
                logger.warning(f"Caption too short in line {line_num}: {line}")
            
            # Store caption data
            if image_name not in captions_data:
                captions_data[image_name] = []
            captions_data[image_name].append(caption_text.strip())
        
        logger.info(f"Found captions for {len(captions_data)} images")
        logger.info(f"Total captions: {sum(len(captions) for captions in captions_data.values())}")
        
        # Check for images with unusual number of captions
        for image_name, captions in captions_data.items():
            if len(captions) != 5:
                logger.warning(f"Image {image_name} has {len(captions)} captions (expected 5)")
        
        if invalid_lines:
            logger.warning(f"Found {len(invalid_lines)} invalid lines")
        
        return len(invalid_lines) == 0
    
    except Exception as e:
        logger.error(f"Error reading captions file: {e}")
        return False


def validate_data_consistency(image_dir, captions_file):
    """Validate consistency between images and captions."""
    logger.info("Validating data consistency")
    
    # Get list of image files
    image_files = set()
    for file_path in Path(image_dir).glob('*.jpg'):
        image_files.add(file_path.stem)
    
    # Get list of images with captions
    caption_images = set()
    try:
        with open(captions_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '#' in line:
                    image_name = line.split('#')[0]
                    caption_images.add(image_name)
    except Exception as e:
        logger.error(f"Error reading captions file: {e}")
        return False
    
    # Check for images without captions
    images_without_captions = image_files - caption_images
    if images_without_captions:
        logger.warning(f"Found {len(images_without_captions)} images without captions")
        logger.warning(f"Examples: {list(images_without_captions)[:5]}")
    
    # Check for captions without images
    captions_without_images = caption_images - image_files
    if captions_without_images:
        logger.warning(f"Found {len(captions_without_images)} captions without images")
        logger.warning(f"Examples: {list(captions_without_images)[:5]}")
    
    return len(images_without_captions) == 0 and len(captions_without_images) == 0


def generate_data_report(image_dir, captions_file, output_file=None):
    """Generate a comprehensive data report."""
    logger.info("Generating data report")
    
    report = {
        'dataset_info': {
            'name': 'Flickr8K',
            'image_directory': image_dir,
            'captions_file': captions_file
        },
        'image_statistics': {},
        'caption_statistics': {},
        'validation_results': {}
    }
    
    # Image statistics
    if os.path.exists(image_dir):
        image_files = list(Path(image_dir).glob('*.jpg'))
        report['image_statistics'] = {
            'total_images': len(image_files),
            'file_extension': 'jpg'
        }
        
        # Sample image dimensions
        if image_files:
            sample_image = Image.open(image_files[0])
            report['image_statistics']['sample_dimensions'] = sample_image.size
    
    # Caption statistics
    if os.path.exists(captions_file):
        try:
            with open(captions_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            total_captions = len([line for line in lines if line.strip()])
            unique_images = set()
            
            for line in lines:
                if line.strip() and '#' in line:
                    image_name = line.split('#')[0]
                    unique_images.add(image_name)
            
            report['caption_statistics'] = {
                'total_captions': total_captions,
                'unique_images': len(unique_images),
                'captions_per_image': total_captions / len(unique_images) if unique_images else 0
            }
        except Exception as e:
            logger.error(f"Error generating caption statistics: {e}")
    
    # Save report
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Report saved to {output_file}")
    
    return report


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Validate Flickr8K dataset')
    parser.add_argument('--image-dir', type=str, default='flickr8k/images',
                       help='Directory containing images')
    parser.add_argument('--captions-file', type=str, default='flickr8k/captions.txt',
                       help='Path to captions file')
    parser.add_argument('--report', type=str, help='Generate and save data report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("Starting data validation")
    
    # Validate images
    images_valid = validate_image_files(args.image_dir)
    
    # Validate captions
    captions_valid = validate_captions_file(args.captions_file)
    
    # Validate consistency
    consistency_valid = validate_data_consistency(args.image_dir, args.captions_file)
    
    # Generate report if requested
    if args.report:
        generate_data_report(args.image_dir, args.captions_file, args.report)
    
    # Summary
    logger.info("Validation Summary:")
    logger.info(f"  Images: {'✓' if images_valid else '✗'}")
    logger.info(f"  Captions: {'✓' if captions_valid else '✗'}")
    logger.info(f"  Consistency: {'✓' if consistency_valid else '✗'}")
    
    if images_valid and captions_valid and consistency_valid:
        logger.info("All validations passed!")
        return 0
    else:
        logger.error("Some validations failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
