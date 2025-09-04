#!/usr/bin/env python3
"""
Hugging Face Dataset Extractor
==============================

This script extracts data from Hugging Face datasets stored in parquet format
and saves it to CSV files. It's designed to handle large datasets efficiently
with progress tracking and error handling.

Author: Dataset Extraction Tool
Date: 2024
"""

import os
import pandas as pd
import glob
from pathlib import Path
from tqdm import tqdm
import logging
from typing import List, Dict, Any
import argparse
import sys
from PIL import Image
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extraction.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DatasetExtractor:
    """
    A class to extract data from Hugging Face datasets stored in parquet format.
    """
    
    def __init__(self, data_directory: str, output_file: str = "extracted_dataset.csv", save_images: bool = False, images_dir: str = "images"):
        """
        Initialize the DatasetExtractor.
        
        Args:
            data_directory (str): Path to the directory containing parquet files
            output_file (str): Name of the output CSV file
            save_images (bool): Whether to save images locally
            images_dir (str): Directory to save images
        """
        self.data_directory = Path(data_directory)
        self.output_file = output_file
        self.save_images = save_images
        self.images_dir = Path(images_dir)
        self.parquet_files = []
        self.extracted_data = []
        
        # Validate data directory
        if not self.data_directory.exists():
            raise FileNotFoundError(f"Data directory not found: {data_directory}")
        
        # Create images directory if saving images
        if self.save_images:
            self.images_dir.mkdir(exist_ok=True)
            logger.info(f"Images will be saved to: {self.images_dir}")
    
    def find_parquet_files(self) -> List[Path]:
        """
        Find all parquet files in the data directory.
        
        Returns:
            List[Path]: List of parquet file paths
        """
        pattern = str(self.data_directory / "*.parquet")
        parquet_files = glob.glob(pattern)
        
        if not parquet_files:
            raise FileNotFoundError(f"No parquet files found in {self.data_directory}")
        
        # Sort files for consistent processing order
        parquet_files.sort()
        self.parquet_files = [Path(f) for f in parquet_files]
        
        logger.info(f"Found {len(self.parquet_files)} parquet files")
        return self.parquet_files
    
    def process_image_field(self, image_data: Any, record_index: int = 0) -> str:
        """
        Process image field data. If save_images is True, saves the image locally
        and returns the local path. Otherwise, returns metadata about the image.
        
        Args:
            image_data: Image data from the dataset
            record_index: Index of the current record for unique naming
            
        Returns:
            str: Local image path or processed image information
        """
        if image_data is None:
            return "No image"
        
        # If saving images is enabled
        if self.save_images:
            try:
                # Handle PIL Image objects
                if hasattr(image_data, 'save'):
                    # Generate unique filename based on record index and image hash
                    image_hash = hashlib.md5(str(image_data.tobytes()).encode()).hexdigest()[:8]
                    filename = f"image_{record_index:06d}_{image_hash}.png"
                    image_path = self.images_dir / filename
                    
                    # Save the image
                    image_data.save(image_path, format='PNG')
                    logger.debug(f"Saved image: {image_path}")
                    return str(image_path)
                
                # Handle Hugging Face Image format (dictionary with 'bytes' key)
                elif isinstance(image_data, dict) and 'bytes' in image_data:
                    image_bytes = image_data['bytes']
                    image_hash = hashlib.md5(image_bytes).hexdigest()[:8]
                    filename = f"image_{record_index:06d}_{image_hash}.png"
                    image_path = self.images_dir / filename
                    
                    # Save bytes as image
                    with open(image_path, 'wb') as f:
                        f.write(image_bytes)
                    logger.debug(f"Saved image from HF format: {image_path}")
                    return str(image_path)
                
                # Handle image data as bytes
                elif isinstance(image_data, bytes):
                    image_hash = hashlib.md5(image_data).hexdigest()[:8]
                    filename = f"image_{record_index:06d}_{image_hash}.png"
                    image_path = self.images_dir / filename
                    
                    # Save bytes as image
                    with open(image_path, 'wb') as f:
                        f.write(image_data)
                    logger.debug(f"Saved image from bytes: {image_path}")
                    return str(image_path)
                
                # Handle string paths (if image is already a file path)
                elif isinstance(image_data, str):
                    # If it's already a local path, return it
                    if os.path.exists(image_data):
                        return image_data
                    else:
                        # If it's a URL or remote path, we can't save it without downloading
                        logger.warning(f"Cannot save remote image: {image_data}")
                        return f"Remote image: {image_data}"
                
                else:
                    logger.warning(f"Unknown image data type: {type(image_data)}")
                    return f"Unknown image type: {type(image_data)}"
                    
            except Exception as e:
                logger.error(f"Error saving image for record {record_index}: {str(e)}")
                return f"Error saving image: {str(e)}"
        
        else:
            # If not saving images, return metadata
            if hasattr(image_data, 'size'):
                return f"Image available (size: {image_data.size})"
            elif isinstance(image_data, str):
                return image_data
            else:
                return "Image data present"
    
    def extract_data_from_parquet(self, parquet_file: Path) -> List[Dict[str, Any]]:
        """
        Extract data from a single parquet file.
        
        Args:
            parquet_file (Path): Path to the parquet file
            
        Returns:
            List[Dict[str, Any]]: List of extracted records
        """
        try:
            # Read parquet file
            df = pd.read_parquet(parquet_file)
            logger.info(f"Processing {parquet_file.name}: {len(df)} records")
            
            # Convert to list of dictionaries
            records = []
            for index, (_, row) in enumerate(df.iterrows()):
                record = {}
                
                for column, value in row.items():
                    # Handle image fields specially
                    if column == 'image':
                        record[column] = self.process_image_field(value, index)
                    else:
                        # Convert other data types to string for CSV compatibility
                        if pd.isna(value):
                            record[column] = ""
                        else:
                            record[column] = str(value)
                
                records.append(record)
            
            return records
            
        except Exception as e:
            logger.error(f"Error processing {parquet_file.name}: {str(e)}")
            return []
    
    def extract_all_data(self) -> None:
        """
        Extract data from all parquet files and combine them.
        """
        logger.info("Starting data extraction...")
        
        # Find all parquet files
        self.find_parquet_files()
        
        # Process each parquet file with progress bar
        for parquet_file in tqdm(self.parquet_files, desc="Processing parquet files"):
            records = self.extract_data_from_parquet(parquet_file)
            self.extracted_data.extend(records)
        
        logger.info(f"Total records extracted: {len(self.extracted_data)}")
    
    def save_to_csv(self) -> None:
        """
        Save extracted data to CSV file.
        """
        if not self.extracted_data:
            logger.warning("No data to save!")
            return
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(self.extracted_data)
            
            # Save to CSV
            df.to_csv(self.output_file, index=False, encoding='utf-8')
            
            logger.info(f"Data saved to {self.output_file}")
            logger.info(f"CSV file contains {len(df)} rows and {len(df.columns)} columns")
            
            # Print column information
            logger.info("Columns in the CSV file:")
            for i, col in enumerate(df.columns, 1):
                logger.info(f"  {i}. {col}")
            
            # Print sample data
            logger.info("\nSample data (first 3 rows):")
            print(df.head(3).to_string())
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            raise
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """
        Get information about the dataset.
        
        Returns:
            Dict[str, Any]: Dataset information
        """
        if not self.extracted_data:
            return {"error": "No data extracted yet"}
        
        df = pd.DataFrame(self.extracted_data)
        
        info = {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "file_size_mb": os.path.getsize(self.output_file) / (1024 * 1024) if os.path.exists(self.output_file) else 0
        }
        
        return info


