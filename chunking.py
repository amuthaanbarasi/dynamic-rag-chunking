
from parsing import parse_pdf


def create_chunks(parsed_content, chunk_size=1000):
    chunks = []
    current_blocks = []
    current_length = 0
    current_page = None

    for block in parsed_content:
        text = block["text"]
        page = block["page"]

        if current_blocks:
            page_changed = page != current_page
            size_exceeded = current_length + len(text) > chunk_size

            if page_changed or size_exceeded:
                chunks.append({
                    "page": current_page,
                    "type": "mixed",
                    "text": "\n".join(
                        item["text"] for item in current_blocks
                    ),
                    "block_count": len(current_blocks)
                })

                current_blocks = []
                current_length = 0

        if not current_blocks:
            current_page = page

        current_blocks.append(block)
        current_length += len(text)

    if current_blocks:
        chunks.append({
            "page": current_page,
            "type": "mixed",
            "text": "\n".join(
                item["text"] for item in current_blocks
            ),
            "block_count": len(current_blocks)
        })

    return chunks


if __name__ == "__main__":
    parsed_content = parse_pdf("documents/sample.pdf")
    chunks = create_chunks(parsed_content)

    print("Improved chunking completed!")
    print("Total parsed blocks:", len(parsed_content))
    print("Total chunks:", len(chunks))

    for index, chunk in enumerate(chunks[:5], start=1):
        print(f"\nChunk {index}")
        print("Page:", chunk["page"])
        print("Blocks:", chunk["block_count"])
        print("Text:", chunk["text"][:250])