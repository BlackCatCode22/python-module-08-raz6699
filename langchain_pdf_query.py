import openai
import os
import streamlit as st
from apikey import apikey
os.environ["OPENAI_API_KEY"] = apikey

from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from PyPDF2 import PdfReader
from langchain_core.prompts import PromptTemplate
prompt_template = "{question}"
prompt = PromptTemplate(
    input_variables=["question"], template=prompt_template
)
llm = LLMChain(llm=OpenAI(), prompt=prompt)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
apikey = os.getenv("OPENAI_API_KEY")

# Configure the OpenAI library with your API key
openai.api_key = apikey

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def main():
    # Streamlit for web page interface
    # ----HEADER SECTION----
    st.set_page_config(page_title="Chatbot PDF Reader",  page_icon="🤖", layout="wide")
    st.header("Python Chatbot using Streamlit and OpenAI ChatGPT 3.5 using Langchain for PDF Text Querying")
    st.title("Chatbot PDF Reader")
    st.divider()
    # ----MAIN SECTION----
    pdf =st.file_uploader("Upload your PDF", type="pdf")
    st.divider()
    # Extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # st.write(text)

        # Split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)

        # st.write(chunks)

        # Create embeddings from OpenAI
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Show user input
        user_question = st.text_input("Ask a question about your PDF:")
        st.divider()
        # ----OUTPUT SECTION----
        if user_question:
            # Search chunks in knowledge_base based on user question
            docs = knowledge_base.similarity_search(user_question)
            st.write(docs)
            # load_qa_chain does not work with the OpenAI wrapper in langchain
            chain = prompt | llm
            # user query that will return an answer if information is stored in knowledge_base
            response = chain.invoke(user_question)
            st.write(response)

if __name__ == "__main__":
    main()