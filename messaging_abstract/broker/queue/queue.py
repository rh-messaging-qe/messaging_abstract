"""
@TODO: dlenoch: Publish-Subscribe | queue routing type (Anycast, Multicast)
@TODO: dlenoch: Point-to-Point | More queues on one Address
"""
from messaging_abstract.broker.address import Address


class QueueAnycast:
    pass


class QueueMulticast:
    pass


class Queue:
    """
    Abstract Queue class
    """
    def __init__(self, name: str, address: Address, messages=None):
        if messages is None:
            messages = []
        self.name = name
        self.address = address
        self.messages = messages
