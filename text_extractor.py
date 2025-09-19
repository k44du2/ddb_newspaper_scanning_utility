import os
import json

INPUT_DIR = "results/1916"       #folder with your JSON files
OUTPUT_FILE = "results/1916/all_fulltext.txt"	#destination folder for full results

all_texts = []

for filename in os.listdir(INPUT_DIR):
	if filename.endswith(".json"):
		filepath = os.path.join(INPUT_DIR, filename)
		with open(filepath, "r", encoding="utf-8") as f:
			data = json.load(f)		#each JSON file contains a list of records
			for record in data:
				fulltext = record.get("plainpagefulltext")
				if fulltext:
					all_texts.append(fulltext.strip())

# Combine everything into one big file
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
	for text in all_texts:
		out.write(text + "\n\n")  #separate pages by blank line

print(f"Saved {len(all_texts)} pages of text into {OUTPUT_FILE}")
