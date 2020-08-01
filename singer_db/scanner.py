"""Scans Singer plugin repo and attempts to automatically update the yaml file."""

from typing import Dict, List, Any

from singer_db.markdown_table_parser import parse_from_file

EXPECTED_COLS = {
    "setting": "name",
    "property": "name",
    "type": None,
    "required": None,
    "description": None,
}


def scan_plugin_readme(filepath) -> Dict[str, Any]:
    md_tables = parse_from_file(filepath)
    settings_list: List[Dict[str, Any]] = []
    for md_table in md_tables:
        if _is_singer_settings_table(md_table):
            settings_list += _standardize(md_table["rows"])
    return {"settings": settings_list}


def _is_singer_settings_table(md_table: Dict[str, List]) -> bool:
    keys = [k.lower().replace("?", "") for k in md_table["column_names"]]
    return any([expected in keys for expected in EXPECTED_COLS.keys()])


def _standardize(settings_rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    output_rows: List[Dict[str, str]] = []
    for input_row in settings_rows:
        output_row: Dict[str, str] = {}
        for key, value in input_row.items():
            cleaned_key = key.lower().replace("?", "")
            if cleaned_key not in EXPECTED_COLS:
                output_row[f"_{cleaned_key}"] = value
            else:
                output_row[EXPECTED_COLS[cleaned_key] or cleaned_key] = value
        output_rows.append(output_row)
    return output_rows
