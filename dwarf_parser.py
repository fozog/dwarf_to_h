import re
from dwarf_model import DwarfEntry
from dwarf_objects import DwarfNode, CompileUnitNode, EnumerationTypeNode, EnumeratorNode, TypedefNode, StructureTypeNode, MemberNode, BaseTypeNode

def parse_dwarfdump(filename):
    entry_re = re.compile(r'^(0x[0-9a-f]+):\s(\s*)(DW_TAG_[\w_]+)')
    attr_re = re.compile(r'^\s+(DW_AT_[\w_]+)\s+\((.*)\)')
    null_re = re.compile(r'^(0x[0-9a-f]+):\s(\s*)NULL')

    stack = []
    root = DwarfEntry(0, "root", -1)

    last = root

    with open(filename, 'r') as f:
        for line in f:
            m_entry = entry_re.match(line)
            m_null = null_re.match(line)
            m_attr = attr_re.match(line)

            if m_entry:
                offset, spaces, tag = m_entry.groups()
                indent = len(spaces)
                entry = DwarfEntry(offset, tag, indent)
                
                if last.indent < indent:
                    stack.append(last)  # The last one becomes a parent
                
                stack[-1].add_child(entry) # ajoute l'entrée comme enfant du parent actuel
                
                last = entry

            elif m_null:
                _, spaces = m_null.groups()
                indent = len(spaces)
                last = stack[-1]
                stack.pop()  # Enlève le parent
            elif m_attr and stack:
                name, value = m_attr.groups()
                # Pour DW_AT_type, ne garder que la partie entre guillemets s'il y en a
                if name == "DW_AT_type":
                    if '"' in value:
                        value = value.split('"')[1]
                    else:
                        value = None  # ou value = value si tu veux garder l'offset brut
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                last.add_attribute(name, value)
    return root

def dwarfentry_to_object(entry):
    if entry.tag == "root":
        node = DwarfNode(type_="", name="root")
    elif entry.tag == "DW_TAG_compile_unit":
        node = CompileUnitNode(
            name=entry.attributes.get("DW_AT_name"),
            file=entry.attributes.get("DW_AT_decl_file"),
            line=entry.attributes.get("DW_AT_decl_line"),
            type_=entry.tag
        )
    elif entry.tag == "DW_TAG_enumeration_type":
        node = EnumerationTypeNode(
            name=entry.attributes.get("DW_AT_name"),
            file=entry.attributes.get("DW_AT_decl_file"),
            line=entry.attributes.get("DW_AT_decl_line"),
            type_=entry.tag
        )
    elif entry.tag == "DW_TAG_enumerator":
        node = EnumeratorNode(
            name=entry.attributes.get("DW_AT_name"),
            type_=entry.tag
        )
        const_val = entry.attributes.get("DW_AT_const_value")
        if const_val is not None:
            node.const_value = const_val
    elif entry.tag == "DW_TAG_typedef":
        node = TypedefNode(
            name=entry.attributes.get("DW_AT_name"),
            type_=entry.tag
        )
    elif entry.tag == "DW_TAG_structure_type":
        node = StructureTypeNode(
            name=entry.attributes.get("DW_AT_name"),
            type_=entry.tag
        )
    elif entry.tag == "DW_TAG_member":
        node = MemberNode(
            name=entry.attributes.get("DW_AT_name"),
            type_=entry.tag
        )
        type_name = entry.attributes.get("DW_AT_type")
        if type_name is not None:
            node.type_name = type_name
    elif entry.tag == "DW_TAG_base_type":
        node = BaseTypeNode(
            name=entry.attributes.get("DW_AT_name"),
            type_=entry.tag
        )
    else:
        node = DwarfNode(type_=entry.tag)
    for child in entry.children:
        child_obj = dwarfentry_to_object(child)
        if child_obj:
            node.add_child(child_obj)
    return node

if __name__ == "__main__":
    root = parse_dwarfdump("dwarf2.txt")
    obj_tree = dwarfentry_to_object(root)
    print(obj_tree.to_string())