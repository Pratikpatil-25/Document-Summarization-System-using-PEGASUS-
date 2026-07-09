from transformers import (
    AutoTokenizer,
    PegasusForConditionalGeneration
)

from src.summarizer.logging import logger


class ModelManager:

    def __init__(self, model_name: str):

        logger.info("Loading tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            local_files_only=True   
        )

        logger.info("Loading Pegasus model...")

        self.model = PegasusForConditionalGeneration.from_pretrained(
            model_name,
            local_files_only=True  
        )

        logger.info("Tokenizer and model loaded successfully.")