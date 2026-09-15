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


## Module Reuse Across Files

LFR supports Verilog-style cross-file module reuse. Put every reusable block
in its own `.lfr` file (one `module` per file), import it with a backtick
`` `import `` directive at the top, and instantiate it by name.

### Convention: `filename == module name`

For every `Foo.lfr` the file must declare exactly one `module Foo(...)`.
The compiler checks this after preprocessing:

- By default: a warning is printed for every mismatch.
- Set `LFR_STRICT_MODULE_NAMES=1` to turn the warning into a hard error.

This convention is what lets the preprocessor, the ANTLR pass, and
`fluigi synthesize` all agree on which file holds which module without any
extra metadata.

### Import syntax

```lfr
`import "Valve.lfr"                 // bare basename
`import "components/Valve.lfr"      // relative path (below the importing file)
`import "/abs/path/Valve.lfr"       // absolute path
```

Only one import per line. The quoted string must end in `.lfr`.

### How imports are resolved

For each `` `import "<spec>" ``, the preprocessor resolves `<spec>` to an
actual file in this order:

1. **Absolute path** -> used as-is if it exists.
2. **Path with a directory component** (e.g. `pkg/Foo.lfr`):
   1. tried relative to the directory of the file doing the import, then
   2. tried relative to each `--pre-load` / library directory.
3. **Bare basename** (e.g. `Foo.lfr`):
   1. first looked up in the preloaded library index (any `.lfr` under the
      `--pre-load` / library directories, scanned recursively), then
   2. tried relative to the directory of the file doing the import.

Nested / transitive imports are followed automatically: if a library file
itself contains `` `import "Bar.lfr" ``, `Bar.lfr` is pulled in too. A
circular import raises an error instead of looping.

### Library search paths

Two sources feed the preloaded library index:

- Anything passed via `--pre-load <dir>` (repeatable, recursive scan).
- The directory given by `--library-path <dir>` (defaults to `pylfr/library`).
  Since Neptune 2026 this directory is **automatically** added to the
  preloaded library index, so `` `import "foo.lfr" `` works without needing
  to repeat the path as `--pre-load`.

### Example

```
project/
├── valve/
│   └── Valve.lfr        // module Valve(...)
└── top.lfr              // `import "valve/Valve.lfr"
                         // Valve v1(a, b, out, c);
```

Compile:

```
fluigi compile_lfr -o ./out top.lfr
```

No `--pre-load` is required because the import uses a path relative to
`top.lfr`.

## User-Defined JSON Components (Black Box)

When your design uses a component that is *not* a 3DuF primitive (so the
primitives server has no idea what its dimensions or terminals look like),
you can ship its ParchMint description alongside your design and hand it
to Fluigi as a **component library**. Fluigi will treat the component as
a black box: its bounding box, params and external terminals are read
out of your JSON, but its internal structure is not merged into the top
design (that's a future pass).

### File convention: `<EntityName>.json`

For every custom entity `FooBar`, place a `FooBar.json` under a directory
that Fluigi scans. By default, Fluigi always looks under the Neptune repo
root at **`user_components/`** (create it if missing; it is tracked with
a `.gitkeep`). Override that root with env **`FLUIGI_USER_COMPONENT_LIBRARY`**
(absolute path, or relative to the shell working directory).

You can add more search roots with **`--component-library <dir>`** (repeatable);
those directories are scanned *after* the default root. Use
**`--no-default-component-library`** if you want *only* your explicit
`--component-library` paths.

The filename stem *is* the entity name. If the top design is a MINT file,
MINT will upper-case the entity to `FOOBAR` — Fluigi matches entity names
case-insensitively so `FooBar.json` still resolves when the design refers
to `FOOBAR`.

### What Fluigi extracts

From each `<EntityName>.json` (a valid ParchMint v1.2 device):

- **Bounding box**: top-level `x-span` / `y-span` (preferred) or
  `params.width` / `params.length`.
- **External terminals**: every component whose `entity` is `"PORT"`.
  - Terminal label = that PORT component's `name`.
  - Terminal `(x, y)` = that PORT component's `params.position`.
  - Terminal `layer` = `FLOW` / `CONTROL` depending on the first layer
    that PORT component references.
- **Default params**: `componentSpacing` is seeded from the JSON (or
  defaulted to `1000`). Other keys are left to the top-level instance.

### CLI flags

```
fluigi compile_mint        [--component-library <dir>] ... <input.mint>
fluigi compile_lfr         [--component-library <dir>] ... <input.lfr>
fluigi synthesize          [--component-library <dir>] ... <input.lfr>
fluigi synthesizeFromMINT  [--component-library <dir>] ... <input.mint>
```

`--component-library` is repeatable (`--component-library dirA
--component-library dirB`). Each directory is scanned recursively for
`*.json`.

### Error behaviour (strict unknown components)

**Strict** mode (collect unknown entities and raise at the end) turns on
when **at least one** `--component-library` path was passed, or when env
**`FLUIGI_STRICT_COMPONENTS=1`** is set. In strict mode, any component whose
`entity` is resolved by **neither** the scanned library directories **nor**
the primitives server is reported once at the end of the pass:

```
Design references 1 unknown component type:
  - MYGADGET                       used by 1 instance(s): gadget_1

