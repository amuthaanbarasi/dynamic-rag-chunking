import pymupdf
from pathlib import Path


def ingest_pdf(pdf_path):
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError("PDF file not found.")

    pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            page_data = {
                "page_number": page_number,
                "text": page.get_text("text"),
                "blocks": page.get_text("blocks")
            }

            pages.append(page_data)

    return pages


if __name__ == "__main__":
    pdf_path = "documents/sample.pdf"

    try:
        pages = ingest_pdf(pdf_path)

        print("PDF ingestion completed successfully!")
        print("Total pages:", len(pages))

        for page in pages:
            print(f"\nPage {page['page_number']}:")
            print(page["text"][:300])

    except (FileNotFoundError, ValueError) as error:
        print("Error:", error)