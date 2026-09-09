# ====================================
# DataInsight-AI Backend - Main API
# ====================================

from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from backend.data_loader import load_dataset
from backend.analysis import analyze_dataset


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

        # Return success response with analysis results
        return {
            "message": "Dataset uploaded and analyzed successfully!",
            "filename": file.filename,
            "analysis": analysis
        }

    except Exception as e:
        # Remove the file if something goes wrong
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=f"Could not process dataset: {str(e)}"
        )