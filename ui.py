import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"
ANALYTICS_URL = "http://127.0.0.1:8000/analytics"

st.set_page_config(page_title="AI Customer Support", layout="wide")

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Dashboard")

show_analytics = st.sidebar.button("📊 Analytics Dashboard")

st.sidebar.markdown("---")
st.sidebar.markdown("💬 Chat History Stored Locally")

# ---------------- ANALYTICS ----------------
if show_analytics:
    try:
        response = requests.get(ANALYTICS_URL)
        data = response.json()

        st.sidebar.subheader("📊 Analytics")

        st.sidebar.write(f"Avg Latency: {data.get('avg_latency', 0):.2f}s")
        st.sidebar.write(f"Max Latency: {data.get('max_latency', 0):.2f}s")
        st.sidebar.write(f"Total Requests: {data.get('total_requests', 0)}")

        st.sidebar.write("Route Distribution:")
        st.sidebar.json(data.get("route_distribution", {}))

    except Exception as e:
        st.sidebar.error(f"Analytics error: {str(e)}")

# ---------------- TITLE ----------------
st.title("🤖 AI Customer Support System")

# ---------------- INPUT ----------------
query = st.text_input("Enter your issue:")

def extract_bot_reply(data):
    """Safe response extractor (handles all backend formats)"""
    resp = data.get("response", {})

    if isinstance(resp, dict):
        return resp.get("message") or "No response received from backend"

    if isinstance(resp, str):
        return resp

    return "No response received from backend"


# ---------------- CHAT ----------------
if st.button("Send") and query:

    try:
        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json={"query": query})

        data = response.json()

        bot_reply = extract_bot_reply(data)

        route = data.get("route", "unknown")
        latency = data.get("latency", 0)

        # save history
        st.session_state.chat_history.append({
            "user": query,
            "bot": bot_reply,
            "route": route,
            "latency": latency
        })

        # display latest response
        st.success(bot_reply)

        st.caption(f"🔀 Route: {route} | ⏱ Latency: {latency:.2f}s")

    except Exception as e:
        st.error(f"Request failed: {str(e)}")

# ---------------- CHAT HISTORY ----------------
st.markdown("## 💬 Conversation History")

for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**🧑 You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.caption(f"Route: {chat['route']} | Latency: {chat['latency']:.2f}s")
    st.markdown("---")

if st.sidebar.button("📊 Show Analytics"):
    response = requests.get("http://127.0.0.1:8000/analytics")

    if response.status_code == 200:
        data = response.json()

        st.sidebar.metric("💰 Cost", f"${data.get('total_cost', 0):.6f}")
        st.sidebar.metric("🔤 Tokens", data.get("total_tokens", 0))
    else:
        st.sidebar.error("Analytics unavailable")

        
