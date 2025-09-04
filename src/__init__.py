"""
Hugging Face Dataset Extraction Tool
===================================

A comprehensive Python tool for extracting data from Hugging Face datasets
stored in parquet format and converting them to CSV files.

Author: Dataset Extraction Tool
Date: 2024
"""

from .extract_dataset import DatasetExtractor

__version__ = "1.0.0"
__author__ = "Dataset Extraction Tool"
__all__ = ["DatasetExtractor"]
