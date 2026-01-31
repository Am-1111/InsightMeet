from transformers import pipeline

_summarizer = pipeline(
    task="text2text-generation",
    model="facebook/bart-large-cnn"
)

def summarize_text(text: str) -> str:
    """
    STEP 4: Abstractive summarization using BART
    """

    if len(text.strip()) < 50:
        return "Transcript too short to summarize."

    result = _summarizer(
        text,
        max_length=130,
        min_length=40,
        do_sample=False
    )

    return result[0]["generated_text"]
