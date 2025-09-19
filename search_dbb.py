import os
import json
from ddbapi import zp_pages
import re

# === Settings ===
OUTPUT_DIR = "results/1918"
KEYWORDS_FILE = "keywords.txt"
DATE_RANGE = "[1918-01-01T00:00:00Z TO 1918-11-11T23:59:59Z]" #note: begins at 1915-04-22 & ends at 1918-11-11

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(name):	#replace all characters that are invalid in filenames with underscore
	return re.sub(r'[<>:"/\\|?*]', '_', name)

def load_keywords(path):
	with open(path, "r", encoding="utf-8") as f:
		return [line.strip() for line in f if line.strip()]

def fetch_and_save(keyword):
	print(f"Searching for '{keyword}'...")
	df = zp_pages(
		publication_date=DATE_RANGE,
		plainpagefulltext=keyword
	)

	if df.empty:
		print(f"No results for '{keyword}'")
		return

	data = df.astype(str).to_dict(orient="records")

	#sanitie filename
	safe_name = sanitize_filename(keyword)
	outfile = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
	with open(outfile, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

	print(f"Saved {len(df)} results for '{keyword}' to {outfile}")



def main():
	keywords = load_keywords(KEYWORDS_FILE)
	for kw in keywords:
		fetch_and_save(kw)

if __name__ == "__main__":
	main()
