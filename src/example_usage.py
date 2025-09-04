#!/usr/bin/env python3
"""
Example usage of the Dataset Extractor
=====================================

This script demonstrates how to use the DatasetExtractor class
to extract data from Hugging Face datasets.
"""

from .extract_dataset import DatasetExtractor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Example usage of the DatasetExtractor.
    """
    # Initialize the extractor
    data_directory = "pmc_clinical_VQA_raw/data"
    output_file = "pmc_clinical_vqa_extracted.csv"
    
    # Example 1: Extract without saving images
    print("Example 1: Extracting data without saving images...")
    try:
        # Create extractor instance (default: save_images=False)
        extractor = DatasetExtractor(data_directory, output_file)
        
        # Extract all data
        logger.info("Starting extraction...")
        extractor.extract_all_data()
        
        # Save to CSV
        extractor.save_to_csv()
        
        # Get and display dataset information
        info = extractor.get_dataset_info()
        
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY (No Images)")
        print("="*50)
        print(f"Total records extracted: {info['total_records']:,}")
        print(f"Total columns: {info['total_columns']}")
        print(f"Output file: {output_file}")
        print(f"File size: {info['file_size_mb']:.2f} MB")
        print("\nColumns in the dataset:")
        for i, col in enumerate(info['columns'], 1):
            print(f"  {i:2d}. {col}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return False
    
    # Example 2: Extract with image saving
    print("\nExample 2: Extracting data with image saving...")
    try:
        # Create extractor instance with image saving enabled
        extractor_with_images = DatasetExtractor(
            data_directory=data_directory, 
            output_file="pmc_clinical_vqa_with_images.csv",
            save_images=True,
            images_dir="extracted_images"
        )
        
        # Extract all data
        logger.info("Starting extraction with image saving...")
        extractor_with_images.extract_all_data()
        
        # Save to CSV
        extractor_with_images.save_to_csv()
        
        # Get and display dataset information
        info = extractor_with_images.get_dataset_info()
        
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY (With Images)")
        print("="*50)
        print(f"Total records extracted: {info['total_records']:,}")
        print(f"Total columns: {info['total_columns']}")
        print(f"Output file: pmc_clinical_vqa_with_images.csv")
        print(f"File size: {info['file_size_mb']:.2f} MB")
        print(f"Images saved to: extracted_images/")
        
        # Count saved images
        if extractor_with_images.images_dir.exists():
            image_count = len(list(extractor_with_images.images_dir.glob("*.png")))
            print(f"Images saved: {image_count}")
        
        print("\nColumns in the dataset:")
        for i, col in enumerate(info['columns'], 1):
            print(f"  {i:2d}. {col}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Extraction with images failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Extraction completed successfully!")
    else:
        print("\n❌ Extraction failed!")
