# README.md Style Guide

This guide will walk you through the best practices for creating docs that can be
automatically parsed into Singer DB documentation.

## Option A: Markdown Tables

Any markdown tables will be automatically parsed and scanned for one or more of the
following column names:

- Setting Names:
  - `Setting`
  - `Settings`
  - `Property`
  - `Properties`
- Description:
  - `Description`
- Required Flag:
  - `Required`
  - `Required?`
- Type:
  - `Type`
  - `Data Type`

### Example Table Markdown:

```
| Property                | Type    | Required?  | Description                                                   |
|-------------------------|---------|------------|---------------------------------------------------------------|
| aws_access_key_id       | String  | No         | S3 Access Key Id. If not provided, `AWS_ACCESS_KEY_ID` environment variable will be used. |
| aws_secret_access_key   | String  | No         | S3 Secret Access Key. If not provided, `AWS_SECRET_ACCESS_KEY` environment variable will be used. |
```

Which renders as:

---

| Property                | Type    | Required?  | Description                                                   |
|-------------------------|---------|------------|---------------------------------------------------------------|
| aws_access_key_id       | String  | No         | S3 Access Key Id. If not provided, `AWS_ACCESS_KEY_ID` environment variable will be used. |
| aws_secret_access_key   | String  | No         | S3 Secret Access Key. If not provided, `AWS_SECRET_ACCESS_KEY` environment variable will be used. |

---

## Option B: Bulleted Lists

If a markdown table is not found, Singer DB will then scan for a bulleted list of settings.

- The bulleted list must be within a markdown section that contains one of the words:
  `Setting`, `Settings`, `Config`, or `Configuration`.
- The exact text `Optional.` or `Required.` within any bullet will be used to populate
  metadata on whether the setting is optional or required. If no such setting can be
  detected, the `Required Flag` will be left null.
- The setting name itself must be either **bolded** or `monospaced`.
- Anything after the setting name will be captured as a text description.

### Example Bulleted List:

---

### Sample configuration settings:

- **aws_access_key_id** - (Optional.) - The S3 Access Key ID. If not provided, the
  `AWS_ACCESS_KEY_ID` environment variable will be used.
- **aws_secret_access_key** - (Optional.) - The S3 Secret Access Key. If not provided, the
  `AWS_SECRET_ACCESS_KEY` environment variable will be used.

---

## Option C: Use a `discovery.yml` File Instead of Markdown

For a more explicit approach that is both human-readable and machine-readable, we recommend
creating your own `discovery.yml` file and storing this in your own repo.
