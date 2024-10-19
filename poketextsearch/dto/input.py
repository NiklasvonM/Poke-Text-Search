from pydantic import BaseModel, Field


class InputData(BaseModel):
    text: str = Field(..., description="Query to compare to Pokémons' descriptions.")
    number_pokemon: int = Field(10, le=100, description="Number of Pokémon to fetch.")
