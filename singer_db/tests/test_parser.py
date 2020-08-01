"""Unit tests for parsing library."""

from singer_db.markdown_table_parser import parse_from_string


MD_TEST = """
# README

## Settings

| Property                            | Type    | Required?  | Description                                                   |
|-------------------------------------|---------|------------|---------------------------------------------------------------|
| aws_access_key_id                   | String  | No         | S3 Access Key Id. If not provided, `AWS_ACCESS_KEY_ID` environment variable will be used. |
| aws_secret_access_key               | String  | No         | S3 Secret Access Key. If not provided, `AWS_SECRET_ACCESS_KEY` environment variable will be used. |
"""


def test_md_table_parse():
    """Test the markdown table parser."""
    tables_list = parse_from_string(MD_TEST)
    assert len(tables_list) == 1
    result = tables_list[0]
    assert result["column_names"] == [
        "Property",
        "Type",
        "Required?",
        "Description",
    ]
    assert len(result["rows"]) == 2
    assert result["breadcrumb"] == ["README", "Settings"]
    print(f"Keys: {result['rows'][0].keys()}")
    assert len(list(result["rows"][0].keys())) == len(result["column_names"])
    assert list(result["rows"][0].keys()) == result["column_names"]
    assert list(result["rows"][1].keys()) == result["column_names"]
    assert list(result["rows"][0].values()) == [
        "aws_access_key_id",
        "String",
        "No",
        "S3 Access Key Id. If not provided, `AWS_ACCESS_KEY_ID` environment variable will be used.",
    ]
    assert list(result["rows"][1].values()) == [
        "aws_secret_access_key",
        "String",
        "No",
        "S3 Secret Access Key. If not provided, `AWS_SECRET_ACCESS_KEY` environment variable will be used.",
    ]
