from enum import Enum, auto


class RoutingType(Enum):
    """
    Routing type
    """
    ANYCAST = auto()
    MULTICAST = auto()
    BOTH = auto()
