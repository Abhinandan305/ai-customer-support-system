from rag import retrieve_policy
from llm import llm_generate


def answer_with_rag(query: str):
    # Step 1: retrieve relevant company policies
    docs = retrieve_policy(query)

    context = "\n".join(docs)

    # Step 2: send to LLM with grounding
    prompt = f"""
You are a company customer support assistant.

You MUST answer ONLY using the context below.
If the answer is not in the context, say:
"I don't have enough information in company policy."

Context:
{context}

User question:
{query}

Answer clearly and professionally:
"""

    return llm_generate(prompt)