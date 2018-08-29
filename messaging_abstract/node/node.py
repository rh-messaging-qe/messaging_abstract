"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from iqa_common.executor import Executor, Command, Execution, ExecutorAnsible, CommandAnsible
import re
import copy


@logged
@traced
class Node:
    """Node component."""

    def __init__(self, hostname: str, executor: Executor, ip: str=None):
        self.hostname = hostname
        Node.__log.info('Initialization of node %s..' % self.hostname)
        self.executor = executor
        self.ip = ip if ip else self._get_ip()

    def execute(self, command: Command) -> Execution:
        """Execute command on node"""
        return self.executor.execute(command)

    def ping(self) -> bool:
        """Send ping to node"""
        cmd_ping = Command([], stdout=True, timeout=20)
        if isinstance(self.executor, ExecutorAnsible):
            cmd_ping = CommandAnsible(ansible_module="ping", stdout=True, timeout=20)
        else:
            # If unable to determine ip address, then do not perform ping
            if self._get_ip() is None:
                return False
            cmd_ping.args = ['ping', '-c', '1', self._get_ip()]

        execution = self.executor.execute(cmd_ping)

        # True if completed with exit code 0 and stdout has some data
        return execution.completed_successfully() and bool(execution.read_stdout())

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
