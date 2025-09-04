# Hugging Face Dataset Extraction Tool

A comprehensive Python tool for extracting data from Hugging Face datasets stored in parquet format and converting them to CSV files.

## Features

- 🚀 **Efficient Processing**: Handles large datasets with 100+ parquet files
- 📊 **Progress Tracking**: Real-time progress bars and logging
- 🖼️ **Image Handling**: Smart handling of image data in CSV format
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

### Method 2: Python Script

```python
from src.extract_dataset import DatasetExtractor

# Initialize extractor
extractor = DatasetExtractor("pmc_clinical_VQA_raw/data", "output.csv")

# Extract all data
extractor.extract_all_data()

# Save to CSV
extractor.save_to_csv()

# Get dataset information
info = extractor.get_dataset_info()
print(f"Extracted {info['total_records']} records")
```

### Method 3: Using the Example Script

```bash
python src/example_usage.py
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--data-dir` | Directory containing parquet files | `pmc_clinical_VQA_raw/data` |
| `--output` | Output CSV file name | `extracted_dataset.csv` |
| `--info-only` | Show dataset info without extracting | `False` |

## Output

The script generates:
- **CSV file**: Contains all extracted data with proper headers
- **Log file**: `extraction.log` with detailed processing information
- **Console output**: Real-time progress and summary information

### Sample Output Structure:
```csv
image,image_id,question_1,answer_1,question_2,answer_2,image_primary_label,image_secondary_label,caption,inline_mentions,image_size,article_license,article_title,article_citation,article_journal
Image available (size: (512, 512)),img_001,What is shown in this image?,This shows a skin lesion,What type of lesion is this?,Melanoma,skin_lesion,melanoma,A clinical image of a skin lesion,patient presents with,512x512,CC BY 4.0,Clinical Study of Skin Lesions,Smith et al. 2023,Journal of Dermatology
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
