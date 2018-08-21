"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from messaging_abstract.component.client import Client
from messaging_abstract.broker import Broker
from messaging_abstract.router import Router
from iqa_common.executor import Executor, Command, Execution, ExecutorAnsible
import re, copy


@logged
@traced
class Node:
    """Node component."""

    def __init__(self, hostname: str, executor: Executor, ip: str=None):
        self.hostname = hostname
        Node.__log.info('Initialization of node %s..' % self.hostname)
        self.executor = executor
        self.ip = ip if ip else self._get_ip()
        self.components = []  # type:

    def execute(self, command: Command) -> Execution:
        """Execute command on node"""
        return self.executor.execute(command)

    def ping(self) -> bool:
        """Send ping to node"""
        executor = copy.deepcopy(self.executor)
        cmd_ping = Command([], stdout=True, timeout=20)
        if isinstance(executor, ExecutorAnsible):
            executor.module = 'ping'
        else:
            cmd_ping.args = ['ping', '-c', '1', self._get_ip()]

        execution = executor.execute(cmd_ping)

        # True if completed with exit code 0 and stdout has some data
        return execution.completed_successfully() and execution.read_stdout()

    def _get_ip(self):
        """Get ip of node"""
        cmd_ip = Command(['ip', 'addr', 'list'], stdout=True, timeout=10)
        execution = self.execute(cmd_ip)

        # If execution failed, skip it
        if not execution.completed_successfully():
            return None

        # Parsing stdout and retrieving the IP
        ip_addr_out = execution.read_stdout()
        if not ip_addr_out:
            return None

        # Parse all returned ip addresses
        ip_addresses = re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', ip_addr_out, re.MULTILINE)
        try:
            ip_addresses.remove('127.0.0.1')
        except ValueError:
            return None

        # If only loop back defined, skip it
        if not ip_addresses:
            return None

        return ip_addresses[0]

    def new_component(self, component):
        """Adding component to under node.

        :param component:
        :type component:

        :return: Component object
        :rtype:
        """
        component = component(node=self)
        self.components.append(component)
        return component

    @property
    def brokers(self):
        """
        Get all broker instances on this node
        :return:
        """
        return [component for component in self.components
                if issubclass(component, Broker)]

    @property
    def clients(self):
        """
        Get all client instances on this node
        @TODO
        :return:
        """
        return [component for component in self.components
                if issubclass(component, Client)]

    @property
    def routers(self):
        """
        Get all router instances on this node
        @TODO
        :return:
        """
        return [component for component in self.components
                if issubclass(component, Router)]
