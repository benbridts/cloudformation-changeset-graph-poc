import typing

from graphviz.dot import Dot

from utils import label_table


class Parameter(object):
    """
    The Parameter data type.
    https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_Parameter.html
    """

    def __init__(self, o: typing.Mapping):
        self.parameter_key = o["ParameterKey"]  # type: str
        self.parameter_value = o["ParameterValue"]  # type: str
        self.resolved_value = o.get("ResolvedValue")  # type: typing.Optional[str]
        self.use_previous_value = o.get(
            "UsePreviousValue"
        )  # type: typing.Optional[bool]

    @property
    def node_id(self) -> str:
        return self.parameter_key

    def render(self, dot: Dot) -> None:
        if self.use_previous_value:
            # this should not happen, previous value does not trigger a change
            raise Exception(
                f"Parameter {self.parameter_value} with UsePreviousValue found"
            )

        value = self.parameter_value
        if self.resolved_value:
            value += f" ==> {self.resolved_value}"
        label = label_table(self.parameter_key, type="Parameter", value=value,)
        dot.node(self.node_id, label, shape="record")
