"""Streamlit 기본 채팅봇.

실행:
    streamlit run web/streamlit_app.py
"""
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="ChatGPT", page_icon="💬")
st.title("ChatGPT 💬")

llm = ChatOpenAI(model="gpt-4o-mini")

# ── 메시지 상태 관리 ─────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── 대화 표시 ────────────────────────────────────────
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

# ── 사용자 입력 처리 ──────────────────────────────────
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    # LangChain 메시지 변환
    msgs = [HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in st.session_state.messages]
    
    with st.chat_message("assistant"):
        answer = st.write_stream(llm.stream(msgs))
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
