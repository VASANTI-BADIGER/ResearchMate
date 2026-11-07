from src.pdf_reader import extract_text_from_pdf
from src.summarizer import summarize_text


def test_summarize_text():
    text = extract_text_from_pdf("uploaded_paper.pdf")

    summary = summarize_text(text)

    assert isinstance(summary, str)
    assert len(summary.strip()) > 0
