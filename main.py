
from pypdf import PdfReader
import re
from parsing import parse_pdf
from chunking import create_chunks


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n\n"

    return text


def fixed_size_chunking(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

    return chunks


def structure_aware_chunking(text, chunk_size=500):
    lines = text.splitlines()
    chunks = []
    current_chunk = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if current_chunk and len(current_chunk) + len(line) + 1 > chunk_size:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += " " + line
            else:
                current_chunk = line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def search_chunks(question, chunks):
    question_words = set(re.findall(r"[a-zA-Z]+", question.lower()))
    results = []

    for chunk in chunks:
        if isinstance(chunk, dict):
            chunk_text = chunk["text"]
        else:
            chunk_text = chunk

        chunk_words = set(re.findall(r"[a-zA-Z]+", chunk_text.lower()))
        score = len(question_words & chunk_words)

        if "average" in question.lower() or "mean" in question.lower():
            if "mean" in chunk_text.lower() or "describe" in chunk_text.lower():
                score += 5

        if score > 0:
            results.append((score, chunk_text))

    results.sort(key=lambda item: item[0], reverse=True)

    return results


pdf_path = "documents/sample.pdf"

text = extract_text(pdf_path)
parsed_content = parse_pdf(pdf_path)

fixed_chunks = fixed_size_chunking(text)
structure_chunks = structure_aware_chunking(text)
type_chunks = create_chunks(parsed_content)

print("Total characters:", len(text))
print("Fixed-size chunks:", len(fixed_chunks))
print("Structure-aware chunks:", len(structure_chunks))
print("Type-aware chunks:", len(type_chunks))


tests = [
    {
        "question": "What are the pressure columns and their average values?",
        "expected": [
            "Heel_Pressure_kPa",
            "Midfoot_Pressure_kPa",
            "Toe_Pressure_kPa",
            "147.034",
            "150.319",
            "26.634"
        ]
    },
    {
        "question": "What is the pressure feature distribution?",
        "expected": [
            "Pressure Feature Distribution"
        ]
    },
    {
        "question": "Which features are used to predict gait type?",
        "expected": [
            "Gait_Type",
            "Heel_Ratio",
            "Midfoot_Ratio",
            "Toe_Ratio"
        ]
    }
]


methods = [
    ("Fixed-size", fixed_chunks),
    ("Structure-aware", structure_chunks),
    ("Type-aware", type_chunks)
]


for test in tests:
    print("\nQuestion:", test["question"])

    for method_name, chunks in methods:
        results = search_chunks(test["question"], chunks)

        print(f"\n{method_name}:")

        if not results:
            print("No matching chunks found.")
            continue

        top_results = results[:3]

        combined_text = "\n".join(
            result_text for score, result_text in top_results
        )

        combined_text = re.sub(
            r"\s+", " ", combined_text
        ).lower()

        missing = [
            item for item in test["expected"]
            if re.sub(r"\s+", " ", item).lower() not in combined_text
        ]

        found_count = len(test["expected"]) - len(missing)

        print("Chunks retrieved:", len(top_results))
        print(
            "Expected items found:",
            found_count,
            "out of",
            len(test["expected"])
        )

        if missing:
            print("Missing items:", missing)
        else:
            print("All expected items found.")

        for rank, (score, result_text) in enumerate(
            top_results, start=1
        ):
            print(f"\nRank {rank} | Score: {score}")
            print(result_text[:250])

    print("=" * 60)