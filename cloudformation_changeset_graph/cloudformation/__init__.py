from graphviz.dot import Dot


class Template(object):
    def __init__(self, resource_id: str = None):
        if resource_id is None:
            self.node_id = "Template"
        else:
            self.node_id = f"{resource_id}-Template"

    def render(self, dot: Dot) -> None:
        dot.node(self.node_id, "Template Modification", shape="box")
