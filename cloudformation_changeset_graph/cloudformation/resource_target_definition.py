import typing
from enum import Enum

from graphviz.dot import Dot

from utils import label_table


class ResourceTargetDefinition(object):
    """
    The field that AWS CloudFormation will change, such as the name of a resource's property, and whether the resource will be recreated.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_ResourceTargetDefinition.html
    """

    def __init__(self, o: typing.Mapping, resource_id: str = None):
        # Strings and Enums
        # Indicates which resource attribute is triggering this update
        self.attribute = Attribute(o["Attribute"])
        # If the Attribute value is Properties, the name of the property. For all other attributes, the value is null.
        self.name = o.get("Name")  # type: str
        #  the Attribute value is Properties, indicates whether a change to this property causes the resource to be recreated
        self.requires_recreation = RequiresRecreation(o["RequiresRecreation"])

        # Not defined by AWS
        self.resource_id = resource_id

    @property
    def node_name(self) -> str:
        # We only have a name when the attribute value is properties
        return (
            self.name
            if self.attribute == Attribute.PROPERTIES
            else self.attribute.value
        )

    @property
    def node_id(self) -> str:
        return "-".join([self.resource_id, self.node_name])

    def node_label(self) -> str:
        return label_table(
            self.node_name, requires_recreation=self.requires_recreation.value
        )

    def render(self, dot: Dot):
        dot.node(
            self.node_id, self.node_label(), shape="record", color=self._pick_color()
        )

    def _pick_color(self):
        if self.requires_recreation == RequiresRecreation.NEVER:
            return "green"
        if self.requires_recreation == RequiresRecreation.CONDITIONALLY:
            return "orange"
        if self.requires_recreation == RequiresRecreation.ALWAYS:
            return "red"
        raise NotImplementedError("unkown value for requires_recreation")


class Attribute(Enum):
    PROPERTIES = "Properties"
    METADATA = "Metadata"
    CREATION_POLICY = "CreationPolicy"
    UPDATE_POLICY = "UpdatePolicy"
    DELETION_POLICY = "DeletionPolicy"
    TAGS = "Tags"


class RequiresRecreation(Enum):
    NEVER = "Never"
    CONDITIONALLY = "Conditionally"
    ALWAYS = "Always"
