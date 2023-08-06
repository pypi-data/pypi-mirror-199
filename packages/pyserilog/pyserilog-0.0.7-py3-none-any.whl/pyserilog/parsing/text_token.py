from io import StringIO

from pyserilog.guard import Guard
from pyserilog.parsing.message_template_token import MessageTemplateToken


class TextToken(MessageTemplateToken):

    def __init__(self, text: str, start_index: int = -1):
        super().__init__(start_index)
        Guard.against_null(text)
        self._text = text

    @property
    def text(self):
        return self._text

    def render(self, properties: dict, writer: StringIO):
        pass

    @property
    def length(self) -> int:
        return len(self._text)

    def __eq__(self, other):
        if not isinstance(other, TextToken):
            return False
        return other._text == self._text

    def __str__(self):
        return self._text
