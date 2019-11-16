import typing
from enum import Enum

from graphviz.dot import Dot

from cloudformation import Template
from cloudformation.resource_target_definition import ResourceTargetDefinition


class ResourceChangeDetail(object):
    """
    For a resource with Modify as the action, the ResourceChange structure describes the changes AWS CloudFormation will make to that resource.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_ResourceChangeDetail.html
    """

    def __init__(self, o: typing.Mapping, resource_id):
        # Strings and Enums
        # If the ChangeSource value is DirectModification, no value is given for CausingEntity.
        self.causing_entity = o.get('CausingEntity')  # type: typing.Optional[str]
        self.change_source = ChangeSource(o['ChangeSource'])
        self.evaluation = Evaluation(o['Evaluation'])
        # Objects
        self.target = ResourceTargetDefinition(o['Target'], resource_id)

        self.resource_id = resource_id

    def render_inside_resource(self, dot: Dot) -> None:
        # draw nodes for the targets
        self.target.render(dot)

    def render_outside_resource(self, dot: Dot):
        if modification_can_be_hidden(self.change_source, self.evaluation):
            return

        if is_template_modification(self.change_source, self.evaluation):
            template_cause = Template(self.resource_id)
            template_cause.render(dot)
            causing_entity = template_cause.node_id
        else:
            causing_entity = self.causing_entity

        dot.edge(causing_entity, self.target.node_id)


class ChangeSource(Enum):
    # Ref intrinsic functions that refer to resources in the template
    RESOURCE_REFERENCE = 'ResourceReference'
    # Ref intrinsic functions that get template parameter values
    PARAMETER_REFERENCE = 'ParameterReference'
    # Fn::GetAtt intrinsic functions that get resource attribute values
    RESOURCE_ATTRIBUTE = 'ResourceAttribute'
    # Changes that are made directly to the template
    DIRECT_MODIFICATION = 'DirectModification'
    # AWS::CloudFormation::Stack resource types (Changes always triggered)
    AUTOMATIC = 'Automatic'


class Evaluation(Enum):
    # CloudFormation can determine that the target value will change, and its value
    STATIC = 'Static'
    # the target value depends on the result of an intrinsic function
    DYNAMIC = 'Dynamic'


def is_template_modification(change_source: ChangeSource, evaluation: Evaluation) -> bool:
    return change_source == ChangeSource.DIRECT_MODIFICATION and evaluation == Evaluation.STATIC


def modification_can_be_hidden(change_source: ChangeSource, evaluation: Evaluation) -> bool:
    return change_source == ChangeSource.DIRECT_MODIFICATION and evaluation == Evaluation.DYNAMIC
