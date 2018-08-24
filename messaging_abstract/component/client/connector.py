"""
    # TODO jstejska: Package description
"""
from iqa_common.executor import Executor
from messaging_abstract.component.client import Client
from messaging_abstract.node.node import Node


class Connector(Client):
    """Abstract class of client's connectors."""

    def __init__(self, name: str, node: Node, executor: Executor):
        super(Connector, self).__init__(name, node, executor)

    def connect(self) -> bool:
        raise NotImplementedError
