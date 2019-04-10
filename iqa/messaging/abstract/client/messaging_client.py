from abc import ABC, abstractmethod

from iqa.messaging.abstract.client import Client
from iqa.messaging.abstract.listener import Listener


class MessagingClient(Client):
    """
    Abstract class for every abstract messaging client
    """

    # Required variables
    supported_protocols = []
    name = None
    version = None

    def __init__(self, name: str, **kwargs):
        self.url = None  # connectionUrl
        self.users = None
        self.logs = None
        self._messages = None

    @abstractmethod
    def set_url(self, url: str):
        pass

    @abstractmethod
    def set_endpoint(self, listener : Listener):
        pass


    @abstractmethod
    def connect(self):
        """
        Create connection to the endpoint
        :return:
        :rtype:
        """
        pass

    @property
    @abstractmethod
    def get_messages(self):
        """

        :return:
        :rtype: List<Messages>
        """
        return self._messages
