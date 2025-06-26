class DwarfNode:
    def __init__(self, type_, name=None, file=None, line=None):
        self.type = type_
        self.name = name
        self.file = file
        self.line = line
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def to_string(self, level=0):
        indent = '    ' * level
        s = f"{indent}{self.type}"
        if self.name:
            s += f" name={self.name}"
        if self.file:
            s += f" file={self.file}"
        if self.line:
            s += f" line={self.line}"
        s += "\n"
        for child in self.children:
            s += child.to_string(level + 1)
        return s

    def __repr__(self):
        return self.to_string()

class CompileUnitNode(DwarfNode):
    def to_string(self, level=0):
        indent = '    ' * level
        s = "//_______________________________\n"
        s += f"//CompileUnit: {self.name or ''}{{\n"
        for child in self.children:
            s += child.to_string(level + 1)
        s +=  f"//CompileUnit:{self.name or ''}}}\n\n"
        return s

class EnumerationTypeNode(DwarfNode):
    def to_string(self, level=0):
        indent = '    ' * level
        s = f"{indent}enum {self.name or ''} {{\n"
        for child in self.children:
            s += child.to_string(level + 1)
        s +=  f"{indent}}};\n"
        return s

class EnumeratorNode(DwarfNode):
    def to_string(self, level=0):
        indent = '    ' * level
        s = f"{indent}{self.name or ''}"
        const_val = getattr(self, "const_value", None)
        if const_val is not None:
            s += f" = {const_val}"
        s += ",\n"
        return s

class TypedefNode(DwarfNode):
    def to_string(self, level=0):
        indent = '    ' * level
        s = f"{indent}typedef {self.name or ''};\n"
        for child in self.children:
            s += child.to_string(level + 1)
        return s

class StructureTypeNode(DwarfNode):
    def to_string(self, level=0):
        indent = '    ' * level
        s = f"{indent}struct {self.name or ''} {{\n"
        for child in self.children:
            s += child.to_string(level + 1)
        s += f"{indent}}};\n"
        return s

class MemberNode(DwarfNode):
    def to_string(self, level=0):
        indent = '    ' * level
        s = f"{indent}"
        type_name = getattr(self, "type_name", None)
        if type_name:
            s += f"{type_name} "
        if self.name:
            s += f"{self.name}"
        s += ";\n"
        return s

class BaseTypeNode(DwarfNode):
    def to_string(self, level=0):
        indent = '    ' * level
        s = f"{indent}// base_type: {self.name or ''}\n"
        return s