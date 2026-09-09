import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from mydb import get_schema, run_query


load_dotenv()

st.set_page_config(page_title="DataGPT", page_icon=":bar_chart:", layout="wide")
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
        }

        h1 {
            margin-top: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("DataGPT")
st.caption("Ask a question about the orders data and get the result from SQL Server.")


@st.cache_data(show_spinner="Loading database schema...")
def load_orders_schema():
    return get_schema("orders")


with st.form("query_form"):
    question = st.text_area(
        "Ask a question",
        placeholder="For example: What are the total orders by month?",
        height=100,
    )
    submitted = st.form_submit_button("Run Query", type="primary")

if submitted:
    if not question.strip():
        st.warning("Enter a question before running the query.")
        st.stop()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEY is not set. Add it to your environment or .env file.")
        st.stop()

    try:
        schema = load_orders_schema()
        prompt = f"""
Generate a MS SQL Server SQL based on the below schema
{schema}
Question: {question}

Provide your response as SQL only.
"""

        with st.spinner("Generating SQL..."):
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model="gpt-5.6-sol",
                input=prompt,
            )

        query = response.output_text.strip()
        if not query:
            st.error("The model returned an empty SQL query.")
            st.stop()

        st.subheader("Generated SQL")
        st.code(query, language="sql")

        with st.spinner("Running query..."):
            result = run_query(query)

        st.subheader("Results")
        st.dataframe(result, use_container_width=True)
        st.caption(f"{len(result):,} rows returned")
    except Exception as error:
        st.error(f"Unable to complete the request: {error}")