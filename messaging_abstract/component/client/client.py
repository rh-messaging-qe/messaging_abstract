"""
    # TODO jstejska: Package description
"""
from iqa_common.executor import Executor, Execution

from messaging_abstract.component.client.command.client_command import ClientCommand
from messaging_abstract.component.component import Component
from messaging_abstract.node.node import Node


class Client(Component):
    """
    Abstract class for every messaging client
    """

    # Required variables
    supported_protocols = []
    version = ''

    def __init__(self, name: str, node: Node, executor: Executor):
        super(Client, self).__init__(name, node, executor)
        self.logs = None  # @TODO

    @property
    def get_supported_protocols(self):
        return self.supported_protocols

    @property
    def get_name(self):
        return self.name

    @property
    def get_version(self):
        return self.version


class ClientExternal(Client):

    TIMEOUT = 30

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ClientExternal, self).__init__(name, node, executor)
        self.execution = None  # type: Execution
        self._command = None  # type: ClientCommand
        self.reset_command()

    @property
    def command(self) -> ClientCommand:
        return self._command

    def reset_command(self):
        self._command = self._new_command(stdout=True, timeout=ClientExternal.TIMEOUT,
                                          daemon=True)  # type: ClientCommand

    def _new_command(self, stdout: bool=False, stderr: bool=False,
                daemon: bool=False, timeout: int=0,
                encoding: str="utf-8") -> ClientCommand:
        raise NotImplementedError

    def set_url(self, url: str):
        raise NotImplementedError

    def set_auth_mechs(self, mechs: str):
        raise NotImplementedError
