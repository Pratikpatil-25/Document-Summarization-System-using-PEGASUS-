from src.summarizer.logging import logger
from fastapi import UploadFile

from src.summarizer.components.doc_ingestion import DocIngestion
from src.summarizer.components.doc_validation import DocValidation
from src.summarizer.components.text_extraction import TextExtraction
from src.summarizer.components.doc_preprocessing import DocPreprocessing

class PredictionPipeline:

    def __init__(self, config): 
        self.config = config
        self.doc_ingestion = DocIngestion(config.get_doc_ingestion_config())
        self.doc_validation = DocValidation(config.get_doc_validation_config())
        self.text_extraction = TextExtraction(config.get_text_extraction_config())
        self.doc_preprocessing = DocPreprocessing(config.get_doc_preprocessing_config())

        # self.tokenizer = Tokenizer()
        # self.chunker = Chunker()
        # self.summarizer = Summarizer()
        # self.postprocessor = Postprocessor()

    def predict(self, uploaded_file : UploadFile) -> str:

        saved_path = self.doc_ingestion.save_document(uploaded_file)

        file_path = self.doc_validation.validate_all(saved_path)
        
        if file_path is False:
            raise ValueError("Uploaded document is invalid.")
        
        else : 
            extracted_text_path = self.text_extraction.extract_text(file_path)

            # accces file from valid_files directory after validation and then clean it
            cleaned_text = self.doc_preprocessing.preprocess(extracted_text_path)

        # tokenized_text = self.tokenizer.tokenize(cleaned_text)

        # chunks = self.chunker.chunk_text(tokenized_text)

        # summary = self.summarizer.generate_summary(chunks)

        # summary = self.postprocessor.postprocess(summary)

        return cleaned_text  # Return cleaned text path for now, replace with summary when implemented