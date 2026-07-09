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

