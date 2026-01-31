import re
from collections import Counter

ACTION_KEYWORDS = [
    "will", "need to", "should", "assign",
    "prepare", "complete", "follow up"
]

DECISION_KEYWORDS = [
    "decided", "final", "approved", "confirmed"
]

URGENCY_KEYWORDS = [
    "today", "tomorrow", "deadline", "asap", "urgent"
]


def sentence_split(text: str) -> list[str]:
    return re.split(r'(?<=[.!?]) +', text)


def impact_score(sentence: str, freq_counter: Counter) -> float:
    score = 0.0
    s = sentence.lower()

    # Action signals
    score += sum(1 for w in ACTION_KEYWORDS if w in s) * 2.5

    # Decision signals
    score += sum(1 for w in DECISION_KEYWORDS if w in s) * 3.0

    # Urgency
    score += sum(1 for w in URGENCY_KEYWORDS if w in s) * 2.0

    # Length importance
    score += min(len(sentence.split()) / 20, 1.5)

    # Repetition importance
    score += freq_counter[s] * 0.5

    return round(score, 2)


def run_impact_score(transcript: str, top_k: int = 5) -> list[dict]:
    """
    IMPACTScore™ – Custom importance ranking model
    """

    sentences = sentence_split(transcript)
    freq_counter = Counter(s.lower() for s in sentences)

    scored = [
        {
            "sentence": s,
            "score": impact_score(s, freq_counter)
        }
        for s in sentences
        if len(s.strip()) > 10
    ]

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]
