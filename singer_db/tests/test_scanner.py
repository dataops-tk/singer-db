"""Unit tests for scanner."""

from singer_db.scanner import scan_plugin_readme

README_PATH = "./singer_db/tests/resources/sample-tap.README.md"
EXPECTED_SETTINGS_LIST = [
    "aws_access_key_id",
    "aws_secret_access_key",
    "aws_session_token",
    "aws_profile",
    "s3_bucket",
    "s3_key_prefix",
    "delimiter",
    "quotechar",
    "add_metadata_columns",
    "encryption_type",
    "encryption_key",
    "compression",
    "naming_convention",
]


def test_scanner():
    """Test the README scanner."""
    result = scan_plugin_readme(README_PATH)
    print(result)
    settings = result["settings"]
    assert len(settings) == len(EXPECTED_SETTINGS_LIST)
    settings_dict = {s["name"]: s for s in settings}
    settings_list = list(settings_dict.keys())
    assert sorted(settings_list) == sorted(EXPECTED_SETTINGS_LIST)
    required_settings_list = [
        v["name"]
        for v in settings
        if v["required"].lower() in ["yes", "true", "y", "t"]
    ]
    assert sorted(required_settings_list) == sorted(["s3_bucket"])
    assert settings_dict["add_metadata_columns"]["type"].lower() == "boolean"
    assert settings_dict["s3_bucket"]["description"] == "S3 Bucket name"
