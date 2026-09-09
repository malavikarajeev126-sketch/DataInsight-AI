import pandas as pd

"""
Dataset analysis module for DataInsight-AI.

This module contains functions used to analyze
uploaded datasets and generate useful insights.
"""


def clean_for_json(data):
    """
    Convert NaN and infinite float values to None
    so the data can be safely serialized as JSON.

    Args:
        data: Dictionary, list, or value to clean.

    Returns:
        JSON-safe version of the input data.
    """

    if isinstance(data, dict):
        return {
            key: clean_for_json(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [clean_for_json(value) for value in data]

    if isinstance(data, float):
        if pd.isna(data) or data in (float("inf"), float("-inf")):
            return None

    return data


def get_missing_values(df):
    """
    Count missing values in each column.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary mapping each column name to its
        number of missing values.
    """

    return df.isnull().sum().to_dict()


def get_duplicate_count(df):
    """
    Count duplicate rows in a pandas DataFrame.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        The number of duplicate rows.
    """

    return int(df.duplicated().sum())


def get_unique_counts(df):
    """
    Count the number of unique values in each column.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary mapping each column name to its
        number of unique values.
    """

    return df.nunique().to_dict()


def get_numeric_statistics(df):
    """
    Generate descriptive statistics for numerical columns.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary containing statistics for each numerical column.
    """

    numeric_df = df.select_dtypes(include="number")

    return numeric_df.describe().to_dict()


def get_categorical_statistics(df):
    """
    Generate statistics for categorical columns.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary containing categorical statistics for each
        categorical column.
    """

    categorical_df = df.select_dtypes(include=["object", "category"])

    statistics = {}

    for column in categorical_df.columns:
        statistics[column] = {
            "unique_count": int(categorical_df[column].nunique()),
            "most_frequent": (
                categorical_df[column].mode().iloc[0]
                if not categorical_df[column].mode().empty
                else None
            ),
            "frequency": int(categorical_df[column].value_counts().iloc[0])
            if not categorical_df[column].value_counts().empty
            else 0,
        }

    return statistics


def get_correlation_matrix(df):
    """
    Calculate the Pearson correlation matrix for numerical columns.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary containing correlation values between
        numerical columns.
    """

    # Select only numerical columns
    numerical_df = df.select_dtypes(include="number")

    # If there are fewer than two numerical columns,
    # correlation cannot provide a meaningful matrix.
    if numerical_df.shape[1] < 2:
        return {}

    # Calculate Pearson correlation coefficients
    correlation = numerical_df.corr()

    # Convert the DataFrame to a normal dictionary
    return correlation.to_dict()


def get_outliers(df):
    """
    Detect outliers in numerical columns using the IQR method.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary containing outlier information for each
        numerical column.
    """

    numerical_df = df.select_dtypes(include="number")

    outliers = {}

    for column in numerical_df.columns:
        series = numerical_df[column].dropna()

        if len(series) < 4:
            outliers[column] = {
                "count": 0,
                "values": [],
            }
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_values = series[
            (series < lower_bound) |
            (series > upper_bound)
        ].tolist()

        outliers[column] = {
            "count": len(outlier_values),
            "values": outlier_values,
        }

    return outliers


def analyze_dataset(df):
    """
    Perform complete analysis of a pandas DataFrame.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary containing dataset profiling,
        missing values, duplicates, unique values,
        numerical statistics, categorical statistics,
        correlation analysis, and outlier detection.
    """

    result = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": get_missing_values(df),
        "duplicate_rows": get_duplicate_count(df),
        "unique_values": get_unique_counts(df),
        "numeric_statistics": get_numeric_statistics(df),
        "categorical_statistics": get_categorical_statistics(df),
        "correlation": get_correlation_matrix(df),
        "outliers": get_outliers(df),
    }

    # Convert NaN and infinite values to None
    # so the result can be safely returned as JSON.
    return clean_for_json(result)
