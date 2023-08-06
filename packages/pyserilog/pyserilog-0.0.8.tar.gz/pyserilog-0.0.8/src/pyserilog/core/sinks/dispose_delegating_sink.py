from typing import Callable

from pyserilog.core.ilog_event_sink import ILogEventSink
from pyserilog.events import log_event


class DisposeDelegatingSink(ILogEventSink):
    def __init__(self, sink: ILogEventSink, exitable):
        self._sink = sink
        self._exitable = exitable

    def emit(self, log_event: log_event):
        self._sink.emit(log_event)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._exitable is not None and hasattr(self._exitable , "__exit__"):
            self._exitable.__exit__(exc_type, exc_val, exc_tb)
