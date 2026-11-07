
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.paragraph_search import split_into_paragraphs


def clean_answer_sentence(sentence):
    sentence = re.sub(r"\s+", " ", sentence).strip()

    # Remove incomplete citation fragments at the beginning.
    sentence = re.sub(
        r"^(?:\(?\d{4}\)?[,.;:]?\s*)+",
        "",
        sentence
    )

    # Reject sentences beginning with obvious PDF extraction noise.
    if re.match(
        r"^(?:ai use AI|use AI to help|"
        r"\d{4}\s*\)|Table\s+\d+)",
        sentence,
        re.IGNORECASE
    ):
        return ""

    return sentence.strip()


def answer_question(question, text):
    if not question.strip():
        return "Please enter a question."

    if not text.strip():
        return "No text is available to answer this question."

    chunks = split_into_paragraphs(text)

    if not chunks:
        return "No readable text chunks were found in the paper."

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        chunk_vectors = vectorizer.fit_transform(
            [question] + chunks
        )

        chunk_scores = cosine_similarity(
            chunk_vectors[0:1],
            chunk_vectors[1:]
        )[0]

        best_index = chunk_scores.argmax()

        if chunk_scores[best_index] < 0.05:
            return "I could not find a relevant answer in the paper."

        best_chunk = chunks[best_index]

        sentences = re.split(
            r"(?<=[.!?])\s+",
            best_chunk
        )

        sentences = [
            clean_answer_sentence(sentence)
            for sentence in sentences
        ]

        sentences = [
            sentence for sentence in sentences
            if len(sentence.split()) >= 8
        ]

        if not sentences:
            return "No meaningful answer was found."

        sentence_vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        sentence_vectors = sentence_vectorizer.fit_transform(
            [question] + sentences
        )

        sentence_scores = cosine_similarity(
            sentence_vectors[0:1],
            sentence_vectors[1:]
        )[0]

        threshold = max(
            0.05,
            sentence_scores.max() * 0.40
        )

        selected = [
            i for i, score in enumerate(sentence_scores)
            if score >= threshold
        ]

        if not selected:
            return "I could not find a relevant answer in the paper."

        selected.sort(
            key=lambda i: sentence_scores[i],
            reverse=True
        )

        selected = selected[:3]

        answer = " ".join(
            sentences[i] for i in selected
        )

        return re.sub(r"\s+", " ", answer).strip()

    except ValueError:
        return "I could not find enough meaningful text to answer."

