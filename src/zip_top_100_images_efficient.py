#!/usr/bin/env python3
"""
Memory-efficient script to extract the top 100 images from the images directory and create a zip file.
This version processes images one by one without loading all file paths into memory.
"""

import os
import zipfile
import glob
from pathlib import Path
import time

def zip_top_100_images_efficient(images_dir="images", output_zip="top_100_images.zip", num_images=100):
    """
    Extract the top N images from a directory and create a zip file efficiently.
    Processes images one by one to minimize memory usage.
    
    Args:
        images_dir (str): Path to the images directory
        output_zip (str): Path to the output zip file
        num_images (int): Number of images to extract
    """
    
    # Check if images directory exists
    if not os.path.exists(images_dir):
        print(f"Error: Images directory '{images_dir}' not found!")
        return False
    
    try:
        print(f"Scanning for images in '{images_dir}'...")
        
        # Common image extensions
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.webp']
        
        # Create zip file
        print(f"Creating zip file: {output_zip}")
        start_time = time.time()
        
        images_processed = 0
        total_original_size = 0
        
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ext in image_extensions:
                if images_processed >= num_images:
                    break
                    
                # Process lowercase extension
                pattern = os.path.join(images_dir, ext)
                for image_path in glob.iglob(pattern):
                    if images_processed >= num_images:
                        break
                    
                    # Get relative path for the zip file
                    arcname = os.path.basename(image_path)
                    
                    # Add file to zip
                    zipf.write(image_path, arcname)
                    
                    # Track statistics
                    file_size = os.path.getsize(image_path)
                    total_original_size += file_size
                    images_processed += 1
                    
                    # Progress indicator
                    if images_processed % 10 == 0 or images_processed == num_images:
                        print(f"Processed {images_processed}/{num_images} images...")
                
                # Process uppercase extension
                if images_processed >= num_images:
                    break
                    
                pattern_upper = os.path.join(images_dir, ext.upper())
                for image_path in glob.iglob(pattern_upper):
                    if images_processed >= num_images:
                        break
                    
                    # Get relative path for the zip file
                    arcname = os.path.basename(image_path)
                    
                    # Add file to zip
                    zipf.write(image_path, arcname)
                    
                    # Track statistics
                    file_size = os.path.getsize(image_path)
                    total_original_size += file_size
                    images_processed += 1
                    
                    # Progress indicator
                    if images_processed % 10 == 0 or images_processed == num_images:
                        print(f"Processed {images_processed}/{num_images} images...")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Get zip file size
        zip_size = os.path.getsize(output_zip)
        
        print(f"\nSummary:")
        print(f"Images processed: {images_processed}")
        print(f"Processing time: {processing_time:.2f} seconds")
        print(f"Total original size: {total_original_size:,} bytes ({total_original_size/1024/1024:.2f} MB)")
        print(f"Zip file size: {zip_size:,} bytes ({zip_size/1024/1024:.2f} MB)")
        if total_original_size > 0:
            print(f"Compression ratio: {zip_size/total_original_size*100:.2f}%")
        print(f"Successfully created '{output_zip}' with top {images_processed} images!")
        
        return True
        
    except Exception as e:
        print(f"Error processing images: {str(e)}")
        return False

def main():
    """Main function to run the script."""
    
    # Configuration
    images_dir = "images"
    output_zip = "top_100_images.zip"
    num_images = 100
    
    print("=" * 60)
    print("Image Top Files Zipper (Efficient Version)")
    print("=" * 60)
    print(f"Images directory: {images_dir}")
    print(f"Output zip: {output_zip}")
    print(f"Number of images to extract: {num_images}")
    print("=" * 60)
    
    # Run the extraction and zipping process
    success = zip_top_100_images_efficient(images_dir, output_zip, num_images)
    
    if success:
        print("\n✅ Process completed successfully!")
    else:
        print("\n❌ Process failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
