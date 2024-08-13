import os
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
PASSWORD = st.secrets["PASSWORD"]

def read_article(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'articles', file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

article1 = read_article("article1.txt")
article2 = read_article("article2.txt")
article3 = read_article("article3.txt")
articles = "Article 1: \n" + article1 + "\n\n-----\n\n" + "Article 2: \n" + article2 + "\n\n-----\n\n" + "Article 3: \n" + article3

def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter the password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter the password", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password")
        return False
    else:
        return True

if check_password():
    model = ChatAnthropic(
        temperature=0,
        api_key=ANTHROPIC_API_KEY,
        model_name="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        streaming=True
    )

    prompt = ChatPromptTemplate.from_template("""
    Generate a comprehensive scientific review article on "{topic}" in the style of a published academic paper, starting directly with the title and abstract. Do not include any introductory statements before the article itself.

    The article should:

    1. Have a clear, descriptive title
    2. Begin with an abstract summarizing the key points (100-150 words)
    3. Include an introduction providing context and outlining the scope of the review
    4. Present a detailed analysis of current research, major findings, and breakthroughs
    5. Discuss key challenges, limitations, and open questions in the field
    6. Examine emerging trends and potential future directions
    7. Conclude with a synthesis of the main insights and their implications

    Base your review on these source articles: {articles}

    Ensure the article is well-structured with clear section headings, coherent paragraphs, and smooth transitions between ideas. Use formal academic language throughout. Include in-text citations and a reference list in a standard academic format (e.g. APA or MLA).

    The article should be written in English and be approximately 2000-3000 words long.

    Begin the article immediately without any preamble.
    """)

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    st.title("Scientific Article Generator")

    topic = st.text_input("Enter the topic of the article:")

    if st.button("Generate Article"):
        if topic:
            st.subheader("Generated Article:")
            output_container = st.empty()
            full_response = ""

            with st.spinner("Generating article..."):
                for chunk in chain.stream({"topic": topic, "articles": articles}):
                    full_response += chunk
                    output_container.markdown(full_response)

            st.success("Article generation complete!")
        else:
            st.error("Please enter a topic before generating the article.")