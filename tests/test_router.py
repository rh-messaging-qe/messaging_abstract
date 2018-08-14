from messaging_abstract.router import Router


class TestRouter:

    def test_router_node(self):
        router = Router()
        assert router
