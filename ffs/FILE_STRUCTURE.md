# File system structure

The proposed structure for data on the file system is inspired by [Spreckelsen et. al 2020][1], but more flexible.
The intention is to provide a structure which is more easily navigable by both humans and computers, with structured metadata and clear documentation about each dataset, while still allowing the flexibility to encompass existing analysis pipelines.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Entries

An entry is a directory on the file system which contains metadata files described below.
Entries MAY contain other entries (child entries).
Entries MAY contain non-entry directories, which MUST be specified using the `ignore` metadata field:
users SHOULD minimise the number of entries which contain both entry and non-entry subdirectories.

Entries are discovered by searching recursively down from a root entry.
Directories which are not valid entries will not be recursed through.

## Metadata

Every entry MUST contain two entry metadata files in it.

### README.md

The `README.md` MUST be a plain text ([UTF-8](https://en.wikipedia.org/wiki/UTF-8)) file with a medium to long description of the entry, in [markdown](https://commonmark.org/help/) format (allowing light formatting which can easily be understood in plain text or rendered into something prettier).
Specifically, this is should follow Commonmark (as per the link above) with the [Github Flavoured Markdown tables extension](https://github.github.com/gfm/#tables-extension-)): however, it is RECOMMENDED that complex tables go in a different file.

It SHOULD contain relevant references, motivations, and project goals.
Primarily, it SHOULD allow a qualified but unfamiliar observer to understand what the entry *is* at a glance.

Such a file MAY look like

```markdown
# My project

This project investigates how common a particular phenomenon is in the world.
There are many such phenomena but some evidence (see `./preliminary-results/` directory) suggests that this is the important one.

You might *think* that it's not that important, but it **really** is.

See [wikipedia][1] for related literature.

[1]: https://en.wikipedia.org/
```

### METADATA.yaml

The `METADATA.yaml` MUST be plain text ([UTF-8](https://en.wikipedia.org/wiki/UTF-8)) structured data file in [YAML](https://en.wikipedia.org/wiki/YAML) format (specifically the much simpler subset [StrictYAML](https://hitchdev.com/strictyaml/)), which is easy for both humans and machines to read and write.
It supports nestable maps (looking up a key to get a value associated with it), sequences of similar/related items, and scalars (numbers/ strings of letters).

At a minimum, an entry MUST have two keys: `responsible` (which MUST be a sequence of one or more people associated with the entry, who MUST be given in an unambiguous format e.g. including an email address) and `description` (which MUST be a one-sentence gist of the project, expanded upon in the `README.md`).
Such a minimal file MAY look like:

```yaml
responsible:
- John Smith <jsmith@mrc-lmb.cam.ac.uk>
- Jane Doe <jd619@cam.ac.uk>
description: Determine optimal parameters for keeping neuroscience fun
```

Other common fields MAY include:

- `ignore`: a list of non-entry subdirectories, as glob patterns (see below)
- `sources`: a list of entries which this entry depends on, as paths (e.g. raw data which an analysis is based on)
- `revisionOf`: if an entry is a fixed/updated version of a previously-created entry
- `results`: a list of the key outputs of this entry, as maps with keys `file` (path or [glob pattern](https://en.wikipedia.org/wiki/Glob_(programming))) and `description` (what these results represent)
- `scripts`: the entry point of a particular simulation run/ analysis pipeline, as a map with the keys `file` (a path) and `description` (what that script does, briefly)

A metadata file including all of these MAY look like

```yaml
responsible:
- John Smith <jsmith@mrc-lmb.cam.ac.uk>
- Jane Doe <jd619@cam.ac.uk>
description: Determine optimal parameters for keeping neuroscience fun
ignore: *
sources:
- ../../2020_brain-stimulation-raw
revisionOf: ../2020_brain-stimulation-analysis
results:
- file: results/traces/subject-*.csv
  description: EMG traces from all participants
- file: results/faces/*/*.tif
  description: videos of participants' faces
scripts:
- file: scripts/warmup.py
  description: protocol to get subjects used to the experimental setup
- file: scripts/experiment.sh
  description: run the full experiment for a single subject
```

Further fields and examples are described in [Spreckelsen][1].

Additional fields which may be valuable for us include:

- IDs of experimental rigs, protocol versions, microscopes
- links to git repositories/ specific revisions for source code used to generate data
- references for a paper where a particular dataset or pipeline is authoritatively described ("inspiration" papers should be kept in the README)

Broadly speaking, if you can think of a reason that different entries may have the same information represented, and it may be necessary for a computer to query that information, it SHOULD go into the `METADATA.yaml`.

#### `ignore`

Entries which contain non-entry directories MUST specify those directories using the `ignore` field, which MUST be either a string or a sequence of strings.
Many directories can be specified at once using case-sensitive [glob syntax](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax).

For example,

```yaml
ignore: *
```

specifies that all subdirectories are non-entries (i.e. this is a leaf entry).

A more complex selection MAY look like

```yaml
ignore:
- *_tmp
- ????-??_experiment
- [abc][!def]*
```

## Differences from Spreckelsen et. al

- Type and purpose of entry are completely freeform, without the category/project/experiment structure
- `kebab-case` entry names SHOULD be preferred over `UpperCamel`
- Split project/ experiment long description and structured metadata into separate files (`README.md` and `METADATA.yaml`)

## Open questions

- How do we handle cross-filesystem references (e.g. references between `zstore1` and `ark`)?
- Are there any other metadata fields to standardise?
    - e.g. rig designation

[1]: https://www.mdpi.com/2306-5729/5/2/43/htm
