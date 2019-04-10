from abc import abstractmethod, ABC

from iqa.messaging.abstract.client import MessagingClient
from iqa.messaging.abstract.message import Message


class Receiver(MessagingClient):
    """Abstract class of client's receivers."""

    def __init__(self, name: str, message_buffer=True, **kwargs):
        super(Receiver, self).__init__(name, **kwargs)
        # Sender settings

    def receive(self):
        """Method for receive message.
        :param message: Received message to be stored
        :type message: iqa.messaging_abstract.message.Message
        """
        recv_messages = self._receive()
        if self.message_buffer:
            self.messages.extend(recv_messages)  # multiple Messages

        self.message_counter += len(recv_messages)

    @abstractmethod
    def _receive(self):
        raise NotImplementedError
