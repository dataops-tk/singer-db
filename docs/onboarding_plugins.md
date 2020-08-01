# Plugin Onboarding Guide

_This guide will walk you through the process of registering a new plugin on Singer DB._

## Step 1: Update the Plugin Index

The plugin index is designed to hold the bare-minimum set of metadata in order to install
the plugin and auto-detect any remaining additional settings.

For example:

```yml
taps:
  adwords:
    about_url: https://ads.google.com
    forks:
    - owner: singer-io
      repo: https://github.com/singer-io/tap-adwords
      pip: tap-adwords
      default: true
    # ...
```

- Each plugin has a name _(`adwords` in the above example)_ which should match the
  `tap-{myname}` convention.
- Each plugin has an `about_url` link which provides more information on the specific
  source being extracted from.
- _Optionally,_ plugins can also have an `icon_url` link which points to an icon that is
  representative of the branding for the source system.
- Each plugin has one or more `forks`:
  - Each fork has an `owner`. This should be **exactly** the lowercase organization or user
    name from the git URL.
  - Each fork has a `repo` URL, which should point to the repository on some git host,
    such as github, gitlab, etc.
  - Each fork can have one of the below, but not both:
    - `pip` - a PyPi package name or any other reference that pip understands. The text
      `git` can be supplied to automatically use the latest from the git default branch.
    - `docker` - the name of a Dockerfile or docker image. If supplying a Dockerfile, the
      value should contain the text `Dockerfile` (e.g. `tap-mssql.Dockerfile`).
  - One (and only one) fork for each plugin can be flagged as `default: true`. This will
    be the default fork provided to users when they do not specify a preferred fork.

## Step 2: Test Auto-Generated Discovery Yaml

After registering the plugin in `taps-index.yml` or `targets-index.yml`, the next step is
to run the auto-discovery process.

> :warning: This part isn't built yet, so consider this a draft spec.

```bash
# Change to the repo root:
cd singer-db
python -m singer_db run_discovery --plugin_name=tap-mytap
```

If all goes well, you will see a new auto-generated file:
`taps/tap-{mytap}@{myname}.yml` or `target/target-{mytarget}@{myname}.yml`.

## Step 3: Update Documentation as Needed or Create a Discovery Override File

After reviewing the auto-generated file, if you are not satisfied with the output, you
have a view options.

Since the definitions in the `taps` and `targets` folders will be regularly auto-updated,
please _do not_ make any manual updates to the files created there.

Instead, you can follow one of these three methods:

1. Follow the [README.md Style Guide](./readme_styleguide.md) for information on how to
   improve auto-discovery by updating the fork's documentation.
2. Create your own discovery.yml file in the fork itself. This will replace the
   auto-discovery process with the values you've provided explicitly there in the repo.
3. If you do not have access to the repo, create a Discovery Yaml file in the
   [tap](../taps/overrides) or [target](../targets/overrides) **overrides** folders. Any
   overrides provided will replace the values otherwise detected automatically.

After completing one or more of the following, rerun **Step 2** from above and repeat the
process until you are fully satisfied that the output if accurate and complete.
