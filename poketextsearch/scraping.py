import re

import requests
from bs4 import BeautifulSoup

from poketextsearch.dto import Pokemon


def scrape_pokemon_data(pokemon_name: str) -> Pokemon:
    """Fetches and extracts Pokémon data from Bulbapedia."""
    url = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name}_(Pokémon)"
    html_content = fetch_html_content(url)
    soup = BeautifulSoup(html_content, "html.parser")

    pokedex_number = extract_pokedex_number(html_content, pokemon_name)
    description = extract_description(soup)
    image_link = extract_image_link(soup)

    return Pokemon(
        pokedex_number=pokedex_number,
        name=pokemon_name,
        description=description,
        bulbapedia_link=url,
        image_link=image_link,
    )


def fetch_html_content(url: str) -> str:
    """Fetches the HTML content of a given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def extract_pokedex_number(html: str, name: str) -> int:
    """Extracts the Pokédex number from the HTML content using regex."""
    cleaned_name = clean_string_for_url(name)
    pattern = rf"/(\d{{4}}){cleaned_name}"
    match = re.search(pattern, html)
    assert match is not None, "Pokédex number not found in the HTML."
    return int(match.group(1))


def clean_string_for_url(s: str) -> str:
    """Cleans a string to make it suitable for use in a URL.

    Args:
      s: The string to clean.

    Returns:
      A cleaned string suitable for use in a URL.
    """
    s = s.replace("'", "%27")  # Farfetch'd
    s = s.replace(" ", "_")  # Mime Jr.
    s = s.replace("♀", "")  # Nidoran♀
    s = s.replace("♂", "")  # Nidoran♂
    s = s.replace("é", "%C3%A9")  # Flabébé
    s = s.replace(":", "")  # Type:_Null
    s = s.removesuffix(".")  # Mime Jr.
    return s


def extract_description(soup: BeautifulSoup) -> str:
    """Extracts the Pokémon description from the BeautifulSoup object."""
    description_div = soup.find("div", class_="mw-parser-output")

    paragraphs: list[str] = []
    capture_biology = False
    for element in description_div.children:
        if element.name == "h2" and element.text == "Biology":
            capture_biology = True
        elif capture_biology and element.name == "p":
            paragraphs.append(element.text.strip())
        elif capture_biology and element.name == "h2":
            capture_biology = False
            break
        elif not capture_biology and element.name == "p":
            paragraphs.append(element.text.strip())
        elif not capture_biology and element.name == "h2":
            break

    data = "\n".join(paragraphs)
    return clean_string(data)


def extract_image_link(soup: BeautifulSoup) -> str:
    """Extracts the Pokémon image link from the BeautifulSoup object."""
    image_element = soup.find("a", class_="image")
    assert image_element is not None, "No image found!"
    image_element = image_element.find("img")
    assert image_element is not None, "No image found!"
    return image_element["src"]


def clean_string(data: str) -> str:
    junk_strings = [
        "(For specifics on this Pokémon's Evolution in the games, refer to Game data→Evolution "
        "data.)",
    ]

    for string in junk_strings:
        data = data.replace(string, "")
    return data.strip()
