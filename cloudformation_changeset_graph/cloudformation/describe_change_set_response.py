import typing
from datetime import datetime
from enum import Enum

from graphviz.dot import Dot  # type: ignore

from cloudformation.change import Change
from cloudformation.parameter import Parameter
from cloudformation.resource_change_detail import ChangeSource
from cloudformation.rollback_configuration import RollbackConfiguration
from cloudformation.tag import Tag


class DescribeChangeSetResponse(object):
    """
    Returns the inputs for the change set and a list of changes that AWS CloudFormation will make if you execute the change set.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_DescribeChangeSet.html#API_DescribeChangeSet_ResponseElements
    """

    def __init__(self, o: typing.Mapping):
        if "NextToken" in o:
            raise NotImplementedError(
                "ChangeSets with multiple pages are not supported yet"
            )

        creation_time = o["CreationTime"]
        if isinstance(creation_time, str):
            # fromisoformat only supports YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]
            if creation_time.endswith("Z"):
                creation_time = creation_time[:-1] + "+00:00"
            creation_time = datetime.fromisoformat(creation_time)

        # the list of capabilities that were explicitly acknowledged when the change set was created
        self.capabilities = [Capability(x) for x in o["Capabilities"]]

        # The ARN of the change set
        self.change_set_id = o["ChangeSetId"]  # type: str
        # The name of the change set
        self.change_set_name = o["ChangeSetName"]  # type: str
        # The start time when the change set was created
        self.creation_time = creation_time
        # Shows if you can execute the ChangeSet
        self.execution_status = (
            ExecutionStatus(o["ExecutionStatus"]) if ExecutionStatus in o else None
        )
        self.notification_arms = o["NotificationARNs"]  # type: typing.List[str]
        # The ARN of the stack that is associated with the change set.
        self.stack_id = o["StackId"]  # type: str
        # The name of the stack that is associated with the change set.
        self.stack_name = o["StackName"]  # type: str
        # The current status of the change set
        self.status = Status(o["Status"])
        # A description of the change set's status
        self.status_reason = o.get("StatusReason")  # type: typing.Optional[str]

        self.changes = [Change(x) for x in o["Changes"]]
        self.parameters = [Parameter(x) for x in o["Parameters"]]
        self.rollback_configuration = (
            RollbackConfiguration(o["RollbackConfiguration"])
            if "RollbackConfiguration" in o
            else None
        )
        self.tags = [Tag(x) for x in o["Tags"]] if "Tags" in o else None

    @property
    def causing_parameters(self) -> typing.List[Parameter]:
        causing_parameter_keys = set()
        for change in self.changes:
            for detail in change.resource_change.details:
                if detail.change_source == ChangeSource.PARAMETER_REFERENCE:
                    causing_parameter_keys.add(detail.causing_entity)

        return [x for x in self.parameters if x.parameter_key in causing_parameter_keys]

    def render(self, dot: Dot) -> None:
        for change in self.changes:
            change.render(dot)
        for parameter in self.causing_parameters:
            parameter.render(dot)


class Capability(Enum):
    IAM = "CAPABILITY_IAM"
    NAMED_IAM = "CAPABILITY_NAMED_IAM"
    AUTO_EXPAND = "CAPABILITY_AUTO_EXPAND"


class ExecutionStatus(Enum):
    UNAVAILABLE = "UNAVAILABLE"
    AVAILABLE = "AVAILABLE"
    EXECUTE_IN_PROGRESS = "EXECUTE_IN_PROGRESS"
    EXECUTE_COMPLETE = "EXECUTE_COMPLETE"
    EXECUTE_FAILED = "EXECUTE_FAILED"
    OBSOLETE = "OBSOLETE"


class Status(Enum):
    CREATE_PENDING = "CREATE_PENDING"
    CREATE_IN_PROGRESS = "CREATE_IN_PROGRESS"
    CREATE_COMPLETE = "CREATE_COMPLETE"
    DELETE_COMPLETE = "DELETE_COMPLETE"
    FAILED = "FAILED"
