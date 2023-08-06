from typing import Callable, Type

from tp_interfaces.knowledge_base.interfaces import KB
from .abstract import AbstractPluginManager


def _get_stub() -> Type[KB]:
    from tp_interfaces.knowledge_base.stub_kb import DMBCommonnessStub
    return DMBCommonnessStub


class KBPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'KB_FACTORY', _get_stub)

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, Callable)
