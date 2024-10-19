import json
from pathlib import Path

from poketextsearch.scraping import clean_string
from poketextsearch.vectorstore import read_descriptions


def main() -> None:
    descriptions_path = Path("data/pokemon_descriptions.jsonl")
    descriptions = read_descriptions(descriptions_path)
    for description in descriptions:
        description["description"] = clean_string(description["description"])
    with open(descriptions_path, "w", encoding="utf-8") as f:
        for description in descriptions:
            f.write(json.dumps(description) + "\n")