Searched component libraries:
  - /path/to/your/lib
  (library knows: MyValve, MyPump)

Searched primitives server: http://localhost:6070

Fix: place a '<EntityName>.json' file in one of the component-library
directories (filename stem must match the entity name), or pass another
directory via --component-library <dir>.
```

This keeps "unknown component" (your design references something nobody
knows about) distinct from "network hiccup" (the primitives server is
unreachable) — the latter degrades to **local fallbacks** for known 3DuF
entities (`PORT`, `MIXER`, `MUX`, `YTREE`, `VIA`, … in `fluigi/primitives.py`)
so a dead server does not emit `x-span=-1`. Truly unknown entities still warn
(or raise in strict mode).

If you rely **only** on the default `user_components/` scan and did **not**
pass `--component-library`, strict mode is **off** by default so existing
pipelines keep warn-and-skip semantics; set **`FLUIGI_STRICT_COMPONENTS=1`**
to require every entity to resolve while still using only the default
directory.

### Built-in `DIYcomponent` black box (call like a function)

Import the module and instantiate it with Verilog-style parameters plus
four clockwise sides (`up` / `right` / `down` / `left`). Use `None` for unused
sides. Do **not** put `#MAP "DIYCOMPONENT" "~"` in the parent module — that
would collide with MIXER/`~` mapping. The `~` map stays inside
`DIYcomponent.lfr`. Flow direction is inferred from the bound nets (no
finput/foutput labels on the sides).

```lfr
`import "library/DIYcomponent.lfr"

module my_chip(finput in1, foutput out1);
    DIYcomponent #(length=10000, width=8000, height=2000) box(
        .up(in1),
        .right(None),
        .down(out1),
        .left(None)
    );
endmodule
```

Parameters (µm):

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `length` | 5000 | Bounding-box height (`y-span`) |
| `width` | 5000 | Bounding-box width (`x-span`) |
| `height` | 250 | Layer depth |
| `componentSpacing` | **1000** | Keepout halo around the box. P&R keeps other components and channel bodies outside this band. |

Override keepout on one instance:

```lfr
DIYcomponent #(length=10000, width=8000, height=2000, componentSpacing=3000) box(
    .up(in1),
    .right(None),
    .down(out1),
    .left(None)
);
```

Terminals: up=1, right=2, down=3, left=4. Fluigi sizes the box from
`length` / `width` / `height` (µm); `componentSpacing` is layout keepout only
(no internal geometry). In 3DuF, DXF export builds a rectangular enclosure
whose depth is `max(component height) + 1 mm` so you can swap in a detailed
CAD part later (Fusion 360, etc.). See `default-modules/DIYcomponent.lfr` and
`Quick_Examples/library/DIYcomponent.lfr`.

### Demo

A minimal, runnable example lives in
`Microfluidics-Benchmarks/Quick_Examples/user_components_demo/`:

```
user_components_demo/
├── lib/
│   └── MyGadget.json     # defines entity MyGadget (4 terminals)
├── TopDesign.mint        # uses MYGADGET gadget_1
└── README.md
```

Run it with:

```bash
cd Microfluidics-Benchmarks/Quick_Examples/user_components_demo
fluigi compile_mint TopDesign.mint --component-library lib/ -o out/
```

## YTREE / TREE mapping

`#MAP "YTREE" "assign"` (and TREE) is a **procedural** primitive. LFR counts
subgraph sources/sinks, writes `in`/`out`/`leafs`, and tags each connecting
option with the FIG node it belongs to. Netlist generation consumes a leaf
only when the neighbor construction node covers that FIG node, so a 16-way
fan-out uses ports **2–17** once each. Unmatched edges (mixers on the trunk)
use port **1** and do not steal leaves. Fluigi may still grow `out`/`in` from
the highest connected MINT port if an older mint says `out=8` but wires port 17.

## Running Benchmark Test Scripts

```
cd scripts
./test-script.sh > test-script-log_"`date +"%d-%m-%Y-%T"`".log 2>&1
```


## License

BSD-3-Clause

Copyright (c) 2021, CIDAR LAB All rights reserved.

