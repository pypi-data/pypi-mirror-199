from abc import ABC, abstractmethod

from io import StringIO


class ITextFormatter(ABC):

    @abstractmethod
    def format(self, log_event, output: StringIO):
        pass
