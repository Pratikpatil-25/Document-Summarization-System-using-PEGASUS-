import re
import unicodedata
from ensure import ensure_annotations


@ensure_annotations
def strip_text(text: str) -> str:
    """
    Remove leading and trailing whitespace.

    """
    return text.strip()


@ensure_annotations
def normalize_unicode(text: str) -> str:
    """
    Normalize Unicode characters into a standard format.

    Examples:
        “ ” -> "
        ‘ ’ -> '
        – — -> -
        … -> ...

    Args:
        text (str): Input text.

    Returns:
        str: Normalized text.
    """

    text = unicodedata.normalize("NFKC", text)

    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "…": "...",
        "ﬄ": "ffl",
        "ﬃ": "ffi",
        "ﬀ": "ff",
        "ﬂ": "fl",
        "ﬁ": "fi"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


@ensure_annotations
def remove_non_printable_characters(text: str) -> str:
    """
    Remove non-printable/control characters.

    """

    return "".join(
        char if char.isprintable() else " "
        for char in text
    )


@ensure_annotations
def remove_extra_whitespace(text: str) -> str:
    """
    Replace multiple spaces/tabs with a single space.

    """

    return re.sub(r"[ \t]+", " ", text)


@ensure_annotations
def remove_extra_newlines(text: str) -> str:
   
    # Replace multiple blank lines with a single blank line.

    return re.sub(r"\n\s*\n+", "\n\n", text)


@ensure_annotations
def remove_multiple_punctuation(text: str) -> str:
   

    # Example:
    #     !!!!! -> !
    #     ????? -> ?
    #     ...... -> .

  

    text = re.sub(r"!{2,}", "!", text)
    text = re.sub(r"\?{2,}", "?", text)
    text = re.sub(r"\.{2,}", ".", text)

    return text


@ensure_annotations
def remove_urls(text: str) -> str:

    return re.sub(r"https?://\S+|www\.\S+", "", text)


@ensure_annotations
def remove_email_addresses(text: str) -> str:

    return re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "",
        text,
    )


@ensure_annotations
def remove_page_numbers(text: str) -> str:
    
    return re.sub(r"(?m)^\s*\d+\s*$", "", text)


@ensure_annotations
def remove_headers_and_footers(text: str) -> str:
    
    # Remove repeated headers and footers

    lines = text.split("\n")
    line_frequency = {}

    for line in lines:
        stripped = line.strip()
        if stripped:
            line_frequency[stripped] = line_frequency.get(stripped, 0) + 1

    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped and line_frequency[stripped] > 3:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


@ensure_annotations
def clean_text(text: str) -> str:
    
    # Complete preprocessing pipeline.


    text = strip_text(text)
    text = normalize_unicode(text)
    text = remove_non_printable_characters(text)
    text = remove_urls(text)
    text = remove_email_addresses(text)
    text = remove_page_numbers(text)
    text = remove_headers_and_footers(text)
    text = remove_multiple_punctuation(text)
    text = remove_extra_whitespace(text)
    text = remove_extra_newlines(text)
    text = strip_text(text)

    return text