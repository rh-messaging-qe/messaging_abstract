from abc import ABC, abstractmethod

from iqa.abstract.messaging.listener import Listener


class Client(ABC):
    """
    Abstract class for every messaging client
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
