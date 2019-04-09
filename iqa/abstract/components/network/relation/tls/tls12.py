from autologging import logged, traced
from messaging_abstract.protocol import Protocol

@logged
@traced
class TLS12(Protocol):
    def __init__(self):
        Protocol.__init__(self)
        self.name = 'TLS 1.2'
