from graphygie.retrieval import Graph
from graphygie.retrieval.database import Neo4j, Database
from graphygie.llm import LLM, Ollama, Message
from graphygie.generation import BasicGenerator
from util import (
    read_to_string,
    unwrap,
    strip_code_fences,
    user_prompt,
    generator_system_prompt,
)

from dotenv import load_dotenv
import os


def main() -> None:
    load_dotenv()

    # Initialize the Neo4j database with credentials and connection URI from environment variables
    database: Database = Neo4j(
        uri=unwrap(os.getenv("NEO4J_URI")),
        username=unwrap(os.getenv("NEO4J_USERNAME")),
        password=unwrap(os.getenv("NEO4J_PASSWORD")),
        database=unwrap(os.getenv("NEO4J_DATABASE")),
    )

    # Initialize the Ollama language model
    # - Connects to Ollama API using the host from environment variables
    # - Uses the "mistral:7b" model
    # - Starts with a system prompt loaded from a file
    # - Applies a custom cleaner function to trim the model's response
    retrieval_llm: LLM = Ollama(
        host=unwrap(os.getenv("OLLAMA_URI")),
        model="mistral:7b",
        chat=[
            Message(
                role="system",
                content=read_to_string("./resources/prompt/retrieval_system.md"),
            )
        ],
        cleaner=strip_code_fences,
    )

    # Create a graph-based retriever using the LLM and database
    retrieval: LLM = Graph(llm=retrieval_llm, database=database)

    # Initialize the Ollama language model
    # - Connects to Ollama API using the host from environment variables
    # - Uses the "mistral:7b" model
    generator_llm: LLM = Ollama(
        host=unwrap(os.getenv("OLLAMA_URI")),
        model="mistral:7b",
    )

    # Load the user prompt template from a file
    base = read_to_string("./resources/prompt/user.md")

    generator: LLM = BasicGenerator(
        retriever=retrieval,
        generator=generator_llm,
        chat=[
            Message(
                role="system",
                content=read_to_string("./resources/prompt/generator_system.md"),
            )
        ],
        maker=generator_system_prompt,
    )

    result = generator.chat(
        chat=[
            Message(
                role="user",
                content=user_prompt(
                    base,
                    intent="Information request",
                    request="What are the main cognitive and behavioral changes associated with Frontal Lobe Syndrome?",
                ),
            )
        ]
    )

    print("Result:\n", result)


if __name__ == "__main__":
    main()
