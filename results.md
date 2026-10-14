# Dynamic RAG Chunking Comparison

## Project Objective

To extract PDF content, identify document structure, create chunks using different methods, and compare their retrieval behavior.

## Dataset

* Document: Smart Shoe Gait Analysis report
* Extracted characters: 20,005
* Parsed blocks: 275

## Chunking Methods

| Method                       | Number of chunks |
| ---------------------------- | ---------------: |
| Fixed-size chunking          |               40 |
| Structure-aware chunking     |               36 |
| Improved page-aware chunking |               28 |

## Retrieval Evaluation

Three questions were used to compare the retrieved content:

1. What are the pressure columns and their average values?
2. What is the pressure feature distribution?
3. Which features are used to predict gait type?

Fixed-size and structure-aware chunking retrieved useful information, while improved page-aware chunking also retrieved the expected pressure statistics and gait prediction features.

## Current Limitations

* Retrieval uses keyword overlap rather than semantic similarity.
* Evaluation uses a small set of questions.
* Exact-text matching can incorrectly mark a result as missing when spacing differs.
* PDF block classification uses heuristic rules.

## Conclusion

The project successfully demonstrates PDF extraction, heuristic parsing, multiple chunking strategies, and keyword-based retrieval comparison. Further work can include improved evaluation, semantic embeddings, vector search, and answer generation with an LLM.
