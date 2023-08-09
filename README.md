# ffs

Python tools for querying a Flexible File Structure as specified in <https://gitlab.com/cardonazlaticlabs/data-policy>

The name of the PyPI package is `flexfs` to avoid naming collisions with the unrelated [`ffs`](https://pypi.org/project/ffs/) project.
The import and CLI name is `ffs`.

## Usage

The entry point is a command line tool called `ffs` with a number of subcommands:

```_main
Usage: ffs [OPTIONS] COMMAND [ARGS]...

  Command line tool for working with a Flexible File Structure.

Options:
  --version      Show the version and exit.
  -v, --verbose  Increase logging verbosity.
  --help         Show this message and exit.

Commands:
  book      Export the FFS metadata into files for mdbook.
  create    Create a new FFS entry.
  export    Read the FFS and its metadata into JSON.
  problems  List problems with the structure of the FFS.
```

### Create

```_create
Usage: ffs create [OPTIONS] NAME [DIRECTORY]

  Create a new FFS entry.

Options:
  -d, --description TEXT          Description of the entry (interactive if not
                                  given)
  -r, --responsible PARSEADDR     Email address of person responsible for this
                                  entry. Several may be given; interactive if
                                  none given.
  -D, --date-resolution [year|y|month|m|day|d]
                                  Smallest unit to show in date prefix of
                                  entry name (default month).
  -t, --today FROMISOFORMAT       ISO-8601 date (YYYY-MM-DD) to assign to
                                  entry (default today)
  -l, --leaf                      Ignore all subdirectories
  -R, --root                      Do not check that parent is an entry which
                                  does not ignore the new entry.
  --help                          Show this message and exit.
```

### Export

```_export
Usage: ffs export [OPTIONS] [ROOT]

  Read the FFS and its metadata into JSON.

Options:
  -s, --sort               Whether to sort keys in outupt.
  -s, --indent INTEGER     Indentation of output: none by default, 0 for
                           newlines, a positive number N for N spaces, a
                           negative number -N for N tabs.
  -l, --flatlines          Un-nest the entries and print one object per line.
                           The 'children' attribute is replaced by an array of
                           string names, and the 'name' attribute now includes
                           the entry's ancestors (/-separated). '--indent'
                           option is ignored.
  -r, --recursion INTEGER  Depth to recurse into entries; negative (default)
                           for infinite. Directories which are not valid
                           entries are not explored.
  --help                   Show this message and exit.
```

### Book

```_book
Usage: ffs book [OPTIONS] [ROOT] TARGET

  Export the FFS metadata into files for mdbook.

Options:
  -t, --title TEXT         Title for generated book, default
                           '{FQDN}:{ROOT_REAL_PATH}'.
  -r, --recursion INTEGER  Depth to recurse into entries; negative (default)
                           for infinite. Directories which are not valid
                           entries are not explored.
  --help                   Show this message and exit.
```

### Problems

```_problems
Usage: ffs problems [OPTIONS] [ROOT]

  List problems with the structure of the FFS.

  Prints a TSV with columns:

  1- comma-separated individuals responsible for entry (or parent if unknown);
  2- path of problem entry, relative to given root; 3- description of the
  problem

Options:
  -c, --check          Exit with an error code at the first problem
  -s, --skip-problems  Do not attempt to traverse below directories with
                       malformed metadata
  --help               Show this message and exit.
```

## Development

A number of `make` recipes are included for convenience of regular development tasks.
In particular, see `make {install-dev,update-spec,fmt,lint,test,readme,book}`.
