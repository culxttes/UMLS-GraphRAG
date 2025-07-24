from retrieval import Graph
from retrieval.database import Neo4j, Database
from retrieval.llm import LLM, Ollama, Message
from util import read_to_string, unwrap, user_prompt

from dotenv import load_dotenv
import os

load_dotenv()

database: Database = Neo4j(
    uri=unwrap(os.getenv("NEO4J_URI")),
    username=unwrap(os.getenv("NEO4J_USERNAME")),
    password=unwrap(os.getenv("NEO4J_PASSWORD")),
    database=unwrap(os.getenv("NEO4J_DATABASE")),
)

llm: LLM = Ollama(
    host=unwrap(os.getenv("OLLAMA_URI")),
    model="mistral:7b",
    chat=[
        Message(role="system", content=read_to_string("./resources/prompt/system.txt"))
    ],
    cleaner=lambda s: s[5:-4],
)

retrieval: LLM = Graph(llm, database)

base = read_to_string("./resources/prompt/user.txt")

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
