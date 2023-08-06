from abc import ABC, abstractmethod
from io import StringIO
from typing import Callable


class LogEventPropertyValue(ABC):

    @abstractmethod
    def render(self, output: StringIO, text_format: str | None = None, formatter: Callable[[object], str] = None):
        pass

    def __str__(self) -> str:
        string_writer = StringIO()
        self.render(string_writer)
        res = string_writer.getvalue()
        string_writer.close()
        return res
