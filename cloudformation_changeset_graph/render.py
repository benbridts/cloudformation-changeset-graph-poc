import json

from graphviz import Digraph  # type: ignore

from cloudformation.describe_change_set_response import DescribeChangeSetResponse


def get_example_change_set(example: str) -> DescribeChangeSetResponse:
    with open(f"examples/{example}.json", "r") as fh:
        return DescribeChangeSetResponse(json.load(fh))


def render(change_set: DescribeChangeSetResponse, base_name: str) -> None:
    dot = Digraph(
        f"Graph for {change_set.change_set_name} on {change_set.stack_name}",
        strict=True,
    )
    change_set.render(dot)
    print(dot.source)
    dot.render(base_name, view=True, format="png")


def render_example(example: str) -> None:
    change_set = get_example_change_set(example)
    render(change_set, f"test-output/{example}")
