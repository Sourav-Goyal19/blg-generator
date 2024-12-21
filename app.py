import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Generate Blogs",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Generate Blogs 🔥")

input_text = st.text_input("Enter the Blog Topic")

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input("No. of words")
with col2:
    blog_style = st.selectbox(
        "Writing the blog for",
        ("Researchers", "Data Scientists", "Common People"),
        index=0,
    )

submit = st.button("Generate")


def generate_blog(title, words_count, blog_type):
    llm = ChatGroq(
        api_key=groq_api_key,
        model="llama3-8b-8192",
        temperature=0.01,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are an advanced AI language model that generates high-quality blogs tailored to different audiences."
                    "Focus on clarity, creativity, and engagement while adhering to the specified number of words."
                )
            ),
            HumanMessage(
                content=(
                    f"Write a blog titled '{title}' in {words_count} words. The blog should be written for {blog_type}. "
                    "Make it engaging and informative."
                )
            ),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(
        {"title": title, "words_count": words_count, "blog_type": blog_type}
    )

    return response


if submit:
    st.text("Making Blog..........")
    st.write(generate_blog(input_text, no_words, blog_style))
