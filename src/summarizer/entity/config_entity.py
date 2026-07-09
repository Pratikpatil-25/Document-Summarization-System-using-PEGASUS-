from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen = True) # frozen enures that once an instance of the following class is created the class attributes can't be modified.
class DocIngestionConfig:
  root_dir: Path
  upload_dir: Path
  supported_extensions: list[str]

@dataclass(frozen = True)
class DocValidationConfig:
  root_dir: Path
  valid_dir: Path
  invalid_dir: Path
  supported_extensions: list[str]
  max_file_size_mb: int
  min_words: int

@dataclass(frozen = True)
class TextExtractionConfig:
  root_dir: Path
  valid_dir: Path
  extracted_dir: Path

@dataclass(frozen = True)
class DocPreprocessingConfig:
  root_dir: Path
  extracted_dir: Path
  preprocessed_dir: Path

@dataclass(frozen = True)
class ChunkingConfig:
  root_dir: Path
  preprocessed_dir: Path
  chunked_dir: Path
  tokenizer_name : str
  chunk_size : int
  overlap : int 

@dataclass(frozen = True)
class SummarizingConfig:
  root_dir: Path
  chunked_dir: Path
  summarized_chunks: Path
  summarized_files: Path
  model_name : str
  max_length : int
  min_length : int
  do_sample : bool
  temperature : float

