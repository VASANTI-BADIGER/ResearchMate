
import pymupdf
import re


def extract_text_from_pdf(pdf_path):
    extracted_pages = []

    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:

            page_width = page.rect.width

            blocks = page.get_text("blocks", sort=True)

            page_blocks = []

            for block in blocks:

                # Ignore image blocks.
                if len(block) < 7 or block[6] != 0:
                    continue

                x0, y0, x1, y1 = block[:4]
                block_text = block[4].strip()

                if not block_text:
                    continue

                # Remove repeated spaces.
                block_text = re.sub(
                    r"[ \t]+",
                    " ",
                    block_text
                )

                # Remove standalone page numbers.
                block_text = re.sub(
                    r"(?m)^\s*\d+\s*$",
                    "",
                    block_text
                )

                block_text = block_text.strip()

                if len(block_text) < 15:
                    continue

                page_blocks.append({
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "text": block_text
                })

            # Separate full-width blocks and column blocks.
            full_width = []
            left_column = []
            right_column = []

            for block in page_blocks:

                block_width = block["x1"] - block["x0"]

                if block_width > page_width * 0.60:
                    full_width.append(block)

                elif block["x0"] < page_width * 0.50:
                    left_column.append(block)

                else:
                    right_column.append(block)

            # Sort blocks vertically.
            full_width.sort(key=lambda b: b["y0"])
            left_column.sort(key=lambda b: b["y0"])
            right_column.sort(key=lambda b: b["y0"])

            ordered_blocks = (
                full_width + left_column + right_column
            )

            page_text = "\n\n".join(
                block["text"] for block in ordered_blocks
            )

            extracted_pages.append(page_text)

    return "\n\n".join(extracted_pages)
