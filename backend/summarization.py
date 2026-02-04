from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

_MODEL = None
_TOKENIZER = None

def _load_model():
    global _MODEL, _TOKENIZER

    if _MODEL is None or _TOKENIZER is None:
        print("🔄 Loading summarization model...")
        _TOKENIZER = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        _MODEL = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    if not text.strip():
        return ""

    _load_model()

    inputs = _TOKENIZER(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    with torch.no_grad():
        summary_ids = _MODEL.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=50,
            do_sample=False
        )

    return _TOKENIZER.decode(summary_ids[0], skip_special_tokens=True)
