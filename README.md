# DDB Newspaper Keyword Search & Snippet Extraction

This project provides Python scripts for searching the **Deutsche Digitale Bibliothek (DDB)** newspaper archive using the [`ddbapi`](https://pypi.org/project/ddbapi/) library.  
It allows you to:

- Search OCR fulltexts of digitized newspapers for keywords.
- Collect and save results as `.json` files.
- Extract contextual text snippets (10 words before, 20 words after) where keywords appear.
- Handle OCR errors (fuzzy matching).
- Deduplicate nearly identical snippets.
- Process multiple keywords at once from a `keywords.txt` file.

---

## Features

1. **Keyword Search**
   - Reads keywords from a text file (`keywords.txt`).
   - Queries the DDB API for each keyword in a given timeframe.
   - Saves results as JSON files in the `results/` directory.

2. **Snippet Extraction**
   - Extracts occurrences of each keyword from `plainpagefulltext`.
   - Captures context: 10 words before, 20 words after the match.
   - Uses fuzzy matching to account for OCR errors (e.g., `Gas-Waſſe` vs. `Gas-Waffe`).
   - Deduplicates similar snippets.
   - Outputs snippets to the `snippets/` directory.

---

## Requirements

- Python 3.8+
- Dependencies:
  ```bash
  pip install ddbapi rapidfuzz
