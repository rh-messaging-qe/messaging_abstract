from iqa_common.executor import Executor
from messaging_abstract.component.client import Client
from messaging_abstract.node.node import Node


class Connector(Client):
    """Abstract class of client's connectors."""

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(Connector, self).__init__(name, node, executor, **kwargs)

    def connect(self) -> bool:
        raise NotImplementedError

    @property
    def supported_protocols(self) -> list:
        raise NotImplementedError

    @property
    def version(self) -> list:
        raise NotImplementedError

    @property
    def implementation(self) -> list:
        raise NotImplementedError
