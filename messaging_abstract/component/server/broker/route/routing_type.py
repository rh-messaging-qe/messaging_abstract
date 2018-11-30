from enum import Enum, auto


class RoutingType(Enum):
    """
    Routing type
    """
    ANYCAST = auto()
    MULTICAST = auto()
    BOTH = auto()

    @staticmethod
    def from_value(value: str):
        if not value:
            return RoutingType.ANYCAST

        if value == 'ANYCAST':
            return RoutingType.ANYCAST
        elif value == 'MULTICAST':
            return RoutingType.MULTICAST
        else:
            return RoutingType.BOTH
