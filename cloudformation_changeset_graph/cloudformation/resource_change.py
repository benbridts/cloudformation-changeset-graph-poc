import typing
from enum import Enum

from graphviz.dot import Dot, Digraph
from cloudformation.resource_change_detail import ResourceChangeDetail
from utils import label_table


class ResourceChange(object):
    """
    The ResourceChange structure describes the resource and the action that AWS CloudFormation will perform on it if you execute this change set.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_ResourceChange.html
    """

    def __init__(self, o: typing.Mapping):
        # Strings and Enums
        self.action = Action(o['Action'])
        self.logical_resource_id = o['LogicalResourceId']  # type: str
        self.physical_resource_id = o.get('PhysicalResourceId')  # type: typing.Optional[str]
        self.replacement = Replacement(
            o['Replacement']) if 'Replacement' in o else None  # type: typing.Optional[Replacement]
        self.resource_type = o['ResourceType']  # type: str
        self.scope = [Scope(x) for x in o['Scope']]

        # Objects
        self.details = [ResourceChangeDetail(x, self.logical_resource_id) for x in o['Details']]

    def render(self, dot:Dot) -> None:
        # the name must begin with cluster, for the subgraph to work
        name = f"cluster{self.logical_resource_id}"
        label_properties = dict(
            resource_type=self.resource_type,
            action=self.action.value,
        )
        if self.replacement:
            label_properties['replacement'] = self.replacement.value

        resource_attr = dict(
            label=label_table(self.logical_resource_id, **label_properties),
            labelloc='b',  # bottom
            color=self._pick_color(),
        )

        if self.action == Action.MODIFY:
            subgraph = Digraph(name=name, graph_attr=resource_attr)
            for detail in self.details:
                detail.render_inside_resource(subgraph)
                detail.render_outside_resource(dot)
            dot.subgraph(graph=subgraph)
        else:
            dot.node(name, **resource_attr, shape='record')

    def _pick_color(self):
        if self.action == Action.ADD:
            return 'green'
        if self.action == Action.REMOVE:
            return 'red'
        if self.action == Action.IMPORT:
            return 'blue'
        if self.action == Action.MODIFY:
            if self.replacement == Replacement.FALSE:
                return 'green'
            if self.replacement == Replacement.CONDITIONAL:
                return 'orange'
            if self.replacement == Replacement.TRUE:
                return 'red'

        raise NotImplementedError('unkown value for Replacement')


class Action(Enum):
    ADD = 'Add'
    MODIFY = 'Modify'
    REMOVE = 'Remove'
    IMPORT = 'Import'


class Replacement(Enum):
    TRUE = 'True'
    FALSE = 'False'
    CONDITIONAL = 'Conditional'


class Scope(Enum):
    PROPERTIES = 'Properties'
    METADATA = 'Metadata'
    CREATION_POLICY = 'CreationPolicy'
    UPDATE_POLICY = 'UpdatePolicy'
    DELETION_POLICY = 'DeletionPolicy'
    TAGS = 'Tags'
