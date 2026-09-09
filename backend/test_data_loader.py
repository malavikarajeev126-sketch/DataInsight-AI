from data_loader import (
    load_dataset,
    get_dataset_info,
    get_summary_statistics,
    get_correlation_matrix
)


# Load dataset
df = load_dataset("data/test.csv")

print("Dataset loaded successfully!")
print()

# Dataset information
info = get_dataset_info(df)

print("Dataset Information:")
print("Rows:", info["rows"])
print("Columns:", info["columns"])
print("Column Names:", info["column_names"])
print("Data Types:", info["data_types"])
print("Missing Values:", info["missing_values"])

print()

# Summary statistics
print("Summary Statistics:")
print(get_summary_statistics(df))

print()

# Correlation matrix
print("Correlation Matrix:")
print(get_correlation_matrix(df))