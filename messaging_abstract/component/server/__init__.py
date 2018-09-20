from .server import *
from .router import *
from .broker import *
from .service import *


class ServiceFactory(object):
    """
    This factory class can be used to help defining how Service implementation of the
    given Server Component will be used to manage startup/shutdown and ping of related
    component.

    When component is running in a docker container, startup/shutdown is done by
    starting / stopping the container.

    Otherwise a valid service name must be provided.
    """

    @staticmethod
    def create_service(executor: Executor, service_name: str=None, **kwargs):

        if service_name:
            return ServiceSystem(name=service_name, executor=executor)
        elif isinstance(executor, ExecutorContainer):
            return ServiceDocker(name=kwargs.get('inventory_hostname'), executor=executor)

        raise ValueError('Unable to determine service for server component')