def main():
    """
    Main function to run the dataset extraction.
    """
    parser = argparse.ArgumentParser(description="Extract data from Hugging Face parquet datasets")
    parser.add_argument(
        "--data-dir", 
        type=str, 
        default="pmc_clinical_VQA_raw/data",
        help="Directory containing parquet files (default: pmc_clinical_VQA_raw/data)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="extracted_dataset.csv",
        help="Output CSV file name (default: extracted_dataset.csv)"
    )
    parser.add_argument(
        "--info-only", 
        action="store_true",
        help="Only show dataset information without extracting"
    )
    parser.add_argument(
        "--save-images", 
        action="store_true",
        help="Save images locally to a directory"
    )
    parser.add_argument(
        "--images-dir", 
        type=str, 
        default="images",
        help="Directory to save images (default: images)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = DatasetExtractor(
            data_directory=args.data_dir, 
            output_file=args.output,
            save_images=args.save_images,
            images_dir=args.images_dir
        )
        
        if args.info_only:
            # Just show information about available files
            parquet_files = extractor.find_parquet_files()
            print(f"\nDataset Information:")
            print(f"Data directory: {args.data_dir}")
            print(f"Number of parquet files: {len(parquet_files)}")
            print(f"Parquet files found:")
            for i, file in enumerate(parquet_files[:5], 1):  # Show first 5 files
                print(f"  {i}. {file.name}")
            if len(parquet_files) > 5:
                print(f"  ... and {len(parquet_files) - 5} more files")
        else:
            # Extract data
            extractor.extract_all_data()
            extractor.save_to_csv()
            
            # Show final information
            info = extractor.get_dataset_info()
            print(f"\nExtraction completed successfully!")
            print(f"Total records: {info['total_records']:,}")
            print(f"Total columns: {info['total_columns']}")
            print(f"Output file: {args.output}")
            print(f"File size: {info['file_size_mb']:.2f} MB")
            if args.save_images:
                print(f"Images saved to: {args.images_dir}")
                # Count saved images
                if extractor.images_dir.exists():
                    image_count = len(list(extractor.images_dir.glob("*.png")))
                    print(f"Images saved: {image_count}")
    
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
