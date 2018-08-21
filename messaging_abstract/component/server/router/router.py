from executor import Executor

from messaging_abstract.component.server.server import Server
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node


class Router(Server):
    """
    Abstract messaging Router
    """

    def __init__(self, name: str, node: Node, executor: Executor, service: Service):
        super(Router, self).__init__(name, node, executor, service)
