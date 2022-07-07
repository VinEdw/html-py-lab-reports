import re

def write_between_markers(html_str: str, mark_name: str, file_name: str) -> bool:
    """
    In the html text file identified with the input name, write the *html_str* between the "markers".
    The markers look like the following:
    <!-- start mark_name -->
    ...
    <!-- end mark_name -->
    They should be on separate lines, can have arbitrary content in between, and can have whitespace indentation at the start.
    That indentation will be used when inserting the *html_str*.
    The intent is to make it only match, and thereby impact, a very limited portion of the document.
    The function return True if the replacement succeeds, and False if the markers cannot be found or are not closed.
    The replacement was not made if False is returned.
    """
    start_marker = f"<!-- start {mark_name} -->"
    end_marker = f"<!-- end {mark_name} -->"
    inside_markers = False
    split_html_str = html_str.split("\n")
    new_full_html = ""
    # html_list = [item for item in html_str.split("\n")]
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            if not inside_markers:
                new_full_html += line
                if line.strip() == start_marker:
                    inside_markers = True
                    indentation = line[:(len(line)-len(line.lstrip()))]
                    for item in split_html_str:
                        new_full_html += indentation + item + "\n"
            else:
                if line.strip() == end_marker:
                    new_full_html += line
                    inside_markers = False
    if inside_markers:
        return False
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(new_full_html)
    return True
