from sentence_transformers import SentenceTransformer, util

_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_recap(previous_notes: list[str], current_summary: str) -> list[str]:
    """
    STEP 7: Recap generation using SBERT + similarity
    """

    embeddings = _model.encode(previous_notes + [current_summary])
    scores = util.cos_sim(embeddings[-1], embeddings[:-1])

    return [
        note for note, score in zip(previous_notes, scores[0])
        if score > 0.6
    ]
