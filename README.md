# Singer DB

A curated index of Singer.io taps and targets.

## Explore

- Installation Info:
  - [taps-index.yml](./taps-index.yml)
  - [targets-index.yml](./targets-index.yml)
  - [transforms-index.yml](./transforms-index.yml)
- Config Info:
  - [taps](./taps)
  - [targets](./targets)
  - [transforms](./transforms)

## Why Singer DB?

Singer DB is an experiment in saving community members time and frustration. When searching
for new taps, there are three common hurtles we wanted to address with Singer DB:

1. **Curating the "best" forks for each source or target.** Who has time to try out
   multiple copies of the same taps?
2. **Improved documentation of plugin options.** When onboarding new taps, the first hurtle
   is to discover which settings are required in order to get the tap up and running.
   Singer DB auto-scrapes config settings from the repos themselves and creates a reference
   file that is both human- and machine-readable.
3. **Dockerization made easy.** We automatically build and publish Docker images for each
   and every plugin in Singer DB, as well as building a `tap-to-target` Docker image for
   every *combination* of source and destination. This means you can get started quickly
   and painlessly run taps in test or production.

## How Can I Help?

We are asking for help from community members in one of 3 ways:

1. Register new taps -
2. Report taps that aren't working - Help us instill trust in working taps and targets by
   reporting those which aren't working.
3. Expand documentation - Read our markdown docs styleguide for information on how to
   ensure settings are automatically parsed.
