import py2neo
from py2neo import Graph, ConnectionUnavailable, Node

from app.repository import RepositoryConfiguration


class DatabaseManager:
    """
    Management class that maintains the current state of the database
    entities such as nodes and relationships.
    """

    def __init__(self):
        self.nodes = []
        self.relationships = []

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

    def add_or_get_node(self, node_type: str, repository: RepositoryConfiguration):
        for node in self.nodes:
            # If we never find the node-name match, we add and return a new node
            if repository.name == node['name']:
                return node
        created_node = Node(*[node_type], **{"name": repository.name})
        self.add_node(created_node)
        return created_node

    def add_or_get_topic_node(self, node_type: str, destination: str):
        for node in self.nodes:
            # If we never find the node-name match, we add and return a new node
            if destination == node['name']:
                return node
        created_node = Node(*[node_type], **{"name": destination})
        self.add_node(created_node)
        return created_node


def build_neo4j_db(manager: DatabaseManager):
    try:
        subgraph = py2neo.Subgraph(manager.nodes, manager.relationships)
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "admin123"))
        graph.create(subgraph)
    except ConnectionUnavailable as e:
        print(f"Unable to open connection::{e}")
