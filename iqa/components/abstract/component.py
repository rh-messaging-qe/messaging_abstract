from inspect import signature

from iqa.system.command.command_base import Command
from iqa.system.executor import Execution
from iqa.system.node.node import Node


class Component(object):
    """
    Main class that represents a abstract component.
    """

    def __init__(self, name: str, node: Node):
        self.name: str = name
        self.node: Node = node

    def execute(self, command: Command) -> Execution:
        # TODO want to have it here?
        return self.node.executor.execute(command)

    @property
    def implementation(self):
        raise NotImplementedError

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
