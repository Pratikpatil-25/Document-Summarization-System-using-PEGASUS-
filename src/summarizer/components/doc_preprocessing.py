from src.summarizer.logging import logger
from src.summarizer.entity.config_entity import DocPreprocessingConfig
from pathlib import Path
from src.summarizer.utils.text_preprocessor import clean_text 
import fitz
from docx import Document

class DocPreprocessing:
    def __init__(self, config: DocPreprocessingConfig):
        self.config = config

    def preprocess(self, file_path: Path) -> Path:

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        cleaned_text = clean_text(text)

        output_path = self.config.preprocessed_dir / f"{file_path.stem}_cleaned.txt"
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(cleaned_text)
            
        return output_path

