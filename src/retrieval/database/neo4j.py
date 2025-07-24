from .database import Database
from neo4j import GraphDatabase, Result
from neo4j.graph import Graph


class Neo4j(Database):
    def __init__(self, uri: str, username: str, password: str, database: str) -> None:
        self.driver: GraphDatabase = GraphDatabase.driver(
            uri, auth=(username, password)
        )
        self.database: str = database

    def query(self, query: str) -> str:
        self.driver.verify_connectivity()
        with self.driver.session(database=self.database) as session:
            result: Result = session.run(query)

            graph: Graph = result.graph()

            node_labels: dict = {}
            for node in graph.nodes:
                print("[DEBUG] graph.node", node)
                name = node.get("name") or node.get("title") or f"Node_{node.id}"
                node_labels[node.id] = name

            textual_rels: list[str] = []
            for rel in graph.relationships:
                start = node_labels[rel.start_node.id]
                end = node_labels[rel.end_node.id]
                rel_type = rel.type
                textual_rels.append(f"{start} {rel_type.lower()} {end}.")

            return "\n".join(textual_rels)

    def __del__(self) -> None:
        self.driver.close()
