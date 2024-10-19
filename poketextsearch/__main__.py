import os

from dotenv import load_dotenv
from fastapi import FastAPI, status

from poketextsearch.argparser import namespace, parser
from poketextsearch.dto import InputData, Pokemon
from poketextsearch.vectorstore import get_vectorstore

load_dotenv()

parser.parse_args(namespace=namespace)

app = FastAPI()
vectorstore = get_vectorstore(model_name=namespace.vectorstore)


@app.get("/health", status_code=status.HTTP_200_OK)
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/search_pokemon", status_code=status.HTTP_200_OK)
async def search_pokemon(input_data: InputData) -> list[Pokemon]:
    """
    Finds the Pokémons that best match the given description.
    """
    similar_pokemon = vectorstore.similarity_search(input_data.text, k=input_data.number_pokemon)
    result = [Pokemon(**doc.metadata) for doc in similar_pokemon]
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=os.getenv("FASTAPI_HOST", "127.0.0.1"), port=8000)
