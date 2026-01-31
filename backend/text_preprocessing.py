from transformers import AutoTokenizer

_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_text(text: str) -> list[str]:
    """
    STEP 3: Text tokenization
    """

    tokens = _tokenizer.tokenize(text)
    return tokens
