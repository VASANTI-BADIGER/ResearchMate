from src.pdf_reader import extract_text_from_pdf
from src.qa_engine import answer_question


def test_answer_question():
    text = extract_text_from_pdf("uploaded_paper.pdf")

    answer = answer_question(
        "What is prompt engineering in LLMs?",
        text
    )

    assert isinstance(answer, str)
    assert "prompt engineering" in answer.lower()
    assert "natural language queries" in answer.lower()
