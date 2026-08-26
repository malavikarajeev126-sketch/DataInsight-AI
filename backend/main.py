# ====================================
# DataInsight-AI Backend - Main API
# ====================================
# This module serves as the entry point for the FastAPI application.
# It handles routing and API endpoints for the DataInsight-AI project.

from fastapi import FastAPI

# Initialize FastAPI application instance
app = FastAPI()


@app.get("/")  #When someone sends a GET request to /, run the function below.
def home():
    """
    Root endpoint for the API.
    
    Returns:
        dict: A JSON response confirming the API is running.
    """
    return {"message": "DataInsight-AI API is running!"}