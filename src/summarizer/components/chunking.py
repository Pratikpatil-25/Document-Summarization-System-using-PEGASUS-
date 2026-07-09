from pathlib import Path
from typing import List

from src.summarizer.entity.config_entity import ChunkingConfig
from src.summarizer.logging import logger

from src.summarizer.utils.common import create_directories
from src.summarizer.utils.tokenizer_utils import split_into_token_chunks

# from src.summarizer.utils.tokenizer_utils import load_tokenizer, split_into_token_chunks


class Chunking:
    
    def __init__(self, config: ChunkingConfig, tokenizer):
        self.config = config
        self.tokenizer = tokenizer
        
        create_directories([
            self.config.root_dir, 
            self.config.chunked_dir
            ])

        # self.tokenizer = load_tokenizer(
        #     self.config.tokenizer_name
        # )

    def chunk_document(self, file_path: Path ) -> List[Path]:
       
        logger.info( f"Chunking document: {file_path.name}" )

        with open( file_path, "r", encoding="utf-8" ) as file:
            text = file.read()

        chunks = split_into_token_chunks(
            text=text,
            tokenizer=self.tokenizer,
            chunk_size=self.config.chunk_size,
            overlap=self.config.overlap
        )

        chunk_paths = []

        for index, chunk in enumerate(chunks, start=1):
            chunk_path = ( self.config.chunked_dir / f"{file_path.stem}_chunk_{index}.txt" )

            with open( chunk_path, "w", encoding="utf-8" ) as chunk_file:
                chunk_file.write(chunk)

            chunk_paths.append(chunk_path)

            logger.info(
                f"Chunk {index} saved at {chunk_path}"
            )

        logger.info(
            f"Generated {len(chunk_paths)} chunks."
        )

        return chunk_paths