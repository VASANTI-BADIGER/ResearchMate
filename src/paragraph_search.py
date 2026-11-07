
import re


def split_into_paragraphs(text):
    if not text or not text.strip():
        return []

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)

    sentences = re.split(r"(?<=[.!?])\s+", text)

    paragraphs = []
    current_sentences = []
    word_count = 0

    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()
        count = len(words)

        if count < 3:
            continue

        # Skip obvious PDF page headers and footers.
        if re.search(
            r"Page\s+\d+\s+of\s+\d+|"
            r"Large language models \(LLMs\): survey|"
            r"^\d+\s+P\.\s*Kumar",
            sentence,
            re.IGNORECASE
        ):
            continue

        # Skip obvious table headings.
        if re.search(
            r"Table\s+\d+|"
            r"\b(Architecture|Methodology|Dataset|Metric|"
            r"Findings|Domain)\b",
            sentence,
            re.IGNORECASE
        ):
            continue

        # Reject badly scrambled text.
        valid_words = re.findall(r"[A-Za-z]{3,}", sentence)

        if len(valid_words) / max(count, 1) < 0.70:
            continue

        current_sentences.append(sentence)
        word_count += count

        if word_count >= 100:
            paragraphs.append(" ".join(current_sentences))
            current_sentences = []
            word_count = 0

    if current_sentences and word_count >= 20:
        paragraphs.append(" ".join(current_sentences))

    return paragraphs

