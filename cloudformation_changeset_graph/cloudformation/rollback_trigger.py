import typing


class RollbackTrigger(object):
    """
    A rollback trigger AWS CloudFormation monitors.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_RollbackTrigger.html
    """

    def __init__(self, o: typing.Mapping):
        self.arn = o["Arn"]  # type: str
        self.type = o["Type"]  # type: str
