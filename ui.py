import streamlit as st
import requests

# ---------------- CONFIG ----------------

API_URL = "https://ai-customer-support-system-5sd2.onrender.com/chat"
ANALYTICS_URL = "https://ai-customer-support-system-5sd2.onrender.com/analytics"

st.set_page_config(
    page_title="AI Customer Support",
    layout="wide"
)


# ---------------- SESSION STATE ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙️ Dashboard")

st.sidebar.markdown("---")
st.sidebar.markdown("💬 Chat History Stored Locally")


# ---------------- ANALYTICS ----------------

if st.sidebar.button("📊 Analytics Dashboard"):

    try:
        response = requests.get(
            ANALYTICS_URL,
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            st.sidebar.subheader("📊 Analytics")

            st.sidebar.write(
                f"Avg Latency: {data.get('avg_latency', 0):.2f}s"
            )

            st.sidebar.write(
                f"Max Latency: {data.get('max_latency', 0):.2f}s"
            )

            st.sidebar.write(
                f"Total Requests: {data.get('total_requests', 0)}"
            )

            st.sidebar.write("Route Distribution:")

            st.sidebar.json(
                data.get("route_distribution", {})
            )

            st.sidebar.metric(
                "💰 Cost",
                f"${data.get('total_cost',0):.6f}"
            )

            st.sidebar.metric(
                "🔤 Tokens",
                data.get("total_tokens",0)
            )

        else:
            st.sidebar.error(
                "Analytics unavailable"
            )

    except Exception as e:
        st.sidebar.error(
            f"Analytics error: {str(e)}"
        )


# ---------------- TITLE ----------------

st.title("🤖 AI Customer Support System")


# ---------------- INPUT ----------------

query = st.text_input(
    "Enter your issue:"
)


def extract_bot_reply(data):

    response = data.get(
        "response",
        {}
    )

    if isinstance(response, dict):

        return (
            response.get("message")
            or "No response received"
        )

    if isinstance(response, str):
        return response

    return "No response received"



# ---------------- CHAT ----------------

if st.button("Send") and query:

    try:

        with st.spinner("Thinking..."):

            response = requests.post(
                API_URL,
                json={
                    "query": query
                },
                timeout=90
            )


        if response.status_code != 200:

            st.error(
                f"Backend error: {response.status_code}"
            )

        else:

            data = response.json()


            bot_reply = extract_bot_reply(
                data
            )

            route = data.get(
                "route",
                "unknown"
            )

            latency = data.get(
                "latency",
                0
            )


            st.session_state.chat_history.append(
                {
                    "user": query,
                    "bot": bot_reply,
                    "route": route,
                    "latency": latency
                }
            )


            st.success(
                bot_reply
            )


            st.caption(
                f"🔀 Route: {route} | ⏱ Latency: {latency:.2f}s"
            )


    except requests.exceptions.Timeout:

        st.error(
            "Request timed out. Backend is taking too long."
        )


    except Exception as e:

        st.error(
            f"Request failed: {str(e)}"
        )



# ---------------- HISTORY ----------------

st.markdown(
    "## 💬 Conversation History"
)


if st.session_state.chat_history:

    for chat in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f"**🧑 You:** {chat['user']}"
        )

        st.markdown(
            f"**🤖 Bot:** {chat['bot']}"
        )

        st.caption(
            f"Route: {chat['route']} | "
            f"Latency: {chat['latency']:.2f}s"
        )

        st.markdown("---")