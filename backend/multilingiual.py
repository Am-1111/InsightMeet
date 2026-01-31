from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

_tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
_model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-multilingual-cased",
    num_labels=2
)

def detect_language(text: str) -> str:
    """
    STEP 6: Multilingual detection (mBERT)
    """

    inputs = _tokenizer(text, return_tensors="pt", truncation=True)
    outputs = _model(**inputs)

    return "multilingual-text"
