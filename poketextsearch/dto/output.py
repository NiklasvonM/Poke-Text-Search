from pydantic import BaseModel


class Pokemon(BaseModel):
    pokedex_number: int
    name: str
    bulbapedia_link: str
    image_link: str
    description: str
