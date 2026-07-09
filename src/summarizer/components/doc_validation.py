from pathlib import Path
import shutil
import fitz
from docx import Document
from src.summarizer.entity.config_entity import DocValidationConfig
from src.summarizer.utils.file_reader import read_pdf_file, read_word_file, read_text_file
from src.summarizer.logging import logger


class DocValidation:

    def __init__(self, config : DocValidationConfig):

        self.config = config

        self.supported_extensions = {
            extension.lower()
            for extension in config.supported_extensions
        }

    ###########################################################################
    # Private Helper
    ###########################################################################

    def extract_text(self, file_path: Path) -> str:

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return read_pdf_file(file_path)

        elif extension == ".docx":

            return read_word_file(file_path)

        elif extension == ".txt":

            return read_text_file(file_path)

        else:

            raise ValueError(
                f"Unsupported document type: {extension}"
            )

    ###########################################################################
    # Validation Functions
    ###########################################################################

    def validate_file_exists(self, file_path: Path ) -> bool:

        if not file_path.exists():
            raise FileNotFoundError(
                f"File does not exist: {file_path}"
            )
        logger.info("File exists.")
        return True

    ###########################################################################

    def validate_file_extension(self, file_path: Path ) -> bool:

        extension = file_path.suffix.lower()

        if extension not in self.supported_extensions:
            raise ValueError(
                f"Unsupported file extension: {extension}"
            )
        logger.info(
            f"Valid extension: {extension}"
        )
        return True

    ###########################################################################

    def validate_file_size(self, file_path: Path ) -> bool:

        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            raise ValueError(
                f"File size ({size_mb:.2f} MB) exceeds "
                f"Maximum allowed size "
                f"({self.config.max_file_size_mb} MB)."
            )
        logger.info(
            f"File size validated ({size_mb:.2f} MB)."
        )
        return True

    ###########################################################################

    def validate_file_readable(self, file_path: Path ) -> bool:
        try:
            extension = file_path.suffix.lower()

            if extension == ".pdf":
                fitz.open(file_path).close()

            elif extension == ".docx":
                Document(file_path)

            elif extension == ".txt":
                with open(file_path, "r", encoding="utf-8"):
                    pass

        except Exception as e:
            raise ValueError(
                f"Unable to read document: {e}"
            )
        logger.info(
            "Document is readable."
        )
        return True

    ###########################################################################

    def validate_text_extraction(self, file_path: Path) -> bool:

        text = self.extract_text(file_path)
        if text is None:
            raise ValueError(
                "Text extraction failed."
            )
        logger.info(
            "Text extraction successful."
        )
        return True

    ###########################################################################

    def validate_empty_document(self, file_path: Path ) -> bool:

        text = self.extract_text(file_path)
        if len(text.strip()) == 0:
            raise ValueError(
                "Document contains no text."
            )
        logger.info(
            "Document is not empty."
        )
        return True

    ###########################################################################

    def validate_minimum_length(self, file_path: Path ) -> bool:

        text = self.extract_text(file_path)
        word_count = len(text.split())

        if word_count < self.config.min_words:
            raise ValueError(
                f"Document contains only "
                f"{word_count} words. "
                f"Minimum required is "
                f"{self.config.min_words}."
            )
        logger.info(
            f"Word count validated ({word_count} words)."
        )
        return True


    ###########################################################################

    def validate_all(self, file_path: Path) -> Path | bool:
        try:
            self.validate_file_exists(file_path)
            self.validate_file_extension(file_path)
            self.validate_file_size(file_path)
            self.validate_file_readable(file_path)
            self.validate_text_extraction(file_path)
            self.validate_empty_document(file_path)
            self.validate_minimum_length(file_path)

            destination = self.config.valid_dir / file_path.name
            shutil.copy2(file_path, destination)

            logger.info(f"Validation successful: {destination}")
            return destination

        except Exception as e:

            destination = self.config.invalid_dir / file_path.name
            shutil.copy2(file_path, destination)

            logger.error(f"Validation failed: {e}")
            return False