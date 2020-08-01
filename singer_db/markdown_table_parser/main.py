"""A simple markdown table parser.

Recommended usage:

```py
from markdown_table_parser import parse_from_file
markdown_tables = parse_from_file("https://raw.githubusercontent.com/transferwise/pipelinewise-target-s3-csv/master/README.md")
print(markdown_tables)
```

Which is identical to:

```py
from uio import get_text_file_contents
from markdown_table_parser import parse_from_string

markdown_text = uio.get_text_file_contents("https://raw.githubusercontent.com/transferwise/pipelinewise-target-s3-csv/master/README.md")
markdown_tables = parse_from_string(markdown_text)
print(markdown_tables)
```

Either approach will produce this output:

```
[
    {
        column_names: [ "Property", "Type", "Required?", "Description" ]
        rows: [
            {
                "Property": "aws_access_key_id",
                "Type", "String",
                "Required?", "No",
                "Description", "S3 Access Key Id. If not provided, `AWS_ACCESS_KEY_ID` environment variable will be used."
            },
            ...
        ]
        breadbrumb: ["pipelinewise-target-s3-csv", "Install", "Non-Profile based authentication"]
    }
]
```
"""

import re
from typing import List, Dict, Tuple

import uio

RE_FLAGS = re.RegexFlag.IGNORECASE | re.RegexFlag.MULTILINE

# Based on: https://stackoverflow.com/a/54771485/4298208
RE_MD_TABLE_PATTERN = (
    r"^(\|[^\n]+\|\r?\n)((?:\|:?[-]+:?)+\|)(\n(?:\|[^\n]+\|\r?\n?)*)?$"
)
RE_MD_TABLE_ROWS_PATTERN = r""
RE_MD_TABLE_KEYS_PATTERN = r""


def parse_from_file(filepath: str, /) -> List[Dict[str, List]]:
    return parse_from_string(uio.get_text_file_contents(filepath))


def parse_from_string(markdown_text: str, /) -> List[Dict[str, List]]:
    result: List[Dict[str, List]] = []
    for breadcrumb, text in _split_md_sections(markdown_text):
        result += _parse_md_tables(text, breadcrumb=breadcrumb)
    return result


def _split_md_sections(md_text: str) -> List[Tuple[List[str], str]]:
    """Return a mapping of section breadbrumbs to the text within each section."""
    sections: List[Tuple[List[str], str]] = []
    current_section_breadcrumb: List[str] = []
    current_section_text = ""
    for line in md_text.splitlines():
        num_hashes = _num_starting_hashes(line)
        if not num_hashes:
            # Continuing previous section
            current_section_text += f"{line}\n"
            continue
        if [l for l in current_section_text.splitlines() if l.strip()]:
            # Add section text if non-blank contents
            sections.append((current_section_breadcrumb, current_section_text))
        # Reset section text:
        current_section_text = ""
        while num_hashes <= len(current_section_breadcrumb):
            # Pop trailing breadcrump parts:
            current_section_breadcrumb.pop()
        while num_hashes - 1 > len(current_section_breadcrumb):
            # If skipping levels, insert blanks into breadcrump:
            current_section_breadcrumb.append("")
        current_section_breadcrumb.append(line[num_hashes:].strip())
    if current_section_text:
        sections.append((current_section_breadcrumb, current_section_text))
    return sections


def _num_starting_hashes(line: str) -> int:
    """Return the number of hashes (#) at the beginning of the line."""
    if not line:
        return 0
    for n, char in enumerate(line, start=0):
        if char != "#":
            return n
    return len(line)


def _parse_md_tables(md_text: str, breadcrumb: List[str]) -> List[Dict[str, List]]:
    """Return a list of dictionaries with keys `column_names`, `rows`, and `breadcrumb`."""
    result: List[Dict[str, List]] = []
    matches = re.finditer(RE_MD_TABLE_PATTERN, md_text, RE_FLAGS)
    match: re.Match
    for match_num, match in enumerate(matches, start=1):
        print(
            f"Match {match_num} was found at {match.start()}-{match.end()}: {match.group()}"
        )
        result.append(_parse_md_table(match.group(), breadcrumb))
    return result


def _parse_md_table(md_text: str, breadcrumb: List[str]) -> Dict[str, List]:
    """Return a dictionary with keys `column_names`, `rows`, and `breadcrumb`."""
    matches = list(re.finditer(RE_MD_TABLE_PATTERN, md_text, RE_FLAGS))
    match: re.Match
    if len(matches) != 1:
        raise ValueError(f"String is not a valid markdown table: {md_text}")
    match = matches[0]
    print(f"Match was found at {match.start()}-{match.end()}: {match.group()}")
    for group_num in range(0, len(match.groups())):
        print(
            f"Group {group_num} found at "
            f"{match.start(group_num)}-{match.end(group_num)}: "
            f"{match.group(group_num)}"
        )
    keys = _parse_md_table_header(match.group(1))
    rows = _parse_md_table_rows(match.group(3), keys=keys)
    return {
        "column_names": keys,
        "rows": rows,
        "breadcrumb": breadcrumb,
    }


def _parse_md_table_header(md_table_header: str) -> List[str]:
    """Return a list of column names."""
    return [key.strip() for key in md_table_header.strip().split("|") if key]


def _parse_md_table_rows(
    md_table_rows_text: str, keys: List[str]
) -> List[Dict[str, str]]:
    """Return a list of row dictionaries."""
    print(f"Attempting to parse rows: ```\n{md_table_rows_text}\n```")
    result: List[Dict[str, str]] = []
    rows_raw: List[str] = []
    for line in md_table_rows_text.splitlines():
        # if line and line[0] == "|":
        rows_raw.append(line)
        # elif line:
        #     rows_raw[len(rows_raw) - 1] += line
    for row_text in rows_raw:
        if row_text.strip():
            cells = [c.strip() for c in row_text.split("|")[1:-1]]
            if len(cells) != len(keys):
                raise ValueError(
                    f"Number of parsed cells ({len(cells)}) did not match "
                    f"the number of columns ({len(keys)}): `{row_text}`"
                )
            row: Dict[str, str] = {}
            for i, key in enumerate(keys, start=0):
                row[key] = cells[i]
            result.append(row)
    return result
