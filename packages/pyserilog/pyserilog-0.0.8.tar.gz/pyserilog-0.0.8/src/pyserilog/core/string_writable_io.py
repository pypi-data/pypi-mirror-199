from abc import ABC, abstractmethod
from io import StringIO


class StringWriteableIO(ABC):

    @abstractmethod
    def write(self, value: str):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __enter__(self):
        return self


class StringIOWritable(StringWriteableIO):
    def __init__(self):
        self._output = StringIO()

    def write(self, value: str):
        if isinstance(value, str):
            self._output.write(value)
        else:
            raise ValueError("value type should be string")

    def getvalue(self):
        return self._output.getvalue()

    def close(self):
        self._output.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._output.close()

    def __str__(self):
        return self._output.getvalue()
