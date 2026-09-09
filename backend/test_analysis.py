import pandas as pd

from backend.analysis import (
    get_missing_values,
    get_duplicate_count,
    get_unique_counts,
    get_numeric_statistics,
    get_categorical_statistics,
    get_correlation_matrix,
    get_outliers,
    analyze_dataset,
)


def create_test_dataframe():
    """Create a sample DataFrame for analysis tests."""

    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Alice"],
        "age": [22, 25, 21, 22],
        "city": ["Bangalore", "Mumbai", "Delhi", "Bangalore"],
        "salary": [45000, 52000, 38000, 45000],
    })


def test_missing_values():
    """Test missing-value detection."""

    df = create_test_dataframe()

    result = get_missing_values(df)

    assert result["name"] == 0
    assert result["age"] == 0
    assert result["city"] == 0
    assert result["salary"] == 0


def test_duplicate_count():
    """Test duplicate-row detection."""

    df = create_test_dataframe()

    result = get_duplicate_count(df)

    assert result == 1


def test_unique_counts():
    """Test unique-value counting."""

    df = create_test_dataframe()

    result = get_unique_counts(df)

    assert result["name"] == 3
    assert result["age"] == 3
    assert result["city"] == 3
    assert result["salary"] == 3


def test_numeric_statistics():
    """Test numerical statistics generation."""

    df = create_test_dataframe()

    result = get_numeric_statistics(df)

    assert "age" in result
    assert "salary" in result

    assert result["age"]["count"] == 4.0
    assert result["salary"]["count"] == 4.0


def test_categorical_statistics():
    """Test categorical statistics generation."""

    df = create_test_dataframe()

    result = get_categorical_statistics(df)

    assert "name" in result
    assert "city" in result

    assert result["name"]["unique_count"] == 3
    assert result["city"]["unique_count"] == 3


def test_correlation_matrix():
    """Test correlation matrix generation."""

    df = create_test_dataframe()

    result = get_correlation_matrix(df)

    assert "age" in result
    assert "salary" in result


def test_outlier_detection():
    """Test numerical outlier detection."""

    df = pd.DataFrame({
        "salary": [40000, 42000, 45000, 43000, 41000, 500000]
    })

    result = get_outliers(df)

    assert result["salary"]["count"] == 1
    assert 500000 in result["salary"]["values"]


def test_analyze_dataset():
    """Test the complete dataset analysis."""

    df = create_test_dataframe()

    result = analyze_dataset(df)

    assert result["rows"] == 4
    assert result["columns"] == 4

    assert "missing_values" in result
    assert "duplicate_rows" in result
    assert "unique_values" in result
    assert "numeric_statistics" in result
    assert "categorical_statistics" in result
    assert "correlation" in result
    assert "outliers" in result