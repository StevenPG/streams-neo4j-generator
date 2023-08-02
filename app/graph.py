import py2neo
from py2neo import Graph, ConnectionUnavailable, Node


class DatabaseManager:
    """
    Management class that maintains the current state of the database
    entities such as nodes and relationships.
    """

    def __init__(self):
        self.nodes = []
        self.relationships = []

    def add_service_node(self, repository):
        self.add_node(Node(*["Service"], **{"name": repository.name}))

    def add_node(self, node):
        self.nodes.append(node)

    def add_nodes(self, nodes: list):
        for node in nodes:
            self.add_node(node)

    def add_relationship(self, relationship):
        self.relationships.append(relationship)

    def add_relationships(self, relationships: list):
        for relationship in relationships:
            self.add_relationship(relationship)

    def add_nodes_relationships(self, nodes: list, relationships: list):
        self.add_nodes(nodes)
        self.add_relationships(relationships)


def build_neo4j_db(manager: DatabaseManager):
    try:
        subgraph = py2neo.Subgraph(manager.nodes, manager.relationships)
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "admin123"))
        graph.create(subgraph)
    except ConnectionUnavailable as e:
        print(f"Unable to open connection::{e}")
