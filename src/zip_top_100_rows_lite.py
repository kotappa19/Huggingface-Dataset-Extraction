#!/usr/bin/env python3
"""
Lightweight script to extract the top 100 rows from extracted_dataset.csv and create a zip file.
This version uses only standard library modules for maximum compatibility and minimal memory usage.
"""

import csv
import zipfile
import os
from pathlib import Path

def zip_top_100_rows_lite(input_file="extracted_dataset.csv", output_zip="top_100_rows.zip", num_rows=100):
    """
    Extract the top N rows from a CSV file and create a zip file using only standard library.
    
    Args:
        input_file (str): Path to the input CSV file
        output_zip (str): Path to the output zip file
        num_rows (int): Number of rows to extract from the top
    """
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    try:
        print(f"Reading top {num_rows} rows from '{input_file}'...")
        
        # Create a temporary CSV file with the top rows
        temp_csv = "temp_top_100_rows.csv"
        
        with open(input_file, 'r', encoding='utf-8', newline='') as infile:
            with open(temp_csv, 'w', encoding='utf-8', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                
                # Read and write header
                header = next(reader)
                writer.writerow(header)
                print(f"Header columns: {len(header)}")
                
                # Read and write the specified number of data rows
                rows_written = 0
                for row in reader:
                    if rows_written >= num_rows:
                        break
                    writer.writerow(row)
                    rows_written += 1
                
                print(f"Successfully read {rows_written} data rows")
        
        print(f"Created temporary CSV file: {temp_csv}")
        
        # Create zip file
        print(f"Creating zip file: {output_zip}")
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(temp_csv, os.path.basename(temp_csv))
        
        # Clean up temporary file
        os.remove(temp_csv)
        print(f"Cleaned up temporary file: {temp_csv}")
        
        # Get file sizes for comparison
        original_size = os.path.getsize(input_file)
        zip_size = os.path.getsize(output_zip)
        
        print(f"\nSummary:")
        print(f"Original file size: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
        print(f"Zip file size: {zip_size:,} bytes ({zip_size/1024:.2f} KB)")
        print(f"Compression ratio: {zip_size/original_size*100:.4f}%")
        print(f"Successfully created '{output_zip}' with top {num_rows} rows!")
        
        return True
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """Main function to run the script."""
    
    # Configuration
    input_file = "extracted_dataset.csv"
    output_zip = "top_100_rows.zip"
    num_rows = 100
    
    print("=" * 60)
    print("CSV Top Rows Zipper (Lite Version)")
    print("=" * 60)
    print(f"Input file: {input_file}")
    print(f"Output zip: {output_zip}")
    print(f"Number of rows to extract: {num_rows}")
    print("=" * 60)
    
    # Run the extraction and zipping process
    success = zip_top_100_rows_lite(input_file, output_zip, num_rows)
    
    if success:
        print("\n✅ Process completed successfully!")
    else:
        print("\n❌ Process failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
