# 🤖 AI Customer Support System

## 🚀 Features
- LLM-powered chatbot (Groq)
- Semantic caching (FAISS)
- RAG-based policy retrieval
- Intent routing
- Observability (latency, cache hit rate, token cost)

## 🧠 Tech Stack
Python, FastAPI, Streamlit, FAISS, Docker

## 📊 Metrics
- Cache hit rate
- Latency per route
- Token usage & cost

## ⚡ Run Locally
uvicorn app:app --reload
streamlit run ui.py
