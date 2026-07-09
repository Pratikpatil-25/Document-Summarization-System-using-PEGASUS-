from pathlib import Path
from typing import List

from transformers import PegasusForConditionalGeneration, PegasusTokenizer

from src.summarizer.entity.config_entity import SummarizingConfig
from src.summarizer.logging import logger
from src.summarizer.utils.common import create_directories


class Summarizing:

    def __init__(self, config: SummarizingConfig, tokenizer, model):
        self.config = config
        self.tokenizer = tokenizer
        self.model = model

        create_directories([
            self.config.root_dir,
            self.config.summarized_chunks,
            self.config.summarized_files
        ])
        
        # logger.info("Loading Pegasus tokenizer...")

        # self.tokenizer = PegasusTokenizer.from_pretrained(model_name, local_files_only=True)

        # logger.info("Loading Pegasus model...")

        # self.model = PegasusForConditionalGeneration.from_pretrained(model_name, local_files_only=True)

        # logger.info("Pegasus model loaded successfully.")

    def summarize_document( self, chunk_paths: List[Path] ) -> Path:

        chunk_summaries = []
        for chunk_path in chunk_paths:
            logger.info(f"Summarizing {chunk_path.name}")

            with open(chunk_path, "r", encoding="utf-8") as file:
                chunk_text = file.read()

            inputs = self.tokenizer(
                chunk_text,
                truncation=True,
                padding="longest",
                max_length=1024,
                return_tensors="pt"
            )

            summary_ids = self.model.generate(
                **inputs,
                max_length=200,
                min_length=50,
                num_beams=4,
                early_stopping=True
            )

            summary = self.tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True
            )

            summary_path = (
                self.config.summarized_chunks /
                f"{chunk_path.stem}_summary.txt"
            )

            with open(summary_path, "w", encoding="utf-8") as file:
                file.write(summary)

            logger.info(
                f"Summary saved at {summary_path}"
            )

            chunk_summaries.append(summary)

        final_summary = "\n\n".join(chunk_summaries)

        output_path = (
            self.config.summarized_files /
            "final_summary.txt"
        )

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(final_summary)

        logger.info(
            f"Final summary saved at {output_path}"
        )

        return output_path