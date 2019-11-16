import typing
from enum import Enum

from graphviz.dot import Dot

from cloudformation.resource_change import ResourceChange


class Change(object):
    """
    The Change structure describes the changes AWS CloudFormation will perform if you execute the change set.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_Change.html
    """

    def __init__(self, o: typing.Mapping):
        # Strings and Enums
        self.type = Type(o['Type'])

        # Objects
        self.resource_change = ResourceChange(o['ResourceChange'])

    def render(self, dot: Dot) -> None:
        # the change itself contains nothing, render the resource change
        self.resource_change.render(dot)



class Type(Enum):
    RESOURCE = 'Resource'
