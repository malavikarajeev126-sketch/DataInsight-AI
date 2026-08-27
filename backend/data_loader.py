# Module for loading and analyzing datasets from various file formats
# Supports CSV, Excel (.xlsx), and JSON file types with validation and analysis functions

import os
import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load a dataset based on its file extension.

    Supports CSV, Excel, and JSON files.
    
    Args:
        file_path: Path to the data file to load
        
    Returns:
        A pandas DataFrame containing the loaded data
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported or the dataset is empty.
    """

    # Validate that the file exists before attempting to load
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    # Extract and normalize file extension to lowercase for consistent comparison
    file_extension = os.path.splitext(file_path)[1].lower()

    # Load CSV format using pandas read_csv
    if file_extension == ".csv":
        df = pd.read_csv(file_path)

    # Load Excel (.xlsx) format using pandas read_excel
    elif file_extension == ".xlsx":
        df = pd.read_excel(file_path)

    # Load JSON format using pandas read_json
    elif file_extension == ".json":
        df = pd.read_json(file_path)

    # Raise error if file extension is not supported
    else:
        raise ValueError(
            f"Unsupported file type: {file_extension}"
        )

    # Validate that the dataset is not empty
    if df.empty:
        raise ValueError("The dataset is empty.")

    return df


def get_dataset_info(df: pd.DataFrame):
    """
    Return basic information about the dataset.
    
    Args:
        df: The pandas DataFrame to analyze
        
    Returns:
        A dictionary containing dataset metadata including shape, columns, types, and missing values
    """

    # Compile dataset metadata into a dictionary
    info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }

    return info


def get_summary_statistics(df: pd.DataFrame):
    """
    Return summary statistics for numerical columns.
    
    Args:
        df: The pandas DataFrame to analyze
        
    Returns:
        A DataFrame containing descriptive statistics (count, mean, std, min, 25%, 50%, 75%, max)
    """

    # Generate and return descriptive statistics for all numerical columns
    return df.describe()


def get_correlation_matrix(df: pd.DataFrame):
    """
    Return correlation matrix for numerical columns.
    
    Args:
        df: The pandas DataFrame to analyze
        
    Returns:
        A DataFrame containing the correlation coefficients between all numerical columns
    """

    # Calculate and return Pearson correlation coefficients for all numerical columns
    return df.corr(numeric_only=True)