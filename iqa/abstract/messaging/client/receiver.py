from abc import abstractmethod

from iqa.abstract.messaging.client import Client
from iqa.abstract.messaging.message import Message


class Receiver(Client):
    """Abstract class of client's receivers."""

    def __init__(self, name: str, message_buffer=True, **kwargs):
        super(Receiver, self).__init__(name, **kwargs)

        # Sender settings
        self.message_buffer = message_buffer  # type: bool
        self.messages = []  # type: list[Message]
        self.received_messages = 0  # type: int

    @property
    def last_message(self):
        """Method for pickup last received message.
        :return: Last message received or None
        :rtype: messaging_abstract.message.Message
        """
        return self.messages[-1] if self.messages else None

    def receive(self):
        """Method for receive message.
        :param message: Received message to be stored
        :type message: messaging_abstract.message.Message
        """
        recv_messages = self._receive()
        if self.message_buffer:
            self.messages.extend(recv_messages)
        self.received_messages += len(recv_messages)

    @abstractmethod
    def _receive(self):
        raise NotImplementedError
