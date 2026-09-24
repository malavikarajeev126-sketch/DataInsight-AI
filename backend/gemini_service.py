import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
load_dotenv()

# Get the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return its response."""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return interaction.output_text