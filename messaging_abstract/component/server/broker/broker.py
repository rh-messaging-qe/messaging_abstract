from iqa_common.executor import Executor
from messaging_abstract.component.server.server import Server
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node
from .queue import Queues


class Broker(Server):
    """
    Abstract broker class
    """
    supported_protocols = []

    def __init__(self, name: str, node: Node, executor: Executor, service: Service,
                 broker_name: str=None, config: str=None, web_port=8161):
        super(Broker, self).__init__(name, node, executor, service)
        self.queues = Queues()
        self.broker_name = broker_name
        self.config = config
        self.web_port = web_port
