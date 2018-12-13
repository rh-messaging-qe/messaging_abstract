import re
import traceback
from enum import Enum

from iqa_common.executor import Execution, ExecutorAnsible, CommandAnsible, Executor, Command, ExecutorContainer, \
    CommandContainer
from iqa_common.utils.docker_util import DockerUtil


class ServiceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FAILED = 'failed'
    UNKNOWN = 'unknown'


class Service(object):
    """
    Represents a service used to control a Server component (Router or Broker).
    """

    TIMEOUT = 20

    def __init__(self, name: str, executor: Executor):
        self.name = name
        self.executor = executor

    def status(self) -> ServiceStatus:
        """
        Returns the service status
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        raise NotImplementedError()

    def start(self) -> Execution:
        raise NotImplementedError()

    def stop(self) -> Execution:
        raise NotImplementedError()

    def restart(self) -> Execution:
        raise NotImplementedError()

    def enable(self) -> Execution:
        raise NotImplementedError()

    def disable(self) -> Execution:
        raise NotImplementedError()


class ServiceSystem(Service):
    """
    Implementation of a systemd or initd service used to manage a Server component.
    """

    class ServiceSystemState(Enum):
        STARTED = ('start', 'started')
        STOPPED = ('stop', 'stopped')
        RESTARTED = ('restart', 'restarted')
        ENABLED = ('enable', 'enabled')
        DISABLED = ('disable', 'disabled')

        def __init__(self, system_state, ansible_state):
            self.system_state = system_state
            self.ansible_state = ansible_state

    def status(self) -> ServiceStatus:
        """
        Returns the service status based on linux service.
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        # service output :
        # is running
        # is stopped

        # systemctl output:
        # (running)
        # (dead)

        # On RHEL7> service is automatically redirected to systemctl
        cmd_status = Command(['service', self.name, 'status'], stdout=True, timeout=self.TIMEOUT)
        execution = self.executor.execute(cmd_status)

        if not execution.read_stdout():
            return ServiceStatus.FAILED

        service_output = execution.read_stdout()

        if re.search('(is running|\(running\))', service_output):
            return ServiceStatus.RUNNING
        elif re.search('(is stopped|\(dead\))', service_output):
            return ServiceStatus.STOPPED

        return ServiceStatus.UNKNOWN

    def start(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceSystemState.STARTED))

    def stop(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceSystemState.STOPPED))

    def restart(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceSystemState.RESTARTED))

    def enable(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceSystemState.ENABLED))

    def disable(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceSystemState.DISABLED))

    def _create_command(self, service_state: ServiceSystemState):
        """
        Creates a Command instance based on executor type and state
        that is specific to each type of command.
        :param service_state:
        :return:
        """
        if isinstance(self.executor, ExecutorAnsible):
            state = service_state.ansible_state
            return CommandAnsible('name=%s state=%s' % (self.name, state),
                                  ansible_module='service',
                                  stdout=True,
                                  timeout=self.TIMEOUT)
        else:
            state = service_state.system_state
            return Command(['service', self.name, state], stdout=True, timeout=self.TIMEOUT)


class ServiceDocker(Service):
    """
    Implementation of a service represented by a docker container.
    So startup and shutdown are done by managing current state of related
    docker container name.
    """

    class ServiceDockerState(Enum):
        STARTED = ('start', 'started')
        STOPPED = ('stop', 'stopped')
        RESTARTED = ('restart', 'started')

        def __init__(self, system_state, ansible_state):
            self.system_state = system_state
            self.ansible_state = ansible_state

    def status(self) -> ServiceStatus:
        """
        Returns the status based on status of container name.
        :return: The status of this specific service
        :rtype: ServiceStatus
        """
        try:
            container = DockerUtil.get_container(self.name)
            if not container:
                return ServiceStatus.UNKNOWN

            if container.status == 'running':
                return ServiceStatus.RUNNING
            elif container.status == 'exited':
                return ServiceStatus.STOPPED
        except Exception:
            traceback.print_tb()
            return ServiceStatus.FAILED

        return ServiceStatus.UNKNOWN

    def start(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceDockerState.STARTED))

    def stop(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceDockerState.STOPPED))

    def restart(self) -> Execution:
        return self.executor.execute(self._create_command(self.ServiceDockerState.RESTARTED))

    def enable(self) -> Execution:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None

    def disable(self) -> Execution:
        """
        Simply ignore it (not applicable to containers)
        :return:
        """
        return None

    def _create_command(self, service_state: ServiceDockerState):
        """
        Creates a Command instance based on executor type and state
        that is specific to each type of command.
        :param service_state:
        :return:
        """
        if isinstance(self.executor, ExecutorAnsible):
            state = service_state.ansible_state
            restart = 'no'
            if service_state == self.ServiceDockerState.RESTARTED:
                restart = 'yes'

            print('name=%s state=%s restart=%s' % (self.name, state, restart))
            return CommandAnsible('name=%s state=%s restart=%s' % (self.name, state, restart),
                                  ansible_module='docker_container',
                                  stdout=True,
                                  timeout=self.TIMEOUT)
        elif isinstance(self.executor, ExecutorContainer):
            state = service_state.system_state
            return CommandContainer([], docker_command=state, stdout=True, timeout=self.TIMEOUT)
        else:
            state = service_state.system_state
            return Command(['docker', state, self.name], stdout=True, timeout=self.TIMEOUT)
