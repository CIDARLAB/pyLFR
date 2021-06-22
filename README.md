# LFR <img align="right" src="LFR-Logo-01.png" width="250">

## Dependencies 

LFR requires the user to install graphviz onto the system for the pygraphviz dependencies to work correctly. Current the pygraphviz wheels available can partially remedy the issue of not finding graphviz as one of the dependencies.

## ANTLR4

We need ANTLR for generating the listener. Install ANTLR4 from the [website](https://www.antlr.org/index.html)

### LFR Grammar

```
antlr4 -o ./lfr/antlrgen/lfr -listener -visitor -Dlanguage=Python3 -lib . ./lfrX.g4
```

### Reggie(Graph Match) Grammar

```
antlr4 -o ./lfr/antlrgen/reggie -listener -visitor -Dlanguage=Python3 -lib . ./reggie.g4
```

### Graphviz

In a pipenv/pip command installing the pygraphviz binary would require the following environment commands.

```
pipenv run pip install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz
```

Compiling a wheels archive of graphviz to partially remove the dependency can be done using the following command. (Ensure that `wheels` is installed).

```
pip wheel pygraphviz -w .
```

In order to use the wheels package as a dependency during installation with poetry you need to set the `pygraphviz` dependency in the following way in the `pyproject.toml` :

For Linux:
```
pygraphviz = { file= "pygraphviz-1.6-cp38-cp38-linux_x86_64.whl" }
```

For Mac:
```
pygraphviz = { file= "pygraphviz-1.6-cp38-cp38-macosx_10_15_x86_64.whl" }
```

## Usage

```
usage: lfr-compile [-h] [--outpath OUTPATH] [--technology TECHNOLOGY] [--library LIBRARY]
                   [--no-mapping NO_MAPPING] [--no-gen]
                   input [input ...]

positional arguments:
  input                 This is the file thats used as the input

optional arguments:
  -h, --help            show this help message and exit
  --outpath OUTPATH     This is the output directory
  --technology TECHNOLOGY
                        This is the mapping library you need to use
  --library LIBRARY     This sets the default library where the different technologies sit in
  --no-mapping NO_MAPPING
                        Skipping Explicit Mappings
  --no-gen              Force the program to skip the device generation
  ```


## Running Benchmark Test Scripts

```
cd scripts
./test-script.sh > test-script-log_"`date +"%d-%m-%Y-%T"`".log 2>&1
```


## License

BSD-3-Clause

Copyright (c) 2021, CIDAR LAB All rights reserved.

