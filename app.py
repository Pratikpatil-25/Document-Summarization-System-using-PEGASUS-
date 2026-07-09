from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from src.summarizer.pipeline.prediction import PredictionPipeline
from src.summarizer.config.configuration import ConfigurationManager

app = FastAPI(
    title="Document Summarization API",
    version="1.0",
    description="Upload PDF, DOCX or TXT files and generate summaries."
)


@app.get("/")
def home():
    return {
        "message": "Document Summarization API is running."
    }


config = ConfigurationManager()

@app.post("/summarize")
def summarize_document(
    file: UploadFile = File(...)
):
    """
    Upload a document.

    Supported formats:
    - PDF
    - DOCX
    - TXT
    """

    try:

        summary = "This is a placeholder summary. The summarization logic is not yet implemented."
        cleaned_text = PredictionPipeline(config).predict(file)

        return {
        "filename": file.filename,
        "cleaned_text": cleaned_text,
        "summary": summary
    }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )