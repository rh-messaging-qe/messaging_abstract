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

    TIMEOUT = 20

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ClientExternal, self).__init__(name, node, executor)
        self.execution = None  # type: Execution
        self._command = self._new_command(stdout=True, timeout=ClientExternal.TIMEOUT)  # type: ClientCommand

    @property
    def command(self) -> ClientCommand:
        return self._command

    def _new_command(self, stdout: bool=False, stderr: bool=False,
                daemon: bool=False, timeout: int=0,
                encoding: str="utf-8") -> ClientCommand:
        raise NotImplementedError
