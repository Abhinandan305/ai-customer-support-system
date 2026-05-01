from llm import llm_generate
from rag import retrieve_context


def base_agent(role, query):
    context = retrieve_context(query)

    prompt = f"""
You are a {role} in a company support system.

Use ONLY the policy context below:
{context}

If answer is not in context, say:
"I don't have enough information in company policy."

User query: {query}
"""

    return {"message": llm_generate(prompt)}


def billing_agent(query):
    return base_agent("Billing Specialist", query)

def tech_agent(query):
    return base_agent("Technical Support Engineer", query)

def refund_agent(query):
    return base_agent("Refund Policy Expert", query)

def faq_agent(query):
    return base_agent("FAQ Assistant", query)