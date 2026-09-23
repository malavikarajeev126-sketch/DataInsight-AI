# ====================================
# DataInsight-AI Backend - Main API
# ====================================
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pathlib import Path
import shutil
import json

from backend.data_loader import load_dataset
from backend.analysis import analyze_dataset

from backend.viz_engine import (
    get_visualization_columns,
    suggest_charts,
    create_bar_chart,
    create_line_chart,
    create_scatter_chart,
    create_box_chart,
    create_correlation_heatmap,
    figure_to_json
)
# Create the FastAPI application
app = FastAPI()


# Folder where uploaded datasets will be stored
UPLOAD_DIR = Path("data/uploads")

# Create the folder if it doesn't already exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():
    """
    Root endpoint to check whether the API is running.
    """
    return {"message": "DataInsight-AI API is running!"}


@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a CSV, Excel, or JSON dataset.

    The uploaded file is saved to data/uploads/,
    loaded using the data loader, analyzed, and the
    analysis results are returned.
    """

    # Supported file extensions
    allowed_extensions = {".csv", ".xlsx", ".json"}

    # Get the extension from the uploaded filename
    file_extension = Path(file.filename).suffix.lower()

    # Reject unsupported file types
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload CSV, Excel, or JSON."
        )

    # Create the path where the file will be saved
    file_path = UPLOAD_DIR / file.filename

    try:
        # Save the uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load the saved dataset
        df = load_dataset(str(file_path))

        # Perform complete dataset analysis
        analysis = analyze_dataset(df)

        # Detect columns suitable for visualization
        visualization_columns = get_visualization_columns(df)

        # Suggest suitable charts
        suggested_charts = suggest_charts(df)

        # Return analysis and visualization information
        return {
            "message": "Dataset uploaded and analyzed successfully!",
            "filename": file.filename,
            "analysis": analysis,
            "visualization": {
                "columns": visualization_columns,
                "suggested_charts": suggested_charts
            }
        }

    except Exception as e:
        # Remove the file if something goes wrong
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=f"Could not process dataset: {str(e)}"
        )
        
@app.post("/visualize")
async def visualize_dataset(
    file: UploadFile = File(...),
    chart_type: str = Form(...),
    x_column: str | None = Form(None),
    y_column: str | None = Form(None),
    column: str | None = Form(None)
):
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load dataset
        df = load_dataset(str(file_path))

        # Create the requested chart
        if chart_type == "bar":
            if not x_column or not y_column:
                raise HTTPException(
                    status_code=400,
                    detail="Bar chart requires x_column and y_column"
                )

            fig = create_bar_chart(df, x_column, y_column)

        elif chart_type == "line":
            if not x_column or not y_column:
                raise HTTPException(
                    status_code=400,
                    detail="Line chart requires x_column and y_column"
                )

            fig = create_line_chart(df, x_column, y_column)

        elif chart_type == "scatter":
            if not x_column or not y_column:
                raise HTTPException(
                    status_code=400,
                    detail="Scatter chart requires x_column and y_column"
                )

            fig = create_scatter_chart(df, x_column, y_column)

        elif chart_type == "box":
            if not column:
                raise HTTPException(
                    status_code=400,
                    detail="Box chart requires column"
                )

            fig = create_box_chart(df, column)

        elif chart_type == "heatmap":
            fig = create_correlation_heatmap(df)

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported chart type"
            )

        return {
            "message": "Visualization created successfully!",
            "chart_type": chart_type,
            "chart": figure_to_json(fig)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not create visualization: {str(e)}"
        )