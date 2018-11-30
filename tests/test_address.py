import pytest

from messaging_abstract.component import Address
from messaging_abstract.component.server.broker.route import RoutingType


class TestAddress:

    @pytest.mark.parametrize("routing_type", [RoutingType.ANYCAST, RoutingType.MULTICAST])
    def test_address(self, routing_type: RoutingType):
        test_address = Address(name='x', routing_type=routing_type)
        assert test_address.name == 'x'
        assert test_address.routing_type == routing_type
