from enum import Enum
from executor import Executor, Command
import re

from iqa_common.executor import Execution, ExecutorAnsible, CommandAnsible
from iqa_common.utils.docker_util import DockerUtil


class ServiceStatus(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FAILED = 'failed'
    UNKNOWN = 'unknown'


class Service(object):
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

    TIMEOUT = 20


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

        if not execution.completed_successfully():
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


    class ServiceDockerState(Enum):
        STARTED = ('start', 'started')
        STOPPED = ('stop', 'stopped')
        RESTARTED = ('restart', 'started')


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

            return CommandAnsible('name=%s state=%s restart=%s' % (self.name, state, restart),
                                  ansible_module='docker',
                                  stdout=True,
                                  timeout=self.TIMEOUT)
        else:
            state = service_state.system_state
            return Command(['docker', state, self.name], stdout=True, timeout=self.TIMEOUT)
