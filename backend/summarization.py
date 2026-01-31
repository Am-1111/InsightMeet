from transformers import BartTokenizer, BartForConditionalGeneration
import torch

# Load once (cached)
_TOKENIZER = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
_MODEL = BartForConditionalGeneration.from_pretrained(
    "facebook/bart-large-cnn"
)

def summarize_text(text: str, max_length: int = 130, min_length: int = 40) -> str:
    """
    STEP: Text Summarization using BART (architecture-faithful)
    Python 3.13 safe, no pipeline dependency
    """

    if not text or len(text.strip()) < 50:
        return "Transcript too short to summarize."

    inputs = _TOKENIZER(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    summary_ids = _MODEL.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    return _TOKENIZER.decode(
        summary_ids[0],
        skip_special_tokens=True
    )
