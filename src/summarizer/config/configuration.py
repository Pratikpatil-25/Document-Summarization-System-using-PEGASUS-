from src.summarizer.constants import *
from src.summarizer.utils.common import read_yaml, create_directories
from src.summarizer.entity.config_entity import (DocIngestionConfig, 
                                                 DocValidationConfig, 
                                                 DocPreprocessingConfig, 
                                                 TextExtractionConfig,
                                                 ChunkingConfig,
                                                 SummarizingConfig)
from pathlib import Path

class ConfigurationManager:
    def __init__(
        self,
        config_file_path = CONFIG_FILE_PATH,
        params_file_path = PARAMS_FILE_PATH,
        schema_file_path = SCHEMA_FILE_PATH):

        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)

        create_directories([self.config.artifacts_root])


    def get_doc_ingestion_config(self) -> DocIngestionConfig:
        config = self.config.document_ingestion

        create_directories([config.root_dir])

        doc_ingestion_config = DocIngestionConfig(
            root_dir=Path(config.root_dir),
            upload_dir=Path(config.upload_dir),
            supported_extensions=config.supported_extensions,
        )

        return doc_ingestion_config
    
    def get_doc_validation_config(self) -> DocValidationConfig:
        config = self.config.document_validation

        create_directories([config.root_dir, config.valid_dir, config.invalid_dir])

        doc_validation_config = DocValidationConfig(
            root_dir=Path(config.root_dir),
            valid_dir=Path(config.valid_dir),
            invalid_dir=Path(config.invalid_dir),
            supported_extensions=config.supported_extensions,
            max_file_size_mb=config.max_file_size_mb,
            min_words=config.min_words
        )

        return doc_validation_config
    
    def get_text_extraction_config(self) -> TextExtractionConfig:
        config = self.config.text_extraction

        create_directories([config.root_dir, config.extracted_dir])

        text_extraction_config = TextExtractionConfig(
            root_dir=Path(config.root_dir),
            valid_dir=Path(config.valid_dir),
            extracted_dir=Path(config.extracted_dir)
        )

        return text_extraction_config

    def get_doc_preprocessing_config(self) -> DocPreprocessingConfig:
        config = self.config.document_preprocessing

        create_directories([config.root_dir, config.preprocessed_dir])

        doc_preprocessing_config = DocPreprocessingConfig(
            root_dir=Path(config.root_dir),
            extracted_dir=Path(config.extracted_dir),
            preprocessed_dir=Path(config.preprocessed_dir)
        )

        return doc_preprocessing_config
    
    def get_chunking_config(self) -> ChunkingConfig:
        config = self.config.chunking
        params = self.params.chunking

        create_directories([config.root_dir, config.chunked_dir])

        chunking_config = ChunkingConfig(
            root_dir=Path(config.root_dir),
            preprocessed_dir=Path(config.preprocessed_dir),
            chunked_dir=Path(config.chunked_dir),
            tokenizer_name = params.tokenizer_name,
            chunk_size=params.chunk_size,
            overlap = params.overlap
        )

        return chunking_config
    
    def get_summarizing_config(self) -> SummarizingConfig:
        config = self.config.summarizing
        params = self.params.summarizing

        create_directories([config.root_dir, config.summarized_chunks, config.summarized_files])

        summarizing_config = SummarizingConfig(
            root_dir = Path(config.root_dir),
            chunked_dir = Path(config.chunked_dir),
            summarized_chunks = Path(config.summarized_chunks),
            summarized_files = Path(config.summarized_files),
            model_name = params.model_name,
            max_length = params.max_length,
            min_length = params.min_length,
            do_sample = params.do_sample,
            temperature = params.temperature
        )

        return summarizing_config
        
