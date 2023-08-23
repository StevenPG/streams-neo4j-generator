from py2neo import Node, Relationship

OUT = "out"
IN = "in"
consumed_by = "CONSUMED_BY"
produces_to = "PRODUCES_TO"
unknown_relation = "---"


class BindingsManager:

    @staticmethod
    def get_binding_type(binding_string):
        """
        Static method to convert binding string details into a simple string.
        Build in this manner to allow for extensibility or custom string parsing.
        :param binding_string: spring cloud streams naming patterned binding, e.g. someBinding-out-0
        :return:
        """
        if "-out-" in binding_string:
            return OUT
        elif "-in-" in binding_string:
            return IN
        else:
            return "---"

    @staticmethod
    def binding_type_to_relationship_type(binding_type):
        """
        Simple mapping between binding_type from spring cloud stream binding name
        :param binding_type: e.g. -out-
        :return:
        """
        if binding_type == OUT:
            return consumed_by
        elif binding_type == IN:
            return produces_to
        else:
            return unknown_relation

    def get_relationship(self, destination, binding_type, node) -> (Node, Relationship):
        """
        Generate a relationship object between a destination and a node
        :param destination: target destination from cloud streams configuration
        :param binding_type: the binding type to be parsed into a binding "direction"
        :param node: the specific node this relationship will be mapped to, the other node being the binding node
        :return: the node and relationship using the node and the input destination
        """
        relationship_type = self.binding_type_to_relationship_type(binding_type)
        if relationship_type == consumed_by:
            binding_node = Node(*["Topic"], **{
                "name": destination
            })
            return binding_node, Relationship(*[binding_node, consumed_by, node])
        elif relationship_type == produces_to:
            binding_node = Node(*["Topic"], **{
                "name": destination
            })
            return binding_node, Relationship(*[node, produces_to, binding_node])
        else:
            binding_node = Node(*["Topic"], **{
                "name": destination
            })
            return binding_node, Relationship(*[node, unknown_relation, binding_node])

    def process_bindings(self, stream_bindings, node) -> (list, list):
        """
        Receive a list of stream bindings in tuple format and process into a binding node and relationships
        :param stream_bindings: incoming binding definition tuple where binding[0]
                                is the binding name and binding[1] is the destination
        :param node: the source of this data that will be half of the mapped binding relationship
        :return:
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
