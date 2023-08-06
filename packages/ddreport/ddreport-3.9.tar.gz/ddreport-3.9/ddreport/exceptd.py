class PytestErrorContent(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ExceptContentObj:
    def __init__(self):
        self.value = None

    def raiseException(self, data):
        self.value = data
        pytestRaiseExcept()


def pytestRaiseExcept():
    raise PytestErrorContent(exceptContentObj)


exceptContentObj = ExceptContentObj()