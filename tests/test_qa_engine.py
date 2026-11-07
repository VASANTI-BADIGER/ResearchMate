from src.pdf_reader import extract_text_from_pdf
from src.qa_engine import answer_question


def test_answer_question():
    text = extract_text_from_pdf("uploaded_paper.pdf")

    answer = answer_question(
        "How can LLMs help with drug development?",
        text
    )

    assert isinstance(answer, str)
    assert "drug development" in answer.lower()
