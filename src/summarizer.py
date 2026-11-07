import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def summarize_text(text, num_sentences=3):
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Prefer the abstract when it is available
    abstract_match = re.search(
        r"\bAbstract\b(.*?)(?=\bKeywords\b|\bKey words\b)",
        text,
        re.IGNORECASE
    )

    if abstract_match:
        text = abstract_match.group(1).strip()

    # Split text into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    cleaned_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()

        if len(words) < 6:
            continue

        if re.search(
            r"\b(et al\.|arXiv preprint|doi:|references|bibliography)\b",
            sentence,
            re.IGNORECASE
        ):
            continue

        cleaned_sentences.append(sentence)

    if not cleaned_sentences:
        return "Not enough meaningful text was found to summarize."

    if len(cleaned_sentences) <= num_sentences:
        return " ".join(cleaned_sentences)

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(cleaned_sentences)

        similarity_matrix = cosine_similarity(vectors)
        scores = similarity_matrix.sum(axis=1)

        ranked = sorted(
            range(len(cleaned_sentences)),
            key=lambda i: scores[i],
            reverse=True
        )

        selected = sorted(ranked[:num_sentences])

        return " ".join(cleaned_sentences[i] for i in selected)

    except ValueError:
        return "The paper does not contain enough meaningful text to summarize."
