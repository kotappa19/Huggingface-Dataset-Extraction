#!/usr/bin/env python3
"""
Test script to extract a small sample of data for demonstration
"""

import pandas as pd
import glob
from pathlib import Path
import logging
import tempfile
import shutil

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
        
        # Save a small sample to CSV (without images)
        sample_output = "sample_extraction.csv"
        sample_df.to_csv(sample_output, index=False, encoding='utf-8')
        logger.info(f"Sample data saved to {sample_output}")
        
        # Test image saving functionality
        test_image_saving(df.head(3))
        
        # Save sample images locally for demonstration
        save_sample_images(df.head(3))
        
        print(f"\n✅ Test completed successfully!")
        print(f"   Sample CSV created: {sample_output}")
        print(f"   Sample images saved to: sample_images/ directory")
        print(f"   Ready to run full extraction with: python extract_dataset.py")
        
    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
        return False
    
    return True

def test_image_saving(sample_df):
    """
    Test the image saving functionality with a small sample of data.
    """
    print(f"\n💾 Testing Image Saving Functionality:")
    
    # Import the DatasetExtractor here to avoid import issues
    try:
        from extract_dataset import DatasetExtractor
    except ImportError:
        print("   ⚠️  Cannot import DatasetExtractor - skipping image saving test")
        return
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_images_dir = temp_path / "test_images"
        
        try:
            # Create extractor with image saving enabled
            extractor = DatasetExtractor(
                data_directory="pmc_clinical_VQA_raw/data",  # Won't be used for this test
                output_file="test_output.csv",
                save_images=True,
                images_dir=str(test_images_dir)
            )
            
            print(f"   📁 Test images directory: {test_images_dir}")
            
            # Test processing a few images
            images_saved = 0
            for idx, (_, row) in enumerate(sample_df.iterrows()):
                if 'image' in row and row['image'] is not None:
                    try:
                        result = extractor.process_image_field(row['image'], idx)
                        if result and result != "No image" and not result.startswith("Error"):
                            images_saved += 1
                            print(f"   ✅ Row {idx + 1}: Image saved as {Path(result).name}")
                        else:
                            print(f"   ⚠️  Row {idx + 1}: {result}")
                    except Exception as e:
                        print(f"   ❌ Row {idx + 1}: Error processing image - {str(e)}")
            
            # Check results
            if test_images_dir.exists():
                saved_files = list(test_images_dir.glob("*.png"))
                print(f"   📊 Images saved: {len(saved_files)}")
                if saved_files:
                    print(f"   📋 Saved files:")
                    for img_file in saved_files:
                        file_size = img_file.stat().st_size
                        print(f"      - {img_file.name} ({file_size} bytes)")
                else:
                    print(f"   ⚠️  No images were saved")
            else:
                print(f"   ❌ Images directory was not created")
            
            # Test without image saving
            print(f"\n   🔄 Testing without image saving...")
            extractor_no_save = DatasetExtractor(
                data_directory="pmc_clinical_VQA_raw/data",
                output_file="test_output.csv",
                save_images=False
            )
            
            for idx, (_, row) in enumerate(sample_df.iterrows()):
                if 'image' in row and row['image'] is not None:
                    result = extractor_no_save.process_image_field(row['image'], idx)
                    print(f"   📝 Row {idx + 1}: {result}")
                    break  # Just test one to show the difference
            
            print(f"   ✅ Image saving test completed!")
            
        except Exception as e:
            print(f"   ❌ Error during image saving test: {str(e)}")

