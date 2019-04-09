from iqa.abstract.messaging.server.messaging_server import MessagingServer


class Router(MessagingServer):
    """
    Abstract messaging Router
    """

    def __init__(self, name: str, **kwargs):
        super(Router, self).__init__()
