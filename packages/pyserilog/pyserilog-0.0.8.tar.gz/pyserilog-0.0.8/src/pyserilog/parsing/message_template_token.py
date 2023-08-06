from abc import ABC, abstractmethod
from pyserilog.core.string_writable_io import StringIOWritable


class MessageTemplateToken(ABC):

    def __init__(self, start_index: int):
        self._start_index = start_index

    @property
    def start_index(self) -> int:
        return self._start_index

    @abstractmethod
    def length(self) -> int:
        pass

    @abstractmethod
    def render(self, properties: dict, writer: StringIOWritable):
        pass
