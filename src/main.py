from retrieval import Graph
from retrieval.database import Neo4j, Database
from retrieval.llm import LLM, Ollama, Message
from util import read_to_string, unwrap, user_prompt

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
    llm: LLM = Ollama(
        host=unwrap(os.getenv("OLLAMA_URI")),
        model="mistral:7b",
        chat=[
            Message(
                role="system", content=read_to_string("./resources/prompt/system.md")
            )
        ],
        cleaner=lambda s: s[5:-4],  # Simple trimming of response content
    )

    # Create a graph-based retriever using the LLM and database
    retrieval: LLM = Graph(llm, database)

    # Load the user prompt template from a file
    base = read_to_string("./resources/prompt/user.md")

    # Send the user query to the retriever:
    # - The LLM generates a Cypher query from the user's message
    # - The Graph retriever executes that query on the Neo4j database
    # - The result is returned as text
    result = retrieval.chat(
        chat=[
            Message(
                role="user",
                content=user_prompt(
                    base,
                    intent="Information request",
                    request="What are the symptoms of asthma?",
                ),
            )
        ]
    )

    print("Result:", result)


if __name__ == "__main__":
    main()
