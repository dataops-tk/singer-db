"""A simple markdown table parser."""

from singer_db.markdown_table_parser.main import parse_from_string, parse_from_file

__all__ = [parse_from_string, parse_from_file]
