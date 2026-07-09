from src.summarizer.logging import logger
from fastapi import UploadFile
from pathlib import Path
from typing import List
from src.summarizer.components.doc_ingestion import DocIngestion
from src.summarizer.components.doc_validation import DocValidation
from src.summarizer.components.text_extraction import TextExtraction
from src.summarizer.components.doc_preprocessing import DocPreprocessing
from src.summarizer.components.chunking import Chunking
from src.summarizer.config.configuration import ConfigurationManager

class PredictionPipeline:

    def __init__(self, config: ConfigurationManager): 
        self.config = config
        self.doc_ingestion = DocIngestion(self.config.get_doc_ingestion_config())
        self.doc_validation = DocValidation(self.config.get_doc_validation_config())
        self.text_extraction = TextExtraction(self.config.get_text_extraction_config())
        self.doc_preprocessing = DocPreprocessing(self.config.get_doc_preprocessing_config())
        self.chunking = Chunking(self.config.get_chunking_config())

        # self.tokenizer = Tokenizer()
        # self.chunker = Chunker()
        # self.summarizer = Summarizer()
        # self.postprocessor = Postprocessor()

    def predict(self, uploaded_file : UploadFile) -> List[Path]:

        saved_path = self.doc_ingestion.save_document(uploaded_file)
        logger.info("Stage 1 : Document Ingestion Completed.")
        file_path = self.doc_validation.validate_all(saved_path)
        logger.info("Stage 2 : Document Validation Completed.")

        if file_path is False:
            raise ValueError("Uploaded document is invalid.")
        
        else : 
            extracted_text_path = self.text_extraction.extract_text(file_path)
            logger.info("Stage 3 : Text Extraction Completed.")
            # accces file from valid_files directory after validation and then clean it
            cleaned_text = self.doc_preprocessing.preprocess(extracted_text_path)
            logger.info("Stage 4 : Text Preprocessing Completed.")
            chunk_file_path = self.chunking.chunk_document(cleaned_text)  # returns list of chunk paths
            logger.info("Stage 5 : Document Chunking Completed.")

        # chunks = self.chunker.chunk_text(tokenized_text)

        # summary = self.summarizer.generate_summary(chunks)

        # summary = self.postprocessor.postprocess(summary)

        return chunk_file_path  # Return list of chunk paths for now, replace with summary when implemented