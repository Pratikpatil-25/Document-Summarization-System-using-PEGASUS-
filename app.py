# from fastapi import FastAPI, UploadFile, File, HTTPException
# from pathlib import Path
# from src.summarizer.pipeline.prediction import PredictionPipeline
# from src.summarizer.config.configuration import ConfigurationManager
# import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.summarizer.pipeline.prediction import PredictionPipeline
from src.summarizer.config.configuration import ConfigurationManager
import traceback

app = FastAPI(
    title="Document Summarization API",
    version="1.0",
    description="Upload PDF, DOCX or TXT files and generate summaries."
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

# @app.get("/")
# def home():
#     return {
#         "message": "Document Summarization API is running."
#     }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )




config = ConfigurationManager()
prediction_pipeline = PredictionPipeline(config)

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

        summary = prediction_pipeline.predict(file)

        return {
        "filename": file.filename,
        "summary": summary
    }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
    )

    # except Exception as e:

    #     raise HTTPException(
    #         status_code=500,
    #         detail=str(e)
    #     )