from iqa.components.abstract.component import Component
from iqa.components.abstract.configuration import Configuration
from iqa.components.abstract.management.client import ManagementClient
from iqa.messaging.abstract.listener import Listener
from iqa.system.node.node import Node
from iqa.system.service.service import Service


class ServerComponent(Component):
    """
    Super class for all Server component implementations (for now Routers and Brokers).
    """

    @property
    def implementation(self):
        pass

    def __init__(self, name: str, node: Node, service: Service, listeners: list[Listener],
                 management: ManagementClient=None, configuration: Configuration=None):
        super(ServerComponent, self).__init__(name, node)
        self.service = service
        self.name = name
        self.node = node
        self.management = management
        self.configuration = configuration
