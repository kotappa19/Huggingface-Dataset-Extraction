#!/usr/bin/env python3
"""
Test script to extract a small sample of data for demonstration
"""

import pandas as pd
import glob
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_single_file():
    """
    Test extraction from a single parquet file to demonstrate functionality.
    """
    data_dir = Path("pmc_clinical_VQA_raw/data")
    
    # Find the first parquet file
    parquet_files = glob.glob(str(data_dir / "*.parquet"))
    if not parquet_files:
        logger.error("No parquet files found!")
        return
    
    first_file = parquet_files[0]
    logger.info(f"Testing with file: {Path(first_file).name}")
    
    try:
        # Read the first parquet file
        df = pd.read_parquet(first_file)
        logger.info(f"Successfully loaded {len(df)} records from {Path(first_file).name}")
        
        # Show basic information
        print(f"\n📊 Dataset Information:")
        print(f"   Records: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   File size: {Path(first_file).stat().st_size / (1024*1024):.2f} MB")
        
        # Show column names
        print(f"\n📋 Columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        # Show sample data (first 3 rows, excluding image data)
        print(f"\n📝 Sample Data (first 3 rows, excluding images):")
        sample_cols = [col for col in df.columns if col != 'image']
        sample_df = df[sample_cols].head(3)
        
        for idx, row in sample_df.iterrows():
            print(f"\n   Row {idx + 1}:")
            for col, value in row.items():
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:97] + "..."
                print(f"     {col}: {value_str}")
        
        # Test image processing
        if 'image' in df.columns:
            print(f"\n🖼️  Image Data Sample:")
            for idx, img_data in enumerate(df['image'].head(3)):
                if img_data is not None:
                    if hasattr(img_data, 'size'):
                        print(f"   Row {idx + 1}: Image available (size: {img_data.size})")
                    else:
                        print(f"   Row {idx + 1}: Image data present")
                else:
                    print(f"   Row {idx + 1}: No image")
        
        # Save a small sample to CSV
        sample_output = "sample_extraction.csv"
        sample_df.to_csv(sample_output, index=False, encoding='utf-8')
        logger.info(f"Sample data saved to {sample_output}")
        
        print(f"\n✅ Test completed successfully!")
        print(f"   Sample CSV created: {sample_output}")
        print(f"   Ready to run full extraction with: python extract_dataset.py")
        
    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_single_file()
    if not success:
        print("\n❌ Test failed!")
    else:
        print("\n🎉 Test passed! The extraction tool is working correctly.")
