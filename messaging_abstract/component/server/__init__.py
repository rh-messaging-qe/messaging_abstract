from .server import *
from .router import *
from .broker import *
from .service import *


class ServiceFactory(object):

    @staticmethod
    def create_service(executor: Executor, service_name: str=None, **kwargs):

        if service_name:
            return ServiceSystem(name=service_name, executor=executor)
        elif isinstance(executor, ExecutorContainer):
            return ServiceDocker(name=kwargs.get('inventory_hostname'), executor=executor)

        raise ValueError('Unable to determine service for server component')
