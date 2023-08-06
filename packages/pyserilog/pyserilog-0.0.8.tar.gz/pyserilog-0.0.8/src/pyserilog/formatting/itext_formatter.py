from abc import ABC, abstractmethod

from pyserilog.core.string_writable_io import StringIOWritable
from typing import TextIO


class ITextFormatter(ABC):

    @abstractmethod
    def format(self, log_event, output: StringIOWritable | TextIO):
        pass
