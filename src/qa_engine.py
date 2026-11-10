
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


CHALLENGE_KEYWORDS = [
    "hallucination",
    "factually accurate",
    "contradicts information",
    "limited knowledge",
    "obsolete information",
    "outdated data",
    "retraining",
    "prompt engineering",
    "prompt variations",
    "safety",
    "controllability",
    "harmful content",
    "misleading content",
    "security",
    "privacy",
    "personal information",
    "computational cost",
    "hardware capacity",
    "ethical challenges"
]


def prepare_sentences(text):
    # Join words split across PDF lines.
    text = re.sub(
        r"([A-Za-z]{2,})-\s*\n\s*([a-z]{2,})",
        r"\1\2",
        text
    )

    text = re.sub(r"\s+", " ", text)

    # Remove references section.
    match = re.search(
        r"\bReferences\b",
        text,
        re.IGNORECASE
    )

    if match and match.start() > len(text) * 0.50:
        text = text[:match.start()]

    sentences = re.split(r"(?<=[.!?])\s+", text)

    cleaned = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence.split()) < 8:
            continue

        if re.search(
            r"Email addresses:|Figure\s+\d+:|"
            r"Equal contribution|arxiv preprint|"
            r"doi:|proceedings of the",
            sentence,
            re.IGNORECASE
        ):
            continue

        cleaned.append(sentence)

    return cleaned


def answer_question(question, text):

    if not question.strip():
        return "Please enter a question."

    if not text.strip():
        return "No text is available."

    sentences = prepare_sentences(text)

    if not sentences:
        return "No meaningful text was found."

    expanded_question = question

    # Expand limitation and challenge questions.
    if re.search(
        r"limitation|challenge|problem|drawback|weakness",
        question,
        re.IGNORECASE
    ):
        expanded_question += " " + " ".join(CHALLENGE_KEYWORDS)

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        vectors = vectorizer.fit_transform(
            [expanded_question] + sentences
        )

        scores = cosine_similarity(
            vectors[0:1],
            vectors[1:]
        )[0]

        # Give relevant challenge sentences an additional score.
        for index, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()

            keyword_matches = sum(
                1 for keyword in CHALLENGE_KEYWORDS
                if keyword in sentence_lower
            )

            if keyword_matches:
                scores[index] += keyword_matches * 0.08

        best_indices = scores.argsort()[::-1]

        selected = []

        for index in best_indices:
            if scores[index] < 0.04:
                continue

            sentence = sentences[index]

            if sentence not in selected:
                selected.append(sentence)

            if len(selected) == 4:
                break

        if not selected:
            return "I could not find a relevant answer in the paper."

        # Preserve the original paper order.
        selected.sort(
            key=lambda sentence: sentences.index(sentence)
        )

        return " ".join(selected)

    except ValueError:
        return "Not enough meaningful text was found to answer."
