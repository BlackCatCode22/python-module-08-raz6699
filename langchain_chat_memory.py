import streamlit as st
import openai
import os
from apikey import apikey
os.environ["OPENAI_API_KEY"] = apikey

from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
apikey = os.getenv("OPENAI_API_KEY")

# Configure the OpenAI library with your API key
openai.api_key = apikey

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def main():
    # Initialize Streamlit application
    st.set_page_config(page_title="Recipe Suggester Chatbot with Chat Memory", page_icon="🤖", layout="wide")

    # ----HEADER SECTION----
    with st.container():
        st.header("Python Chatbot using Streamlit and OpenAI ChatGPT 3.5 using LangChain for Entity Memory")
        st.title("Recipe Suggester Assistant")
        st.divider()

    # ----MAIN SECTION----
    with st.container():
        user_input = st.text_input("Ask me anything about Recipes", "")
        st.divider()

    # ----OUTPUT SECTION----
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            with st.chat_message("user"):
                st.write(":green[_Your question_:]", user_input)  # Display user input

        with right_column:
            with st.chat_message("assistant"):
                try:
                    # Entity memory remembers certain entities in a conversation history
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9)
                    conversation = ConversationChain(llm=llm, memory=ConversationEntityMemory(llm=llm),
                                                     prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE, verbose=False)

                    # Generate a response using OpenAI's GPT-3.5-turbo
                    response = conversation.predict(input=user_input)

                    # Display the response
                    st.write("🤖 :red[_Chatbot Response_:]", response)

                except Exception as e:
                    st.write("🤖 :red[Chatbot Response:]", e)
                    return "I'm sorry, I couldn't generate a response."

if __name__ == "__main__":
    main()