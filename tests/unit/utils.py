def yaml_indent(yaml_string: str, levels: int = 1, tabsize: int = 2) -> str:
    space_length: int = levels * tabsize
    space_string: str = " " * space_length
    indented_string: str = ""
    for line in yaml_string.splitlines(keepends=True):
        indented_string = indented_string + space_string + line

    return indented_string
