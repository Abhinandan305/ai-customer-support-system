def hallucination_check(answer, context):
    """
    Simple but effective rule-based verifier
    """

    context_words = set(context.lower().split())
    answer_words = set(answer.lower().split())

    overlap = len(context_words.intersection(answer_words))

    # if very low overlap → likely hallucination
    if overlap < 5:
        return False

    # also block unsafe generic answers
    banned_phrases = [
        "as an AI I think",
        "I believe",
        "probably",
        "you should contact support for details"
    ]

    for phrase in banned_phrases:
        if phrase in answer.lower():
            return False

    return True