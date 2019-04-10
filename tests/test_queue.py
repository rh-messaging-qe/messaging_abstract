from iqa.components.abstract.component import Address, Queue
from iqa.components.abstract.component.server.broker.route import RoutingType

address = Address(name='address_1', routing_type=RoutingType.ANYCAST)
queue = Queue(name='Test_Queue_1', routing_type=RoutingType.ANYCAST, address=address)


class TestQueue:

    def test_queue_name(self):
        assert queue.name == 'Test_Queue_1'

    def test_queue_address(self):
        assert queue.address == address

    def test_queue_fqqn(self):
        assert '%s::%s' % (address.name, queue.name) == queue.fqqn
