import streamlit as st
from langserve import RemoteRunnable
from langchain_core.messages import AIMessage, HumanMessage
from requests.exceptions import RequestException

# app config
st.set_page_config(page_title="Neo4j Chatbot", page_icon="🤖")
st.title("Knowledge Chatbot")

st.sidebar.title("RAG Settings")

if 'strategy' not in st.session_state:
    st.session_state.strategy = "typical_rag"

st.session_state.strategy = st.sidebar.selectbox("Strategy", [
    "typical_rag", "parent_strategy", "hypothetical_questions", "summary_strategy"
])


def get_response(user_query, chat_history, strategy):
    chain_url = "http://api:8080/neo4j-advanced-rag-memory"

    try:
        chain = RemoteRunnable(chain_url)
        chain.with_config({"strategy": strategy})
        response = chain.stream({
            "question": user_query,
            "chat_history": chat_history
        })
        return response
    except RequestException as e:
        st.error(f"Request failed: {e}")
        return None


# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, how can I help you?"),
    ]

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history, st.session_state.strategy))

    st.session_state.chat_history.append(AIMessage(content=response))
