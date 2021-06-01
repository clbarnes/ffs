# ffs

Python tools for querying a Flexible File Structure as specified in https://gitlab.com/cardonazlaticlabs/data-policy

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
  book      Export the FFS metadata into markdown files which can be...
  export    Read the FFS and its metadata into JSON.
  problems  List problems with the structure of the FFS.
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

  Export the FFS metadata into markdown files which can be consumed by
  mdbook for creating a static website.

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

Options:
  -c, --check          Exit with an error code at the first problem
  -s, --skip-problems  Do not attempt to traverse below problematic
                       directories

  --help               Show this message and exit.
```
