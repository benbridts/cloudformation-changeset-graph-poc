import typing

from cloudformation.rollback_trigger import RollbackTrigger


class RollbackConfiguration(object):
    """
    Structure containing the rollback triggers.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_RollbackConfiguration.html
    """

    def __init__(self, o: typing.Mapping):
        self.monitoring_time_in_minutes = o['MonitoringTimeInMinutes']  # type: int
        self.rollback_triggers = [RollbackTrigger(x) for x in o['RollbackTriggers']]