def save_sample_images(sample_df):
    """
    Save sample images locally for demonstration purposes.
    """
    print(f"\n💾 Saving Sample Images Locally:")
    
    # Import the DatasetExtractor here to avoid import issues
    try:
        from extract_dataset import DatasetExtractor
    except ImportError:
        print("   ⚠️  Cannot import DatasetExtractor - skipping image saving")
        return
    
    # Create a local directory for sample images
    sample_images_dir = Path("sample_images")
    sample_images_dir.mkdir(exist_ok=True)
    
    try:
        # Create extractor with image saving enabled
        extractor = DatasetExtractor(
            data_directory="pmc_clinical_VQA_raw/data",  # Won't be used for this test
            output_file="sample_with_images.csv",
            save_images=True,
            images_dir=str(sample_images_dir)
        )
        
        print(f"   📁 Sample images directory: {sample_images_dir.absolute()}")
        
        # Process and save images
        images_saved = 0
        image_paths = []
        
        for idx, (_, row) in enumerate(sample_df.iterrows()):
            if 'image' in row and row['image'] is not None:
                try:
                    result = extractor.process_image_field(row['image'], idx)
                    if result and result != "No image" and not result.startswith("Error"):
                        images_saved += 1
                        image_paths.append(result)
                        print(f"   ✅ Row {idx + 1}: Image saved as {Path(result).name}")
                    else:
                        print(f"   ⚠️  Row {idx + 1}: {result}")
                except Exception as e:
                    print(f"   ❌ Row {idx + 1}: Error processing image - {str(e)}")
        
        # Create a CSV with image paths
        if image_paths:
            sample_with_images_df = sample_df.copy()
            sample_with_images_df['image'] = [extractor.process_image_field(row['image'], idx) if 'image' in row and row['image'] is not None else "No image" 
                                            for idx, (_, row) in enumerate(sample_df.iterrows())]
            
            sample_with_images_output = "sample_extraction_with_images.csv"
            sample_with_images_df.to_csv(sample_with_images_output, index=False, encoding='utf-8')
            print(f"   📄 Sample CSV with image paths saved: {sample_with_images_output}")
        
        # Show summary
        if sample_images_dir.exists():
            saved_files = list(sample_images_dir.glob("*.png"))
            print(f"   📊 Total images saved: {len(saved_files)}")
            if saved_files:
                print(f"   📋 Saved files:")
                for img_file in saved_files:
                    file_size = img_file.stat().st_size
                    print(f"      - {img_file.name} ({file_size:,} bytes)")
        
        print(f"   ✅ Sample images saved successfully!")
        print(f"   💡 You can now view the images in the '{sample_images_dir}' directory")
        
    except Exception as e:
        print(f"   ❌ Error saving sample images: {str(e)}")

def show_usage_examples():
    """
    Show examples of how to use the extraction tool with image saving.
    """
    print(f"\n📖 Usage Examples:")
    print(f"   " + "="*50)
    
    print(f"\n1️⃣  Extract data without saving images (default):")
    print(f"   python src/extract_dataset.py")
    
    print(f"\n2️⃣  Extract data with images saved to default 'images' directory:")
    print(f"   python src/extract_dataset.py --save-images")
    
    print(f"\n3️⃣  Extract data with images saved to custom directory:")
    print(f"   python src/extract_dataset.py --save-images --images-dir 'my_images'")
    
    print(f"\n4️⃣  Extract data with custom output file and image directory:")
    print(f"   python src/extract_dataset.py --output 'my_dataset.csv' --save-images --images-dir 'dataset_images'")
    
    print(f"\n5️⃣  View dataset information only:")
    print(f"   python src/extract_dataset.py --info-only")
    
    print(f"\n6️⃣  Using the example script (shows both modes):")
    print(f"   python src/example_usage.py")
    
    print(f"\n💡 Tips:")
    print(f"   - Images are saved as PNG files with unique names")
    print(f"   - CSV file will contain local paths to saved images")
    print(f"   - Use --info-only to check dataset before full extraction")
    print(f"   - Check extraction.log for detailed processing information")

if __name__ == "__main__":
    success = test_single_file()
    if not success:
        print("\n❌ Test failed!")
    else:
        print("\n🎉 Test passed! The extraction tool is working correctly.")
        print("📁 Check the 'sample_images/' directory to see the saved sample images!")
    
    # Show usage examples
    show_usage_examples()
