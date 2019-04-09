from iqa.abstract.components.component import Component
from iqa.abstract.components.configuration import Configuration
from iqa.abstract.components.management.client import ManagementClient
from iqa.abstract.messaging.listener import Listener
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
