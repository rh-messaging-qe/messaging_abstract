from abc import abstractmethod

from iqa.abstract.messaging.client import Client
from iqa.abstract.messaging.message import Message


class Sender(Client):
    """Abstract class of sender client."""

    def __init__(self, name: str, **kwargs):
        super(Sender, self).__init__(name, **kwargs)
        # Sender settings
        self.message_buffer = None  # type: bool
        self.messages = []  # type: list
        self.sent_messages = 0  # type: int

    @property
    def last_message(self):
        """Method for pickup last received message.
        :return: Last message received or None
        :rtype: messaging_abstract.message.Message
        """
        return self.messages[-1] if self.messages else None

    def send(self, message: Message, **kwargs):
        """Method for send message.
        :param message: Message to be sent
        :type: messaging_abstract.message.Message
        """
        if self.message_buffer:
            self.messages.append(message)

        self.sent_messages += 1
        self._send(message, **kwargs)

    @abstractmethod
    def _send(self, message: Message, **kwargs):
        raise NotImplementedError
