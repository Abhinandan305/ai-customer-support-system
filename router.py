from llm import llm_generate

def classify_intent(query):
    prompt = f"""
Classify into: billing, tech, refund, faq

Query: {query}

Return only one word.
"""
    return llm_generate(prompt).strip().lower()