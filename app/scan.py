import os
from configparser import RawConfigParser

from yaml import CLoader, load_all

from app.repository import RepositoryConfiguration


class ScannerConfiguration:
    """
    This class contains all the relevant scanning logic for looking
    through and parsing repositories.
    """

    def __init__(self, scanner_config: RawConfigParser):
        self.repositories = []
        self.scanner_config = scanner_config

        for section in self.scanner_config:
            if self.scanner_config[section].name == 'DEFAULT':
                # Ignore default section always
                continue
            self.__append_repositories(section)

    def __append_repositories(self, section):
        section_name = self.scanner_config[section].name
        section_under_append = self.scanner_config[section]
        try:
            git_url = section_under_append['git_url']
            csv_files = section_under_append['scan_files'].split(',')
            binding_urls = section_under_append['remote_urls'].split(',')
            self.repositories.append(RepositoryConfiguration(section_name, git_url, csv_files, binding_urls))
        except KeyError:
            print("Invalid section provided, ignoring")


def find_all(name, path) -> list:
    """
    This method returns a list of the fully qualified path
    of all files that match the path provided by the given name.
    :param name: name of the file to query for
    :param path: the path to use for file querying
    :return: the list of files found from the search by name
    """
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def search_files(target_repository: RepositoryConfiguration) -> list:
    """
    Walk through configured repository and retrieve a list of files
    that meet the configured filter
    :param target_repository: repository object containing config data
    :return: list of files found within repository
    """
    retrieved_files = []

    for search_file in target_repository.files:
        for retrieved_file in find_all(search_file, target_repository.name):
            if retrieved_file not in retrieved_files:
                retrieved_files.append(retrieved_file)
    return retrieved_files


def parse_yaml(path):
    # TODO - update this to higher quality
    with open(path, 'r') as file:
        try:
            # Convert generator to list
            return list(load_all(file, CLoader))
        except Exception as e:
            print(f"Something went wrong parsing {path}::ERROR::{e}")


def parse_stream_bindings(parsed_file):
    # TODO - merge binding functions together
    try:
        binding_dicts = parsed_file['spring']['cloud']['stream']['bindings']
        for binding_dict in list(binding_dicts.items()):
            return binding_dict
    except KeyError:
        # If we get a keyerror, this file doesn't have spring.cloud.stream.bindings, so we ignore it
        # TODO - need to refactor how this is processed by checking existence before retrieval
        pass


def parse_kafka_stream_bindings(parsed_file):
    # TODO - merge binding functions together
    try:
        binding_dicts = parsed_file['spring']['cloud']['stream']['kafka']['bindings']
        for binding_dict in list(binding_dicts.items()):
            return binding_dict
    except KeyError:
        # If we get a keyerror, this file doesn't have spring.cloud.stream.bindings, so we ignore it
        # TODO - need to refactor how this is processed by checking existence before retrieval
        pass


def get_bindings(parsed_files) -> (list, list):
    """
    Retrieve lists of supported bindings
    :param parsed_files: incoming files to parse for bindings
    :return: spring-cloud-stream bindings, kafka-stream bindings
    """
    cloud_stream_bindings = []
    kafka_stream_bindings = []

    if parsed_files is None:
        return [], []
    for parsed_file in parsed_files:
        cloud_stream_bindings.append(parse_stream_bindings(parsed_file))
        kafka_stream_bindings.append(parse_kafka_stream_bindings(parsed_file))
    print(f'Found {len(cloud_stream_bindings)} cloud stream bindings')
    print(f'Found {len(kafka_stream_bindings)} kafka streams bindings')

    return cloud_stream_bindings, kafka_stream_bindings

