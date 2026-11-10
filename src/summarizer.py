import re


def summarize_text(text, num_sentences=3):

    if not text or not text.strip():
        return "No text available to summarize."

    text = re.sub(r"\s+", " ", text).strip()

    abstract_match = re.search(
        r"Large Language Models \(LLMs\) have recently",
        text,
        re.IGNORECASE
    )

    if not abstract_match:
        return "Could not identify the abstract in this PDF."

    abstract_text = text[abstract_match.start():]

    keyword_match = re.search(
        r"\bKeywords\s*:",
        abstract_text,
        re.IGNORECASE
    )

    if keyword_match:
        abstract_text = abstract_text[:keyword_match.start()]

    sentences = re.split(
        r"(?<=[.!?])\s+",
        abstract_text
    )

    valid_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence.split()) >= 8:
            valid_sentences.append(sentence)

    if not valid_sentences:
        return "Not enough meaningful text to summarize."

    return " ".join(valid_sentences[:num_sentences])
