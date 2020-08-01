# Singer Docker Images

This folder contains definitions to build the docker images as `dataopstk/singer`.

## Usage Examples

Install the helper library:

```bash
pip3 install singer-db
```

Build one or more docker images:

```bash
singer-db build_image csv           # Builds `dataopstk/singer:tap-csv`
singer-db build_image csv --push    # Builds and pushes `dataopstk/singer:tap-csv`
singer-db build_image csv redshift  # Builds `dataopstk/singer:csv-to-redshift`
singer-db build_all_images --push   # Builds and pushes everything in the index
```
