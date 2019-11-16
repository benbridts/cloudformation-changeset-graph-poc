import typing


class Tag(object):
    def __init__(self, o: typing.Mapping) -> None:
        self.key = o["Key"]
        self.value = o["Value"]
