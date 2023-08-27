import requests
import re


def get_remote_binding_json(binding_urls: list) -> list[tuple]:
    # TODO - make the API call here in iteration and return
    stream_bindings = []
    # tuple[1] is destination
    # tuple[0] is binding name

    # TODO - if something goes wrong, just don't include in bindings
    for binding_url in binding_urls:
        binding_json = make_http_request(binding_url)
        for binding in binding_json:
            try:
                binding_name = binding['bindingName']
                destination = binding['name']
                stream_bindings.append((binding_name, destination))
            except KeyError as ke:
                # Ignore if any keys are missing, that means this
                # binding json is invalid
                pass

    return stream_bindings


def make_http_request(binding_url):
    # TODO - optional authorization
    r = requests.get(binding_url)
    return r.json()


"""
        nodes = []
        relationships = []

        for binding in stream_bindings:
            if binding is None:
                # If we found a null binding, just skip processing
                continue

            destination = str(binding[1]['destination'])
            binding_type = BindingsManager.get_binding_type(binding[0])

            binding_node, relationship = self.get_relationship(destination, binding_type, node)
            nodes.append(binding_node)
            relationships.append(relationship)

        return nodes, relationships
"""
