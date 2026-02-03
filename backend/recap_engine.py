from sentence_transformers import SentenceTransformer, util

_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def generate_recap(previous_summaries, current_summary: str) -> str:
    """
    Generate recap using SBERT similarity
    """

    if not previous_summaries:
        return "No previous meetings found."

    embeddings = _MODEL.encode(previous_summaries + [current_summary])
    current_emb = embeddings[-1]
    past_embs = embeddings[:-1]

    scores = util.cos_sim(current_emb, past_embs)[0]

    relevant = [
        previous_summaries[i]
        for i, score in enumerate(scores)
        if score > 0.55
    ]

    if not relevant:
        return "No strong overlap with previous meetings."

    recap = "Related points from previous meetings:\n\n"
    for i, text in enumerate(relevant, 1):
        recap += f"{i}. {text}\n"

    return recap
