import json
import typing

from graphviz import Digraph

from cloudformation.change import Change

def get_example_changes(example: str) -> typing.Sequence[Change]:
    with open(f'examples/{example}.json', 'r') as fh:
        return [Change(x) for x in json.load(fh)['Changes']]


def render_example(example: str) -> None:
    dot = Digraph(f"Change Set {example}", strict=True)
    # changes = get_changes(stack_name, change_set_name)
    changes = get_example_changes(example)
    for change in changes:
        change.render(dot)
    print(dot.source)
    dot.render(f'test-output/{example}', view=True, format='png')
