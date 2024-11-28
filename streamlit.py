import streamlit as st
import openai
from dotenv import load_dotenv
import os
from apikey import apikey

os.environ["OPENAI_API_KEY"] = apikey

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
apikey = os.getenv("OPENAI_API_KEY")

# Configure the OpenAI library with your API key
openai.api_key = apikey

from openai import OpenAI
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def main():
    # Initialize Streamlit application
    # streamlit run filepath
    st.set_page_config(page_title="Recipe Suggester Chatbot", page_icon="mag", layout="wide")

    # ----HEADER SECTION----
    with st.container():
        st.header("Python Chatbot using Streamlit and OpenAI ChatGPT 3.5")
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
                        if user_input:
                            completion = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system",
                                     "content": "You are a wonderful assistant for aspiring chefs named Bella, and you help them find delicious recipes, suggest creative meal ideas, and guide them through cooking step-by-step. You are knowledgeable about various cuisines, dietary restrictions, and cooking techniques. Your goal is to make cooking enjoyable and accessible for everyone."},
                                    {"role": "user", "content": user_input}
                                ]
                            )

                            answer = completion.choices[0].message.content
                            st.write("🤖 :red[_Chatbot Response_:]", answer)

                except Exception as e:
                    st.write("🤖 :red[Chatbot Response:]", e)
                    return "I'm sorry, I couldn't generate a response."

if __name__ == "__main__":
    main()
