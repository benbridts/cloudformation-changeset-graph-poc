import json
import typing

from graphviz import Digraph

from cloudformation.describe_change_set_response import DescribeChangeSetResponse

def get_example_change_set(example: str) -> DescribeChangeSetResponse:
    with open(f'examples/{example}.json', 'r') as fh:
        return DescribeChangeSetResponse(json.load(fh))


def render_example(example: str) -> None:
    dot = Digraph(f"Change Set {example}", strict=True)
    change_set = get_example_change_set(example)
    change_set.render(dot)

    print(dot.source)
    dot.render(f'test-output/{example}', view=True, format='png')
