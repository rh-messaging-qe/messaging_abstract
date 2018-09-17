"""
    # TODO jstejska: Package description
"""
from iqa_common.executor import Executor, Execution

from messaging_abstract.component.client.command.client_command import ClientCommand
from messaging_abstract.component.component import Component
from messaging_abstract.node.node import Node
from inspect import signature

class Client(Component):
    """
    Abstract class for every messaging client
    """

    # Required variables
    supported_protocols = []
    version = ''

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
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

    # Default is run forever
    # As mixing --timeout with --count is causing issues
    TIMEOUT = 90

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(ClientExternal, self).__init__(name, node, executor, **kwargs)
        self.execution = None  # type: Execution
        self._command = None  # type: ClientCommand
        self._url = None  # type: str
        self.reset_command()

        # initializing client from kwargs
        for func in [self.set_url, self.set_auth_mechs, self.set_ssl_auth]:
            self.call_if_all_arguments_in_kwargs(func, **kwargs)

    @staticmethod
    def call_if_all_arguments_in_kwargs(func, **kwargs):
        """
        Call the given function if all declared arguments exist in
        the kwargs dictionary. In example, if passed function is set_ssl_auth,
        it will be called if kwargs contains the following keys:
        pem_file, key_file, keystore, keystore_pass and keystore_alias.
        :param func:
        :param extra_args:
        :return:
        """
        # kwargs not informed
        if not kwargs:
            return

        # Not all function arguments needed are available in kwargs
        if not all([k in list(kwargs.keys()) for k in list(signature(func).parameters.keys())]):
            return

        # Calling function if all args present in kwargs
        arg_dict = {k: v for k, v in kwargs.items() if k in list(signature(func).parameters.keys())}
        func(**arg_dict)

    @property
    def command(self) -> ClientCommand:
        return self._command

    def reset_command(self):
        self._command = self._new_command(stdout=True, timeout=ClientExternal.TIMEOUT,
                                          daemon=True)  # type: ClientCommand

    def get_url(self):
        return self._url

    def set_url(self, url: str):
        self._set_url(url)

    def _new_command(self, stdout: bool=False, stderr: bool=False,
                daemon: bool=False, timeout: int=0,
                encoding: str="utf-8") -> ClientCommand:
        raise NotImplementedError

    def _set_url(self, url: str):
        raise NotImplementedError

    def set_auth_mechs(self, mechs: str):
        raise NotImplementedError

    def set_ssl_auth(self, pem_file: str=None, key_file: str=None, keystore: str=None,
                     keystore_pass: str=None, keystore_alias: str=None):
        raise NotImplementedError
