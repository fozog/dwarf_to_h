import re
from dwarf_model import DwarfEntry

def parse_dwarfdump(filename):
    entry_re = re.compile(r'^(0x[0-9a-f]+):(\s*)(DW_TAG_[\w_]+)')
    attr_re = re.compile(r'^\s+(DW_AT_[\w_]+)\s+\((.*)\)')
    null_re = re.compile(r'^(0x[0-9a-f]+):(\s*)NULL')

    stack = []
    root = None

    with open(filename, 'r') as f:
        for line in f:
            m_entry = entry_re.match(line)
            m_null = null_re.match(line)
            m_attr = attr_re.match(line)

            if m_entry:
                offset, spaces, tag = m_entry.groups()
                indent = len(spaces)
                entry = DwarfEntry(offset, tag, indent)
                # Trouver le parent selon l'indentation
                while stack and stack[-1].indent >= indent:
                    stack.pop()
                if stack:
                    stack[-1].add_child(entry)
                else:
                    root = entry
                stack.append(entry)
            elif m_null:
                _, spaces = m_null.groups()
                indent = len(spaces)
                # Fermer la branche courante
                while stack and stack[-1].indent >= indent:
                    stack.pop()
            elif m_attr and stack:
                name, value = m_attr.groups()
                stack[-1].add_attribute(name, value)
    return root

if __name__ == "__main__":
    root = parse_dwarfdump("dwarf.txt")
    print(root)