# Hugging Face Dataset Extraction Tool

A comprehensive Python tool for extracting data from Hugging Face datasets stored in parquet format and converting them to CSV files.

## Features

- 🚀 **Efficient Processing**: Handles large datasets with 100+ parquet files
- 📊 **Progress Tracking**: Real-time progress bars and logging
- 🖼️ **Image Handling**: Smart handling of image data in CSV format
- 💾 **Local Image Storage**: Save images locally as PNG files with unique naming
- 🛡️ **Error Handling**: Robust error handling and recovery
- 📝 **Detailed Logging**: Comprehensive logging to file and console
- ⚙️ **Configurable**: Command-line arguments for customization

## Dataset Information

This project works with the **PMC Clinical VQA** dataset, which contains:
- **864,182 records** across 112 parquet files
- **Medical images** with questions and answers
- **Multiple fields**: images, questions, answers, captions, labels, and metadata

### Dataset Fields:
1. `image` - Medical images (processed as metadata)
2. `image_id` - Unique identifier for images
3. `question_1` & `question_2` - Medical questions
4. `answer_1` & `answer_2` - Corresponding answers
5. `image_primary_label` & `image_secondary_label` - Image classifications
6. `caption` - Image descriptions
7. `inline_mentions` - Text mentions
8. `image_size` - Image dimensions
9. `article_license` - License information
10. `article_title` - Source article title
11. `article_citation` - Citation information
12. `article_journal` - Journal name

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kotappa19/Huggingface-Dataset-Extraction.git
   cd Huggingface-Dataset-Extraction
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Method 1: Command Line Interface

**Basic extraction**:
```bash
python src/extract_dataset.py
```

**Custom data directory and output file**:
```bash
python src/extract_dataset.py --data-dir "path/to/parquet/files" --output "my_dataset.csv"
```

**View dataset information only**:
```bash
python src/extract_dataset.py --info-only
```

**Extract data with image saving**:
```bash
python src/extract_dataset.py --save-images --images-dir "my_images"
```

### Method 2: Python Script

```python
from src.extract_dataset import DatasetExtractor

# Initialize extractor (without image saving)
extractor = DatasetExtractor("pmc_clinical_VQA_raw/data", "output.csv")

# Initialize extractor with image saving
extractor_with_images = DatasetExtractor(
    data_directory="pmc_clinical_VQA_raw/data", 
    output_file="output_with_images.csv",
    save_images=True,
    images_dir="extracted_images"
)

# Extract all data
extractor_with_images.extract_all_data()

# Save to CSV
extractor_with_images.save_to_csv()

# Get dataset information
info = extractor_with_images.get_dataset_info()
print(f"Extracted {info['total_records']} records")
```

### Method 3: Using the Example Script

```bash
python src/example_usage.py
```

## Image Saving Feature

The tool now supports saving images locally when extracting datasets. This is particularly useful for:

- **Offline analysis**: Work with images without internet connectivity
- **Data backup**: Keep local copies of all images
- **Custom processing**: Apply your own image processing pipelines
- **Dataset distribution**: Share complete datasets with images

### How Image Saving Works:

1. **Automatic Detection**: The tool automatically detects image fields in the dataset
2. **Unique Naming**: Images are saved with unique filenames: `image_000001_a1b2c3d4.png`
3. **Format Conversion**: All images are saved as PNG files for consistency
4. **Path Tracking**: The CSV file contains local paths to the saved images
5. **Error Handling**: Failed image saves are logged but don't stop the extraction

### Image Naming Convention:
- Format: `image_{record_index:06d}_{hash}.png`
- Example: `image_000001_a1b2c3d4.png`
- Record index ensures uniqueness across the dataset
- Hash prevents duplicate images from being saved multiple times

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--data-dir` | Directory containing parquet files | `pmc_clinical_VQA_raw/data` |
| `--output` | Output CSV file name | `extracted_dataset.csv` |
| `--info-only` | Show dataset info without extracting | `False` |
| `--save-images` | Save images locally to a directory | `False` |
| `--images-dir` | Directory to save images | `images` |

## Output

The script generates:
- **CSV file**: Contains all extracted data with proper headers
- **Images directory**: Local images saved as PNG files (when `--save-images` is used)
- **Log file**: `extraction.log` with detailed processing information
- **Console output**: Real-time progress and summary information

### Sample Output Structure:

**Without image saving**:
```csv
image,image_id,question_1,answer_1,question_2,answer_2,image_primary_label,image_secondary_label,caption,inline_mentions,image_size,article_license,article_title,article_citation,article_journal
Image available (size: (512, 512)),img_001,What is shown in this image?,This shows a skin lesion,What type of lesion is this?,Melanoma,skin_lesion,melanoma,A clinical image of a skin lesion,patient presents with,512x512,CC BY 4.0,Clinical Study of Skin Lesions,Smith et al. 2023,Journal of Dermatology
...
```

**With image saving**:
```csv
image,image_id,question_1,answer_1,question_2,answer_2,image_primary_label,image_secondary_label,caption,inline_mentions,image_size,article_license,article_title,article_citation,article_journal
images/image_000001_a1b2c3d4.png,img_001,What is shown in this image?,This shows a skin lesion,What type of lesion is this?,Melanoma,skin_lesion,melanoma,A clinical image of a skin lesion,patient presents with,512x512,CC BY 4.0,Clinical Study of Skin Lesions,Smith et al. 2023,Journal of Dermatology
...
```

## Performance

- **Processing Speed**: ~1,000-5,000 records per second (depending on hardware)
- **Memory Usage**: Optimized for large datasets with streaming processing
- **File Size**: Output CSV typically 20-50% smaller than original parquet files

## Error Handling

The script includes comprehensive error handling:
- **File not found errors**: Clear messages for missing directories/files
- **Corrupted parquet files**: Skips problematic files and continues processing
- **Memory issues**: Efficient processing to handle large datasets
- **Encoding issues**: UTF-8 encoding for international characters

## Logging

All operations are logged to both console and `extraction.log` file:
- **INFO**: General progress information
- **WARNING**: Non-critical issues
- **ERROR**: Critical errors that stop processing

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- pyarrow >= 10.0.0
- tqdm >= 4.64.0
- Pillow >= 9.0.0 (for image processing)

## Troubleshooting

### Common Issues:

1. **"No parquet files found"**:
   - Check that the data directory path is correct
   - Ensure parquet files exist in the specified directory

2. **Memory errors**:
   - The script processes files one at a time to minimize memory usage
   - If issues persist, consider processing smaller batches

3. **Permission errors**:
   - Ensure write permissions for the output directory
   - Check that the output file isn't open in another application

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is open source and available under the MIT License.
