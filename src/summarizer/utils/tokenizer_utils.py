from typing import List
from ensure import ensure_annotations
from transformers import AutoTokenizer, PreTrainedTokenizerBase
from nltk.tokenize import sent_tokenize



def load_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
    """
    Load a Hugging Face tokenizer.

    Args:
        model_name (str): Hugging Face model name.

    Returns:
        PreTrainedTokenizerBase: Loaded tokenizer.
    """

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return tokenizer


@ensure_annotations
def count_tokens(text: str,tokenizer: PreTrainedTokenizerBase) -> int:
    """
    Count the number of tokens in the text.

    Args:
        text (str): Input text.
        tokenizer: Hugging Face tokenizer.

    Returns:
        int: Number of tokens.
    """

    tokens = tokenizer.encode(
        text,
        add_special_tokens=True
    )

    return len(tokens)


@ensure_annotations
def is_text_too_long(text: str,tokenizer: PreTrainedTokenizerBase,max_tokens: int) -> bool:
    """
    Check whether text exceeds the maximum token limit.

    Args:
        text (str): Input text.
        tokenizer: Hugging Face tokenizer.
        max_tokens (int): Maximum allowed tokens.

    Returns:
        bool: True if text exceeds limit.
    """

    return count_tokens(text, tokenizer) > max_tokens


@ensure_annotations
def truncate_text(text: str,tokenizer: PreTrainedTokenizerBase, max_tokens: int) -> str:
    """
    Truncate text to the specified number of tokens.

    Args:
        text (str): Input text.
        tokenizer: Hugging Face tokenizer.
        max_tokens (int): Maximum tokens.

    Returns:
        str: Truncated text.
    """

    tokenized = tokenizer(
        text,
        truncation=True,
        max_length=max_tokens,
        return_tensors=None
    )

    truncated_text = tokenizer.decode(
        tokenized["input_ids"],
        skip_special_tokens=True
    )

    return truncated_text





def split_into_token_chunks(
    text: str,
    tokenizer: PreTrainedTokenizerBase,
    chunk_size: int,
    overlap: int = 0
):
    """
    Split text into chunks without breaking sentences.

    Each chunk contains as many complete sentences as possible
    while staying below chunk_size tokens.
    """

    sentences = sent_tokenize(text)

    chunks = []

    current_chunk = []

    current_tokens = 0

    for sentence in sentences:

        sentence_tokens = len(
            tokenizer.encode(
                sentence,
                add_special_tokens=False
            )
        )

        # Sentence itself larger than chunk
        if sentence_tokens > chunk_size:

            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_tokens = 0

            token_ids = tokenizer.encode(
                sentence,
                add_special_tokens=False
            )

            step = chunk_size - overlap

            for i in range(0, len(token_ids), step):

                part = tokenizer.decode(
                    token_ids[i:i + chunk_size],
                    skip_special_tokens=True
                )

                chunks.append(part)

            continue

        if current_tokens + sentence_tokens <= chunk_size:

            current_chunk.append(sentence)

            current_tokens += sentence_tokens

        else:

            chunks.append(" ".join(current_chunk))

            current_chunk = [sentence]

            current_tokens = sentence_tokens

    if current_chunk:

        chunks.append(" ".join(current_chunk))

    return chunks