class DwarfEntry:
    def __init__(self, offset, tag, indent):
        self.offset = offset
        self.tag = tag
        self.indent = indent
        self.attributes = {}
        self.children = []

    def add_attribute(self, name, value):
        self.attributes[name] = value

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        indent = '  ' * level
        s = f"{indent}{self.offset}: {self.tag}\n"
        for k, v in self.attributes.items():
            s += f"{indent}  {k}: {v}\n"
        for child in self.children:
            s += child.__repr__(level + 1)
        return s