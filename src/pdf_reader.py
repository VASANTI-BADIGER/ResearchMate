
import pymupdf
import re


def extract_text_from_pdf(pdf_path):
    extracted_pages = []

    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            page_text = page.get_text("text", sort=True)

            # Join words split by a hyphen at a line break
            page_text = re.sub(
                r"([A-Za-z]{2,})-\s*\n\s*([a-z]{2,})",
                r"\1\2",
                page_text
            )

            # Replace repeated spaces and tabs
            page_text = re.sub(r"[ \t]+", " ", page_text)

            # Remove page-number-only lines
            lines = page_text.splitlines()
            cleaned_lines = []

            for line in lines:
                line = line.strip()

                if not line:
                    continue

                if re.fullmatch(r"\d+", line):
                    continue

                cleaned_lines.append(line)

            extracted_pages.append("\n".join(cleaned_lines))

    return "\n".join(extracted_pages)
