import pandas as pd


def get_visualization_columns(df):
    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    return {
        "numerical": numerical_columns,
        "categorical": categorical_columns
    }
    
    # Automatic chart suggestion command
def suggest_charts(df):
    columns = get_visualization_columns(df)

    numerical = columns["numerical"]
    categorical = columns["categorical"]

    suggestions = []

    # Numerical + numerical → scatter plot
    if len(numerical) >= 2:
        suggestions.append("scatter")

    # Categorical columns → bar chart
    if len(categorical) >= 1:
        suggestions.append("bar")

    # Numerical columns → box plot
    if len(numerical) >= 1:
        suggestions.append("box")

    # Two or more numerical columns → correlation heatmap
    if len(numerical) >= 2:
        suggestions.append("heatmap")
        

    return suggestions

def create_bar_chart(df, category_column, value_column):
    import plotly.express as px

    fig = px.bar(
        df,
        x=category_column,
        y=value_column,
        title=f"{value_column} by {category_column}"
    )

    return fig
def create_line_chart(df, x_column, y_column):
    import plotly.express as px

    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} over {x_column}"
    )

    return fig
