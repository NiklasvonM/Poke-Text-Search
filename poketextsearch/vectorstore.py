import json
import os
from pathlib import Path
from typing import Any

from langchain.schema import Document
from langchain_community.vectorstores import FAISS, VectorStore
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

from poketextsearch.dto import Pokemon


def read_descriptions(filename: str | Path) -> list[dict[str, Any]]:
    with open(filename, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def create_vectorstore(model_name: str, persist_directory: str | Path) -> VectorStore:
    print(f"Creating new vectorstore using model {model_name}. This may take a while...")
    pokemon_metadata = read_descriptions("data/pokemon_descriptions.jsonl")
    documents: list[Document] = []
    for metadata in pokemon_metadata:
        _ = Pokemon(**metadata)  # validate the metadata
        documents.append(
            Document(
                page_content=metadata["description"],
                metadata=metadata,
            )
        )
    embeddings = get_embeddings(model_name)
    vectorstore = FAISS.from_documents(documents, embeddings)
    print(f"Saving vectorstore to {persist_directory}")
    Path(persist_directory).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(persist_directory))
    return vectorstore


def get_model_name(model_name: str) -> tuple[bool, str]:
    model_name_cleaned = model_name.removeprefix("openai/")
    is_openai_model = model_name_cleaned != model_name
    return is_openai_model, model_name_cleaned


def get_embeddings(model_name: str) -> Embeddings:
    is_openai, model_name = get_model_name(model_name)
    embeddings: Embeddings
    if is_openai:
        api_key_env_name = "OPENAI_API_KEY"
        api_key = os.getenv(api_key_env_name)
        if not api_key:
            raise AssertionError(
                "It seems you're trying to use OpenAI embeddings. "
                f"You need to set the {api_key_env_name} environment variable!"
            )
        embeddings = OpenAIEmbeddings(model=model_name, api_key=SecretStr(api_key))
    else:
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings


def load_vectorstore(model_name: str, persist_directory: str | Path) -> VectorStore:
    print(f"Loading vectorstore from {persist_directory}")
    embeddings = get_embeddings(model_name)
    vectorstore = FAISS.load_local(
        str(persist_directory), embeddings=embeddings, allow_dangerous_deserialization=True
    )
    return vectorstore


def get_vectorstore(model_name: str = "BAAI/bge-m3") -> VectorStore:
    persist_directory = Path("data/pokemon_faiss") / model_name
    vectorstore = (
        load_vectorstore(model_name, persist_directory)
        if persist_directory.exists()
        else create_vectorstore(model_name, persist_directory)
    )
    return vectorstore
