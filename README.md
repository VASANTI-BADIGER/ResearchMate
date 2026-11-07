# 📚 ResearchMate – AI Research Paper Assistant

ResearchMate is a Python-based application that helps users understand research papers easily. Users can upload a PDF research paper, generate a summary, and ask questions about its contents.

## 🚀 Features

- Upload research papers in PDF format.
- Extract text from PDF documents.
- Clean and process extracted text.
- Generate research paper summaries.
- Ask questions about uploaded research papers.
- Retrieve relevant answers using TF-IDF and cosine similarity.
- Filter irrelevant and noisy PDF content.

## 🛠️ Technologies Used

- Python
- Streamlit
- PyMuPDF
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Pytest
- Git and GitHub

## 📂 Project Structure

```text
ResearchMate/
│
├── app.py
├── requirements.txt
├── .gitignore
├── sample.pdf
│
├── src/
│   ├── pdf_reader.py
│   ├── text_processor.py
│   ├── paragraph_search.py
│   ├── summarizer.py
│   └── qa_engine.py
│
└── tests/
    ├── test_pdf_reader.py
    ├── test_qa_engine.py
    └── test_summarizer.py
```

## ⚙️ Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/VASANTI-BADIGER/ResearchMate.git
cd ResearchMate
```

**2. Create a virtual environment**

```bash
python3 -m venv .venv
```

**3. Activate the virtual environment**

```bash
source .venv/bin/activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the application**

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to use ResearchMate.

## 🧪 Run Tests

Execute the following command:

```bash
python -m pytest -v
```

## 🔍 How It Works

1. The user uploads a research paper in PDF format.
2. PyMuPDF extracts text from the document.
3. The extracted text is cleaned and divided into meaningful paragraphs.
4. TF-IDF and cosine similarity help identify relevant content.
5. The summarizer generates a concise summary.
6. The question-answering module retrieves relevant sentences from the paper.

## 🎯 Project Objective

The objective of ResearchMate is to simplify research paper reading by providing automated summarization and question-answering capabilities.

## 👩‍💻 Author

**Vasanti Badiger**

GitHub: https://github.com/VASANTI-BADIGER

---

*ResearchMate – Making research paper reading easier.*
