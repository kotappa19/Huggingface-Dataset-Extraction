# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Setup Environment
```bash
# Run the setup script (creates virtual environment and installs dependencies)
./setup.sh

# Or manually:
python3 -m venv dataset_extraction
source dataset_extraction/bin/activate
pip install -r requirements.txt
```

### 2. Test the Tool
```bash
# Activate the virtual environment
source dataset_extraction/bin/activate

# Test with a small sample
python src/test_extraction.py

# Or view dataset information
python src/extract_dataset.py --info-only
```

### 3. Extract Full Dataset
```bash
# Extract all data to CSV
python src/extract_dataset.py

# Or with custom output file
python src/extract_dataset.py --output "my_dataset.csv"
```

## 📊 What You'll Get

- **CSV file** with all extracted data (864,182 records)
- **Log file** with detailed processing information
- **Progress tracking** with real-time updates

## 🔧 Available Options

| Command | Description |
|---------|-------------|
| `python src/extract_dataset.py` | Extract all data (default) |
| `python src/extract_dataset.py --info-only` | Show dataset info only |
| `python src/extract_dataset.py --output "file.csv"` | Custom output file |
| `python src/extract_dataset.py --data-dir "path/to/data"` | Custom data directory |

## 📁 Output Structure

The CSV will contain these columns:
- `image` - Image metadata (since images can't be stored in CSV)
- `image_id` - Unique image identifier
- `question_1`, `question_2` - Medical questions
- `answer_1`, `answer_2` - Corresponding answers
- `image_primary_label`, `image_secondary_label` - Image classifications
- `caption` - Image descriptions
- `inline_mentions` - Text mentions
- `image_size` - Image dimensions
- `article_license` - License information
- `article_title` - Source article title
- `article_citation` - Citation information
- `article_journal` - Journal name

## ⚡ Performance

- **Processing Speed**: ~1,000-5,000 records per second
- **Total Records**: 864,182 across 112 parquet files
- **Estimated Time**: 3-10 minutes (depending on hardware)
- **Output Size**: ~500MB-1GB CSV file

## 🆘 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Run `python src/extract_dataset.py --help` for command options
- Check `extraction.log` for detailed processing information

## ✅ Ready to Go!

Your dataset extraction tool is ready to use. The code is clean, well-documented, and optimized for large datasets.
