from transformers import pipeline

_ner = pipeline(
    "token-classification",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

def extract_action_items(text: str) -> list[str]:
    """
    STEP 5: Action item extraction using NER
    """

    entities = _ner(text)
    actions = []

    for ent in entities:
        if ent["entity_group"] == "PER":
            actions.append(f"Action involving {ent['word']}")

    return list(set(actions))
