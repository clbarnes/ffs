# Cardona lab data guidelines

These guidelines are intended to minimise ambiguity between researchers, and maximise compatibility with software tools and conventions.
While these guidelines may represent a "best practice" and a good starting point for new projects, they are less important than consistency within existing projects and compatibility with existing tools.

## Tooling

Where possible, use free, open source tools (e.g. python or R rather than MATLAB; LibreOffice rather than Microsoft Office).
This maximises accessibility and portability.

Always specify required software packages and their versions in an appropriate way which makes it as easy as possible to reproduce the environment.
For example, python's `requirements.txt`, `Imports` in R's `DESCRIPTION` file, or listing required toolboxes and 3rd party packages (with URLs, ideally to specific versions) for MATLAB.

Ideally, being able to run an analysis pipeline in a container ([docker](https://docs.docker.com) or [singularity](https://sylabs.io/guides/latest/user-guide/introduction.html)) guarantees portability.

## Determinism

Everything except raw experimental data and subjective annotations should be repeatable.
Many types of analysis are not, by default: they could use random numbers, or be order-dependent.

In most cases, sorting the data deterministically, and [seeding pseudo-random number generators](https://en.wikipedia.org/wiki/Random_seed), will make your analysis deterministic, and therefore repeatable.

e.g.

```python
#!/usr/bin/env python
import random

def not_repeatable():
    return [random.random(), random.random(), random.random()]

def repeatable():
    rng = random.Random(1991)  # some arbitrary seed number
    return [rng.random(), rng.random(), rng.random()]
```

If working with results which get jumbled up during analysis, sort them before output:

```python
#!/usr/bin/env python
my_numbers = {5, 7, 1, 2, 45, 3}

for n in sorted(my_numbers):
    print(n)
```

## Configuration

Various formats exist for sharing configuration between humans and machines.
If you have structured metadata in your project (e.g. experimental parameters), try to use one of these rather than hard-coding values into your scripts and pipelines.
Always use an appropriate file extension.

| Name | Pros | Cons |
| ---- | ---- | ---- |
| [TOML](https://github.com/toml-lang/toml) | Easy for humans and machines to read/write | Not good for deeply nested structures |
| [YAML](https://en.wikipedia.org/wiki/YAML) | Reasonably easy for humans to read, good for nesting and internal references | Specification is complicated - so are the programs which read it <br> ([StrictYAML](https://hitchdev.com/strictyaml/) is a simple, safe subset, but not widely used) |
| [JSON](https://en.wikipedia.org/wiki/JSON) | Somewhat easy for humans to read when formatted, very easy for machines to read/write, very widely supported | Harder for humans to write, or read when compact, no comments |
| [XML](https://en.wikipedia.org/wiki/XML) | Good for enforcing schemas, easy for machines to read/write, built-in metadata | Hard for humans to read/write, overly verbose |
| [INI](https://en.wikipedia.org/wiki/INI_file) | Commonly used, absolute basics are intuitive, some kind of support is often built-in | No specification, so different software interprets it differently - AVOID |

Broadly speaking:

- If the file will primarily be read/written by machines (with human editing as a fallback), use JSON.
- If the file requires deep nesting, use YAML.
- Otherwise, use TOML.

These formats can easily be inter-converted.

Other formats do exist (like HJSON, which tries to make JSON more human-readable) but are not widely used.

## Dates / times

As far as possible, dates should conform to [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601).
This makes them sortable, readable, unambiguous, and widely supported.

Use 4 digits for years, and 2 digits for months, days, hours, minutes, and seconds.
Always use a 24-hour clock.
Sub-second times can be represented as a decimal of appropriate precision.
Time zone, where appropriate, should be specified as `Z` for [UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time), or as a `+`/`-` `HHMM` offset from UTC.

Separate date values with `-`.
Separate date from time with `T`.
Separate time values (other than UTC offsets) with `:`.

e.g.

```
1999-11-30
2020-12-31T23:59:59.9999+0000
```

In C-like time representation (also used in python and the POSIX `date` utility), that is `%Y-%m-%dT%H:%M:%S%z` (in C and python, use `%f` for microseconds: `date` uses `%N` for nanoseconds).

Note the exceptions below for datetimes in filenames.

## File names

As much as possible, do not to use whitespace in file names.
If whitespace is absolutely necessary, use only a single space character (i.e. no tab, newline, carriage return, or multiple spaces).

Prefer lower case as much as possible.
Only use upper case where it confers some meaning, e.g. in an acronym or initialisation.
As far as possible, no two files in the same directory should be disambiguated solely by capitalisation (e.g. "my_file.txt" and "My_File.TXT").

### Characters

Where possible, use only [printable 7-bit ASCII characters](https://en.wikipedia.org/wiki/ASCII#Printable_characters).
This maximises compatability with software tools and researchers' keyboards.

Some platforms [restrict the characters you can use in file names](https://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words), or assign special meaning to characters such that they require quoting or escaping.
Try to avoid these characters (including, but not limited to, ``/\?%*^:;|`'"<>,=()[]{}&#$``) where possible, even if your platform allows them.

Where ASCII characters are not sufficient, make efforts to use [UTF-8 encoding](https://en.wikipedia.org/wiki/UTF-8), as it is a strict superset of ASCII, very widely supported, and can encode all [Unicode](https://en.wikipedia.org/wiki/Unicode) characters.

### Case conventions

Be aware of these common conventions for delimiting words without spaces, and try to stay consistent within a project:

- `snake_case`
- `SCREAMING_SNAKE_CASE`
- `kebab-case`
- `camelCase`
- `UpperCamel`

### File extensions

Most humans, and many software tools including some operating systems, infer a file's format from its extension: a few characters after the final period in a file name.
Where extensions exist for your file format, use them as specifically as possible.
For example, use `.csv` rather than `.txt` for comma separated value files even though they are indeed text; `.tsv` if the separators are tabs.

If there is no appropriate file extension for your specific data format, consider using `.bin` for binary data, and `.dat` for generic text data not designed for human consumption (can also be used for binary).
Document the format of this data, either alongside the data files, or with a permalink (do not rely on institutional knowledge).

### Datetimes in file names

Windows does not support `:` in file names, and many systems assign importance to period characters, so ISO-8601 datetimes are often not be appropriate.
Stripping just the problematic delimiters (`:.`) is therefore necessary for file names; stripping all delimiters (`-T:.+-`) may also be convenient if human readability is a secondary concern.
Also consider the precision appropriate for your file name (you probably don't need to name files for the millisecond they correspond to).

### File name schemas

When designing a file name schema for a project, it is important to find the balance between how easy it is the parse for humans and machines.
If you can guarantee a fixed width (e.g. for bounded numbers like times), use zero padding.
If the file name can semantically be split into different components, try to delimit those components with a particular character which should not occur in any of the individual components.
For example, a directory name which encodes the date, experimenter, and protocol name could look like

`2020-08-14_cbarnes_the-best-protocol`

This can be parsed in python using `date_str, name, protocol = my_filename.split("_")`, or in `awk` (printing each component on a new line) with `echo $my_directory | awk -F _ '{ printf "date: %s\nname: %s\nprotocol: %s", $1, $2, $3 }'`

Subdirectories are (more or less) free!
If lots of files in a directory share a component in their name, consider using a subdirectory for that component.
It can also be convenient to minimise the types of files present in a directory by keeping e.g. input data separate to output data separate to metadata and configuration.

## Versioning

### Version control systems

Relatively small, plain-text files (e.g. code, configuration, summary data, manuscripts) should be version-controlled for ease of tracking, attribution, sharing and collaboration.
Prefer [git](https://git-scm.com/) as a widely compatible, free/ open source, very thoroughly documented solution with a vibrant ecosystem.

Files are added to an index, and changes are stored in explicitly-controlled, annotated blocks called commits.
Commits can branch off from each other and later be merged back together, for experimental or parallel collaborative work.

Keeping experimental parameters, summary data, figures, and manuscripts synchronised (they can be in different repositories - use [git submodules](https://www.vogella.com/tutorials/GitSubmodules/article.html) to make a meta-repo to synchronise versions) is extremely valuable, as is being able to trivially jump through the project's history.
Furthermore, git with a remote service like GitHub or GitLab makes it very easy to backup, share, and collaborate on projects.

There are plenty of tutorials available for various purposes, including [this lab-internal one](https://clbarnes.github.io/version-control-tutorial/).
There are additionally standards/ workflows built on top of git, such as [Conventional Commits](https://www.conventionalcommits.org) and [GitFlow](https://datasift.github.io/gitflow/IntroducingGitFlow.html), which you may find helpful.

### Versioning schemes

#### Semantic versioning ([SemVer](https://semver.org/))

Use this if you can distinguish between "major" and "minor" versions (possibly smaller distinctions too).

In software, a major version comes with breaking changes: something which works on v1 may not work on v2 and vice versa.
A minor version may add functionality, but it does not change existing functionality other than to fix a bug: something which works correctly on v1.1 should work on v1.2, but the reverse is not true.
A patch version fixes a bug, but does not change correct functionality.

For a paper, a major version could be a submitted revision, a minor version adds content, and a patch version e.g. fixes typos.

Semantic versions are not necessarily lexicographically sortable as numbers enter double digits in an unpredictable manner, but most programming languages and shell tools can sort them fairly easily (e.g. python `sorted(version_list, key=lambda s: tuple(int(c) for c in s.split(".")))`, bash `cat versions.txt | sort -t "." -k1,1n -k2,2n -k3,3n`).

#### Calendar versioning ([CalVer](https://calver.org/))

If you are not making guarantees about the interface between versions, consider serialising the release date in some way (preferably sortable; see section on dates) and using that as a version.

Note that your choice of resolution (e.g. `YYYY.mm`) may limit your release schedule.
Some projects use a mixed schema where the components are year, then month, then the release number within that month.

#### Commit hashes

For maximum reproducibility, if part of a project is under version control, you can refer to the specific commit you used (e.g. noting which configuration you used for an experiment).
This is not particularly human-readable or ordinal, but it's specific and makes it very easy to retrieve those parameters.
Use `git rev-parse HEAD` to get the current git commit hash.
You may not need to use all of it (usually the first 7 or so characters are sufficient).

## Documentation

Include a plain-text README file wherever some explanation would be helpful.
Consider a light markup language like [markdown](https://commonmark.org/help/) for some basic formatting.

For more involved documentation, multiple tool ecosystems exist, including

- [mdBook](https://rust-lang.github.io/mdBook/), tying together multiple markdown pages into an HTML page
- [asciidoctor](https://asciidoctor.org/)
- [sphinx](https://www.sphinx-doc.org/en/master/)

## References

- [The FAIR Guiding Principles for scientific data management and stewardship](https://www.nature.com/articles/sdata201618)
- [Guidelines for a Standardized Filesystem Layout for Scientific Data](https://www.mdpi.com/2306-5729/5/2/43/htm)
- [Parallel sequencing lives, or what makes large sequencing projects successful](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5714127/)
