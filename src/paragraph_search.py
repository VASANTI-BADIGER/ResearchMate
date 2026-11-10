
import re


def split_into_paragraphs(text):
    if not text or not text.strip():
        return []

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Normalize spaces.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove URLs.
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Remove common page headers and footers.
    text = re.sub(
        r"(?im)^.*(?:Page\s+\d+\s+of\s+\d+|"
        r"Large language models \(LLMs\): survey).*$",
        "",
        text
    )

    # Remove standalone page numbers.
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)

    # Remove reference section if present near the end.
    reference_match = re.search(
        r"(?im)^\s*(References|Bibliography|Works Cited)\s*$",
        text
    )

    if reference_match and reference_match.start() > len(text) * 0.50:
        text = text[:reference_match.start()]

    # Split text into sentences.
    sentences = re.split(r"(?<=[.!?])\s+", text)

    valid_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()

        # Skip very short fragments.
        if len(words) < 8:
            continue

        # Skip table headings and citation-heavy content.
        if re.search(
            r"Table\s+\d+|"
            r"arxiv preprint|"
            r"doi:\s*10\.|"
            r"acm digital library|"
            r"proceedings of the",
            sentence,
            re.IGNORECASE
        ):
            continue

        # Check whether the sentence contains enough readable words.
        valid_words = re.findall(r"[A-Za-z]{3,}", sentence)

        if len(valid_words) / max(len(words), 1) < 0.70:
            continue

        # Reject sentences dominated by citation years.
        years = re.findall(r"\b(?:19|20)\d{2}\b", sentence)

        if len(years) >= 2:
            continue

        # Reject incomplete sentences.
        if sentence[-1] not in ".!?":
            continue

        valid_sentences.append(sentence)

    # Group meaningful sentences into paragraphs.
    paragraphs = []
    current_sentences = []
    word_count = 0

    for sentence in valid_sentences:
        current_sentences.append(sentence)
        word_count += len(sentence.split())

        if word_count >= 100:
            paragraphs.append(" ".join(current_sentences))
            current_sentences = []
            word_count = 0

    if current_sentences and word_count >= 20:
        paragraphs.append(" ".join(current_sentences))

    return paragraphs
