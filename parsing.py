
import pymupdf
import re


def classify_block(text, font_size, is_bold):
    stripped_text = text.strip()
    lower_text = stripped_text.lower()

    code_patterns = [
        r"\bimport\b",
        r"\bfrom\b.+\bimport\b",
        r"\bdef\s+\w+",
        r"\bclass\s+\w+",
        r"\breturn\b",
        r"\bprint\s*\(",
        r"\bif\b.*:",
        r"\bfor\b.*\bin\b.*:",
        r"\bwhile\b.*:",
        r"\bplt\.",
        r"\bsns\.",
        r"\bpd\.",
        r"\bdf\s*[\.\[]",
        r"\bnp\."
    ]

    for pattern in code_patterns:
        if re.search(pattern, stripped_text):
            return "code"

    if (
        re.search(r"\b(count|mean|std|min|max|median)\b", lower_text)
        and re.search(r"\d", stripped_text)
    ):
        return "table_like"

    if len(stripped_text) < 100 and (
        is_bold or font_size >= 14
    ):
        return "heading"

    return "paragraph"


def parse_pdf(pdf_path):
    parsed_content = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "lines" not in block:
                    continue

                text_parts = []
                font_sizes = []
                bold_found = False

                for line in block["lines"]:
                    for span in line["spans"]:
                        text_parts.append(span["text"])
                        font_sizes.append(span["size"])

                        if "bold" in span["font"].lower():
                            bold_found = True

                text = " ".join(text_parts).strip()

                if not text:
                    continue

                average_font_size = (
                    sum(font_sizes) / len(font_sizes)
                    if font_sizes else 0
                )

                content_type = classify_block(
                    text,
                    average_font_size,
                    bold_found
                )

                parsed_content.append({
                    "page": page_number,
                    "type": content_type,
                    "text": text,
                    "x0": block["bbox"][0],
                    "y0": block["bbox"][1],
                    "x1": block["bbox"][2],
                    "y1": block["bbox"][3]
                })

    return parsed_content


if __name__ == "__main__":
    content = parse_pdf("documents/sample.pdf")

    print("Parsing completed!")
    print("Total blocks:", len(content))

    type_counts = {}

    for item in content:
        content_type = item["type"]
        type_counts[content_type] = (
            type_counts.get(content_type, 0) + 1
        )

    print("\nContent type counts:")

    for content_type, count in type_counts.items():
        print(f"{content_type}: {count}")

    for item in content[:10]:
        print(f"\nPage: {item['page']}")
        print(f"Type: {item['type']}")
        print(f"Text: {item['text'][:200]}")