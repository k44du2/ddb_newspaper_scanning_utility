import os
import json
import re
from rapidfuzz import fuzz, process

# === Settings ===
INPUT_DIR = "results/1915"	#enter the desired year here (optional, otherwise everything will end up in the same directory)
OUTPUT_DIR = "snippets/1915"
BEFORE = 10	#words prior
AFTER = 20	#words after
SIMILARITY_THRESHOLD = 90   #similarity between snippets
WORD_SIMILARITY_THRESHOLD = 90  #similarity between keywords and keywords in OCR

os.makedirs(OUTPUT_DIR, exist_ok=True)

def tokenize(text):
	return re.findall(r"\w+", text)

def is_word_match(word, keyword, threshold=80):	#checks whether the file name is close enough to the OCR
	return fuzz.ratio(word.lower(), keyword.lower()) >= threshold	#sideeffect: eliminates texts with terrible OCR -> better collocation results, but poorer accuracy of analysis results -> compromise

def extract_snippets(text, keyword, before=10, after=20):
	words = tokenize(text)
	snippets = []
	seen_positions = set()

	for i, w in enumerate(words):
		if is_word_match(w, keyword, WORD_SIMILARITY_THRESHOLD):	#avoid duplicate snippets from close matches
			if any(abs(i - pos) < after for pos in seen_positions):
				continue
			start = max(0, i - before)
			end = min(len(words), i + after + 1)
			snippet = " ".join(words[start:end])
			snippets.append(snippet.strip())
			seen_positions.add(i)
	return snippets

def deduplicate(snippets, threshold=90):	#if several snippets are 90% identical, only one will be inserted. yes, this is a magic number
	unique = []
	for snip in snippets:
		if not any(fuzz.ratio(snip.lower(), u.lower()) >= threshold for u in unique):
			unique.append(snip)
	return unique

def process_file(filepath):
	keyword = os.path.splitext(os.path.basename(filepath))[0]
	outfile = os.path.join(OUTPUT_DIR, f"{keyword}_snippets.txt")

	with open(filepath, "r", encoding="utf-8") as f:
		data = json.load(f)

	all_snippets = []
	for record in data:
		fulltext = record.get("plainpagefulltext", "")
		if fulltext:
			all_snippets.extend(extract_snippets(fulltext, keyword, BEFORE, AFTER))

	unique_snippets = deduplicate(all_snippets, SIMILARITY_THRESHOLD)

	with open(outfile, "w", encoding="utf-8") as out:
		for snip in unique_snippets:
			out.write(snip + "\n\n")

	print(f"Saved {len(unique_snippets)} unique snippets for '{keyword}' to {outfile}")

def main():
	for filename in os.listdir(INPUT_DIR):
		if filename.endswith(".json"):
			process_file(os.path.join(INPUT_DIR, filename))

if __name__ == "__main__":
	main()
