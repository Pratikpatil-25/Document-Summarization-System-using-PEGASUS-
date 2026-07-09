from src.summarizer.logging import logger
from src.summarizer.entity.config_entity import TextExtractionConfig
from src.summarizer.utils.file_reader import read_pdf_file, read_word_file, read_text_file
from pathlib import Path

class TextExtraction:
    def __init__(self, config: TextExtractionConfig):
        self.config = config

    def extract_text(self, file_path: Path) -> Path:
        extension = file_path.suffix.lower()

        if extension == ".pdf":
            text = read_pdf_file(file_path)

        elif extension == ".docx":
            text = read_word_file(file_path)

        elif extension == ".txt":
            text = read_text_file(file_path)

        else:
            raise ValueError(f"Unsupported file type: {extension}")

        output_path = self.config.extracted_dir / f"{file_path.stem}.txt"

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)

        return output_path

