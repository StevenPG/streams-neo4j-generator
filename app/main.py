from py2neo import Node

from app.components import BindingsManager
from app.graph import build_neo4j_db, DatabaseManager
from ini_config import scan_configuration
from repository import RepositoryManager
from scan import parse_yaml, search_files, get_bindings

if __name__ == '__main__':
    configuration = scan_configuration()

    repo_manager = RepositoryManager()
    database_manager = DatabaseManager()
    bindings_manager = BindingsManager()

    # TODO - duplicates might be getting parsed out now

    for repository in configuration.repositories:
        repo_manager.clone_repository(repository)

        # Generate our primary database node objects
        repository_node = Node(*["Service"], **{"name": repository.name})
        database_manager.add_node(repository_node)

        found_files = search_files(repository)
        print(f'Found {len(found_files)} in ${repository.git_url}')
        for found_file in found_files:
            parsed_files = parse_yaml(found_file)
            cloud_stream_bindings, kafka_stream_bindings = get_bindings(parsed_files)

            found_valid_url_bindings = False
            if (repository.binding_urls is not None and len(repository.binding_urls) != 0
                    and len(repository.binding_urls[0]) != 0):
                try:
                    remote_nodes, remote_ships = bindings_manager.process_http_bindings(repository.binding_urls,
                                                                                        repository_node)
                    database_manager.add_nodes_relationships(remote_nodes, remote_ships)
                    found_valid_url_bindings = True
                except Exception as e:
                    print(f"Issue occurred when processing remote stream-bindings::{e}")

            if not repository.prefer_url or not found_valid_url_bindings:
                try:
                    cs_nodes, cs_ships = bindings_manager.process_bindings(cloud_stream_bindings, repository_node)
                    database_manager.add_nodes_relationships(cs_nodes, cs_ships)
                except Exception as e:
                    print(f"Issue occurred when processing cloud-stream-bindings::{e}")

                try:
                    ks_nodes, ks_ships = bindings_manager.process_bindings(kafka_stream_bindings, repository_node)
                    database_manager.add_nodes_relationships(ks_nodes, ks_ships)
                except Exception as e:
                    print(f"Issue occurred when processing kafka-stream-bindings::{e}")

    repo_manager.remove_repositories()
    build_neo4j_db(database_manager)
