from iqa_common.executor import Executor

from messaging_abstract.component.component import Component
from messaging_abstract.node.node import Node


class Client(Component):
    """
    Abstract class for every messaging client
    """

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(Client, self).__init__(name, node, executor)

    @property
    def supported_protocols(self) -> list:
        raise NotImplementedError

    @property
    def version(self) -> list:
        raise NotImplementedError

    @property
    def implementation(self) -> list:
        raise NotImplementedError
