from src.pdf_reader import extract_text_from_pdf


def test_extract_text_from_pdf():
    text = extract_text_from_pdf("sample.pdf")

    assert isinstance(text, str)
    assert len(text.strip()) > 0
