from graphviz.dot import Dot

from cloudformation_changeset_graph.utils import label_table


class Template(object):
    def __init__(self, resource_id: str = None):
        if resource_id is None:
            self.node_id = 'Template'
        else:
            self.node_id = f"{resource_id}-Template"

    def render(self, dot:Dot) -> None:
        dot.node(self.node_id, "Template Modification", shape='box')


class Parameter(object):
    def __init__(self, parameter_name: str):
        self.node_id = parameter_name

    def render(self, dot:Dot) -> None:
        dot.node(self.node_id, label_table(self.node_id, type='Parameter'), shape='record')
