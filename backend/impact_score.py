from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load once (cached)
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def extract_impact_points(text: str, top_k: int = 5):
    """
    Custom IMPACTScore™
    Extracts the most important sentences from transcript
    """

    # Split transcript into sentences
    sentences = [
        s.strip()
        for s in text.split(".")
        if len(s.strip()) > 20
    ]

    if not sentences:
        return []

    # Encode sentences
    embeddings = _MODEL.encode(sentences)

    # Compute centroid
    centroid = np.mean(embeddings, axis=0)

    # Similarity with centroid
    scores = util.cos_sim(centroid, embeddings)[0]

    # Rank sentences
    ranked = sorted(
        zip(sentences, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # Top-k results
    results = []
    for sent, score in ranked[:top_k]:
        results.append({
            "sentence": sent,
            "score": round(float(score), 3)
        })

    return results
