from fastapi import FastAPI
from pydantic import BaseModel
import time

from router import classify_intent
from llm import llm_generate
from metrics import Metrics


# --------------------
# App Init
# --------------------

app = FastAPI(
    title="AI Customer Support System"
)

metrics = Metrics()


# --------------------
# Lazy Loaded Objects
# --------------------

cache = None


def get_cache():

    global cache

    if cache is None:
        from semantic_cache import SemanticCache

        cache = SemanticCache(
            threshold=0.85
        )

    return cache



def get_agents():

    from agents import (
        billing_agent,
        tech_agent,
        refund_agent,
        faq_agent
    )

    return (
        billing_agent,
        tech_agent,
        refund_agent,
        faq_agent
    )


# --------------------
# Token + Cost Helpers
# --------------------

def estimate_tokens(text):

    if not text:
        return 0

    return int(
        len(text.split()) * 1.3
    )


COST_PER_1K_TOKENS = 0.0002


def calculate_cost(tokens):

    return (
        tokens / 1000
    ) * COST_PER_1K_TOKENS



# --------------------
# Request Model
# --------------------

class QueryRequest(BaseModel):

    query: str



# --------------------
# Health Check
# --------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "service": "AI Customer Support System"
    }



# --------------------
# Chat Endpoint
# --------------------

@app.post("/chat")
async def chat(request: QueryRequest):

    start = time.time()

    query = request.query


    # --------------------
    # Load cache only when needed
    # --------------------

    cache_instance = get_cache()


    # --------------------
    # 1. Semantic Cache
    # --------------------

    cached_response = cache_instance.get(
        query
    )


    if cached_response is not None:

        latency = time.time() - start

        metrics.log_request(
            cache_hit=True
        )

        metrics.log_latency(
            "semantic_cache",
            latency
        )


        return {
            "status": "success",
            "route": "semantic_cache",
            "latency": latency,
            "response": {
                "message": str(cached_response)
            }
        }



    # --------------------
    # 2. Intent Routing
    # --------------------

    route = classify_intent(
        query
    )


    (
        billing_agent,
        tech_agent,
        refund_agent,
        faq_agent
    ) = get_agents()



    if route == "billing":

        response = billing_agent(
            query
        )


    elif route == "tech":

        response = tech_agent(
            query
        )


    elif route == "refund":

        response = refund_agent(
            query
        )


    elif route == "faq":

        response = faq_agent(
            query
        )


    else:

        response = {
            "message": llm_generate(
                query
            )
        }



    latency = time.time() - start



    # --------------------
    # 3. Normalize Response
    # --------------------

    if isinstance(response, dict):

        final_response = (
            response.get("message")
            or str(response)
        )

    else:

        final_response = str(
            response
        )



    if (
        not final_response
        or final_response == "None"
    ):

        final_response = (
            "Sorry, I couldn't generate a response."
        )



    # --------------------
    # 4. Store Cache
    # --------------------

    cache_instance.set(
        query,
        final_response
    )



    # --------------------
    # 5. Metrics
    # --------------------

    metrics.log_request(
        cache_hit=False
    )


    metrics.log_latency(
        route,
        latency
    )


    tokens_used = (
        estimate_tokens(query)
        +
        estimate_tokens(final_response)
    )


    cost = calculate_cost(
        tokens_used
    )


    metrics.log_cost(
        tokens_used,
        cost
    )



    return {

        "status": "success",

        "route": route,

        "latency": latency,

        "response": {

            "message": final_response

        }

    }



# --------------------
# Analytics Endpoint
# --------------------

@app.get("/analytics")
def analytics():

    return metrics.get_stats()