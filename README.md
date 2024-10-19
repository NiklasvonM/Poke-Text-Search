# Poké Text Search

Search for Pokémons using text.

This is done by comparing the embeddings of the given query to the descriptions scraped from [Bulbapedia](https://bulbapedia.bulbagarden.net/).

## Getting Started

- Install Poetry.
- Run `poetry install`.
- Optionally update the Pokémon metadata by scraping Bulbapedia via scripts/bulk_scrape_bulbapedia.py.
- Run the application via `poetry run python -m poketextsearch`. You may optionally supply an embedding model name, e.g., `poetry run python -m poketextsearch --vectorstore openai/text-embedding-3-small`, see `poetry run python -m poketextsearch --help`.
- Run `curl -X POST http://127.0.0.1:8000/search_pokemon -H 'Content-Type: application/json' -d '{"text": "Ash Ketchums yellow mouse", "number_pokemon": 1}'`.

```bash
[
    {
        "pokedex_number": 25,
        "name": "Pikachu",
        "bulbapedia_link": "https://bulbapedia.bulbagarden.net/wiki/Pikachu_(Pokémon)",
        "image_link": "https://archives.bulbagarden.net/media/upload/thumb/4/4a/0025Pikachu.png/250px-0025Pikachu.png",
        "description": "Pikachu (Japanese: ピカチュウ Pikachu) is an Electric-type Pokémon introduced in Generation I. [...]"
    }
]
```
