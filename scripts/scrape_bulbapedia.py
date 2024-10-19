from poketextsearch.scraping import scrape_pokemon_data

POKEMON_NAME: str = "Scizor"


if __name__ == "__main__":
    pokemon_info = scrape_pokemon_data(POKEMON_NAME)
    print(pokemon_info.model_dump_json(indent=2))
