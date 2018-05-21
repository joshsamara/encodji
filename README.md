# Encodji 👌

A library to:

```
😵🙈🤖🙉💩😺🤐🧒😺😹🧑😿👽🧒🤐👦👧🧑😸😸🤐😼🙈👧🙉🤐👽🤐👦👧🧒😼🙈😹🤐🙉😸🤐😺😾🙉😽😼👦🙃
```

aka

```
Encode regular stuff into a string of emojis.
```

as well as:

```
🤪😺🤖🙉💩😺🤐👦👧🧒😼🙈😹👦🤐🙉😸🤐😺😾🙉😽😼👦🤐😼🙈👧🙉🤐👧😺🧓👧🙃
```

(*Decode strings of emojis into text.*)

# Setup

*Note* This project uses [pipenv](https://docs.pipenv.org/). See
https://docs.pipenv.org/ for setup instructions.

To setup and basically use any commands use:

```
pipenv install --dev
```

# Usage

Two commands are currently supported (with the same options).

They can be run with the following:

```
python [encode/decode] [-t TEXT TO PROCESS] [-i INPUT_FILE] [-o OUTPUT FILE]
```

You have the option to either encode or decode text (not both).

You can pass one of either:

* `-t` to pass text right there or;
* `-i` to have the script read from a file

If `-o` is passed, a file will be written to with the output of the command,
otherwise the result will be printed to std out

## Examples

### Using the -t flag
```
$ python scripts.py encode -t yo
👴🙉
```

```
$ python scripts.py encode -t 👴🙉
yo
```

### Using the -i and -o flags
```
$ python scripts.py encode -i fetcher/fetch.py -o tmp.txt
```


```
$ python scripts.py decode -i tmp.txt
"""
Fetches and saves emojis to disk.
"""

import json
...
```
