from iqa_common.executor import Executor
from messaging_abstract.message import Message
from messaging_abstract.node.node import Node
from .client import Client


class Sender(Client):
    """Abstract class of client's senders."""

    def __init__(self, name: str, node: Node, executor: Executor, message_buffer: bool = False, **kwargs):
        """
        Sender init
        :param name:
        :param node:
        :param executor:
        :param message_buffer:
        :param kwargs:
        """
        super(Sender, self).__init__(name, node, executor, **kwargs)
        # Sender settings
        self.message_buffer = message_buffer  # type: bool
        self.messages = []  # type: list
        self.sent_messages = 0  # type: int

    @property
    def supported_protocols(self) -> list:
        raise NotImplementedError

    @property
    def version(self) -> list:
        raise NotImplementedError

    @property
    def implementation(self) -> list:
        raise NotImplementedError

    @property
    def last_message(self):
        """Method for pickup last received message.
        :return: Last message received or None
        :rtype: messaging_abstract.message.Message
        """
        return self.messages[-1] if self.messages else None

    def send(self, message: Message = None, **kwargs):
        """Method for send message.
        :param message: Message to be sent
        :type: messaging_abstract.message.Message
        """
        message_to_send = message

        if "msg_content" in kwargs:
            message_to_send = kwargs["msg_content"]

        if self.message_buffer:
            self.messages.append(message_to_send)
        else:
            self.messages = [message_to_send]

        self.sent_messages += 1
        self._send(message, **kwargs)

    def _send(self, message: Message, **kwargs):
        raise NotImplementedError
