import re

def write_between_tags(text: str, id: str, tag: str, file_name: str):
    """In the identified text file, write the input text between tags that look like the following.
    <*tag* id="*id*">
    ...
    </*tag*>
    Note that this must match exactly, otherwise it will not work.
    The goal is to make it only match a very limited portion of the document.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        file_text = f.read()
    text = "\n\n" + text + "\n\n"
    pattern = fr'(?<=<{tag} id="{id}">).+?(?=</{tag}>)'
    substitution, n = re.subn(pattern, text, file_text, 0, re.DOTALL)
    if n != 0:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(substitution)