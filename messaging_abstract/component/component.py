from iqa_common.executor import Executor, Execution, Command

from messaging_abstract.node.node import Node


class Component(object):

    def __init__(self, name: str, node: Node, executor: Executor):
        self.name: str = name
        self.node: Node = node
        self.executor: Executor = executor

    def execute(self, command: Command) -> Execution:
        return self.executor.execute(command)

    @property
    def implementation(self):
        raise NotImplementedError
