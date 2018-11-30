from iqa_common.executor import Executor

from messaging_abstract.component.server.broker.address import Address
from messaging_abstract.component.server.server import Server
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node
from .queue import Queue
from typing import List
import abc


class Broker(Server, abc.ABC):
    """
    Abstract broker class
    """
    supported_protocols = []

    def __init__(self, name: str, node: Node, executor: Executor, service: Service,
                 broker_name: str=None, broker_path: str=None, web_port=8161, **kwargs):
        super(Broker, self).__init__(name, node, executor, service)

        self.broker_name = kwargs.get('broker_name', broker_name)
        self.broker_path = kwargs.get('broker_path', broker_path)
        self.web_port = kwargs.get('broker_web_port', web_port)
        self.user = kwargs.get('broker_user', None)
        self.password = kwargs.get('broker_password', None)

    @abc.abstractmethod
    def queues(self, refresh: bool=True) -> List[Queue]:
        """
        Must return existing queues
        :return:
        """
        pass

    @abc.abstractmethod
    def addresses(self, refresh: bool=True) -> List[Address]:
        """
        Must return existing addresses
        :return:
        """

    @abc.abstractmethod
    def create_address(self, address: Address):
        """
        Creates an address using its name and specialized type (ANYCAST, MULTICAST).
        :param address:
        :return:
        """
        pass

    @abc.abstractmethod
    def create_queue(self, queue: Queue, address: Address, durable: bool=True):
        """
        Creates a queue using its name and specialized type, nested to the given address.
        :param queue:
        :param address:
        :param durable:
        :return:
        """
        pass

    @abc.abstractmethod
    def delete_address(self, name: str, force: bool = False):
        """
        Deletes a given address.
        :param name:
        :param force:
        :return:
        """
        pass

    @abc.abstractmethod
    def delete_queue(self, name: str, remove_consumers: bool = False):
        """
        Deletes a given queue.
        :param name:
        :param remove_consumers:
        :return:
        """
        pass
