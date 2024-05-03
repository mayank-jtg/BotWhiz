import streamlit as st
from chat import agent_executor
from langchain_core.messages import AIMessage, HumanMessage

st.title("BotWhiz")

# Left side drawer options
option = st.sidebar.selectbox("Options", ("New Chat", "History", "Close"))

# Initialize session_state messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handling different options
if option == "New Chat":
    # Chat window
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hello! Welcome to BotWhiz! How can I help you today ?!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        chat_history = []
        for message in st.session_state.messages:
            if message["role"] == "user":
                chat_history.append(HumanMessage(message["content"]))
            else:
                chat_history.append(AIMessage(message["content"]))
        with st.chat_message("assistant"):
            with st.spinner("Crunching data for you ...."):
                output = agent_executor.invoke({"input": prompt, "chat_history": chat_history})
            response = st.write(output["output"])
        st.session_state.messages.append({"role": "assistant", "content": output['output']})

elif option == "History":
    # Show chat history grouped by type
    history = {}
    for message in st.session_state.messages:
        if message["role"] not in history:
            history[message["role"]] = []
        history[message["role"]].append(message["content"])

    # Display history with headings
    for role, messages in history.items():
        st.subheader(role.capitalize())
        for message in messages:
            st.write(message)

elif option == "Close":
    st.stop()

