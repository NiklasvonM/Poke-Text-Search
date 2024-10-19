import json
from pathlib import Path
from typing import Any

import polars as pl
from tqdm import tqdm

from poketextsearch.scraping import scrape_pokemon_data


def save_data(
    data: dict[str, Any], filename: str | Path = "data/pokemon_descriptions.jsonl"
) -> None:
    with open(filename, "a+", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    output_file = Path("data/pokemon_descriptions.jsonl")
    already_done: set[str] = set()
    output_file.touch(exist_ok=True)
    with open(output_file, encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            already_done.add(data["pokedex_number"])
    df = pl.read_csv("data/poketextsearch.csv").filter(~pl.col("Number").is_in(already_done))
    for row in tqdm(df.iter_rows(named=True)):
        pokedex_number = int(row["Number"])
        name = row["Name"]
        info = scrape_pokemon_data(name)
        save_data(info.model_dump())
