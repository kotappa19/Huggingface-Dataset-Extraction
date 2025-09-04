#!/usr/bin/env python3
"""
Script to extract the top 100 images from the images directory and create a zip file.
This script efficiently handles large image directories by processing files in batches.
"""

import os
import zipfile
import glob
from pathlib import Path
import time

def zip_top_100_images(images_dir="images", output_zip="top_100_images.zip", num_images=100):
    """
    Extract the top N images from a directory and create a zip file.
    
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
        
        # Get all image files
        image_files = []
        for ext in image_extensions:
            pattern = os.path.join(images_dir, ext)
            image_files.extend(glob.glob(pattern))
            # Also check for uppercase extensions
            pattern_upper = os.path.join(images_dir, ext.upper())
            image_files.extend(glob.glob(pattern_upper))
        
        # Remove duplicates and sort
        image_files = sorted(list(set(image_files)))
        
        print(f"Found {len(image_files)} image files")
        
        if len(image_files) == 0:
            print("No image files found in the directory!")
            return False
        
        # Take only the first num_images
        selected_images = image_files[:num_images]
        
        print(f"Selected top {len(selected_images)} images for zipping...")
        
        # Create zip file
        print(f"Creating zip file: {output_zip}")
        start_time = time.time()
        
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, image_path in enumerate(selected_images, 1):
                # Get relative path for the zip file
                arcname = os.path.basename(image_path)
                
                # Add file to zip
                zipf.write(image_path, arcname)
                
                # Progress indicator
                if i % 10 == 0 or i == len(selected_images):
                    print(f"Processed {i}/{len(selected_images)} images...")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Get file sizes for comparison
        total_original_size = sum(os.path.getsize(img) for img in selected_images)
        zip_size = os.path.getsize(output_zip)
        
        print(f"\nSummary:")
        print(f"Images processed: {len(selected_images)}")
        print(f"Processing time: {processing_time:.2f} seconds")
        print(f"Total original size: {total_original_size:,} bytes ({total_original_size/1024/1024:.2f} MB)")
        print(f"Zip file size: {zip_size:,} bytes ({zip_size/1024/1024:.2f} MB)")
        if total_original_size > 0:
            print(f"Compression ratio: {zip_size/total_original_size*100:.2f}%")
        print(f"Successfully created '{output_zip}' with top {num_images} images!")
        
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
    print("Image Top Files Zipper")
    print("=" * 60)
    print(f"Images directory: {images_dir}")
    print(f"Output zip: {output_zip}")
    print(f"Number of images to extract: {num_images}")
    print("=" * 60)
    
    # Run the extraction and zipping process
    success = zip_top_100_images(images_dir, output_zip, num_images)
    
    if success:
        print("\n✅ Process completed successfully!")
    else:
        print("\n❌ Process failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
