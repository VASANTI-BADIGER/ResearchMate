
import streamlit as st

from src.pdf_reader import extract_text_from_pdf
from src.text_processor import clean_text
from src.summarizer import summarize_text
from src.qa_engine import answer_question


st.set_page_config(
    page_title="ResearchMate",
    page_icon="📚",
    layout="centered"
)

st.title("📚 ResearchMate")
st.subheader("AI Research Paper Assistant")

st.write(
    "Upload a research paper to generate a summary "
    "and ask questions about its contents."
)

uploaded_file = st.file_uploader(
    "Upload a research paper PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        with open("uploaded_paper.pdf", "wb") as file:
            file.write(uploaded_file.getbuffer())

        text = extract_text_from_pdf("uploaded_paper.pdf")
        text = clean_text(text)

        if not text:
            st.error("No text could be extracted from this PDF.")

        else:
            st.success("Research paper uploaded successfully!")

            st.divider()
            st.header("📝 Research Paper Summary")

            if st.button("Generate Summary"):
                with st.spinner("Generating summary..."):
                    summary = summarize_text(text)

                st.markdown("### Summary")
                st.write(summary)

            st.divider()
            st.header("💬 Ask a Question")

            question = st.text_input(
                "Enter your question about the research paper"
            )

            if st.button("Get Answer"):
                if question.strip():
                    with st.spinner("Finding an answer..."):
                        answer = answer_question(question, text)

                    st.markdown("### Answer")
                    st.write(answer)

                else:
                    st.warning("Please enter a question.")

    except Exception as error:
        st.error("Something went wrong while processing the PDF.")
        st.caption(f"Error details: {error}")
