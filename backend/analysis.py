"""
Dataset analysis module for DataInsight-AI.

This module contains functions used to analyze
uploaded datasets and generate useful insights.
"""


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

def analyze_dataset(df):
    """
    Perform basic profiling of a pandas DataFrame.

    Args:
        df: The pandas DataFrame to analyze.

    Returns:
        A dictionary containing basic dataset information,
        missing-value counts, and duplicate-row count.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": get_missing_values(df),
        "duplicate_rows": get_duplicate_count(df),
        "unique_values": get_unique_counts(df),
        "numeric_statistics": get_numeric_statistics(df),
        "categorical_statistics": get_categorical_statistics(df),
       "correlation": get_correlation_matrix(df),
    }