from argparse import ArgumentParser


class Namespace:
    vectorstore: str


namespace = Namespace()

parser = ArgumentParser()
parser.add_argument(
    "-v",
    "--vectorstore",
    default="BAAI/bge-m3",
    help=(
        "See https://huggingface.co/models?other=embeddings. "
        'For OpenAI embedding models, the name needs to start with "openai/".'
    ),
)
