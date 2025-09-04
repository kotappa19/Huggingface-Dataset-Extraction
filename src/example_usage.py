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
    
    try:
        # Create extractor instance
        extractor = DatasetExtractor(data_directory, output_file)
        
        # Extract all data
        logger.info("Starting extraction...")
        extractor.extract_all_data()
        
        # Save to CSV
        extractor.save_to_csv()
        
        # Get and display dataset information
        info = extractor.get_dataset_info()
        
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY")
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
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Extraction completed successfully!")
    else:
        print("\n❌ Extraction failed!")
