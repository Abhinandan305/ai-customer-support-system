from app import app
from rag import retrieve_context
from verifier import hallucination_check

test_cases = [
    "Can I get refund after 10 days?",
    "Why was I charged twice?",
    "My app is crashing on login",
    "Do you support PayPal?",
    "What is your refund policy?"
]

results = []

for q in test_cases:
    context = retrieve_context(q)

    # simulate agent output
    from agents import base_agent
    res = base_agent("Test Agent", q)["message"]

    valid = hallucination_check(res, context)

    results.append({
        "query": q,
        "response": res,
        "valid": valid
    })

print(results)