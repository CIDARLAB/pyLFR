### MIXER

```
{
    v1:MIX
}
```

### DROPLET CAPACITANCE SENSOR

```
{
    v1:TECHNOLOGY
}
```

### LONG CELL TRAP

```
{
    v1:STORAGE
}
```

### SQUARE CELL TRAP

```
{
    v1:STORAGE
}
```

### REACTION CHAMBER

```
{
    v1:STROAGE
}
```

### CHEMOSTAT RING

```
{
    v1:STORAGE
}
```

### CURVED MIXER

```
{
    v1:MIX
}
```

### DIAMOND REACTION CHAMBER

```
{
    v1:STORAGE
}
```

### NOZZLE DROPLET GENERATOR

```
{
    v1:METER
}
```

### DROPLET GENERATOR FLOW FOCUS

```
{
    v1:IO -> v2:METER
}
```

### DROPLET GENERATOR T

```
{
    v1:METER
}
```

### DROPLET MERGER

```
{
    v1:MIX
}
```

### FILTER

```
{
    v1:TECHNOLOGY
}
```

### GRADIENT GENERATOR

TODO - Figure out how to show this as the gradient generator
```
{
    ???????
}
```

### LL CHAMBER
TODO - Change the name of this

```
{
    v1:MIX -> v2:STORAGE
}
```

### LOGIC ARRAY

TODO - Figure out how to control sequences work from an LFR file. Also figure out where the 

```
{
    v1:STORAGE <-> v2:STORAGE,
    v1:STORAGE <-> v3:STORAGE,
    v1:STORAGE <-> v4:STORAGE,
    v2:STORAGE <-> v3:STORAGE,
    v3:STORAGE <-> v4:STORAGE
}
```

### DROPLET MERGER

```
{
    v1:MIX
}
```

### MUX
```
{
    ?:DISTRIBUTE_OR { "or_1" } -> v1,
    (?:DISTRIBUTE_OR { "or_1" } -> v1)+
}
```

```
{
    v1 -> ?:DISTRIBUTE_OR { "or_1" },
    (v1 -> ?:DISTRIBUTE_OR { "or_1" })+
}
```

### PICOINJECTOR
```
{
    v1:MIX
}
```

### PORT

```
{
    v1:IO
}
```

### PUMP

```
{
    v1:PUMP
}
```

### PUMP3D

```
{
    v1:PUMP
}
```

### ROTARY MIXER

```
{
    v1:MIX -> v2:STROAGE
}
```

```
{
    v1:STORAGE -> v2:MIX
}
```

### DROPLET SORTER

```
{
    v1:SIEVE
}
```

### MIXER3D

```
{
    v1:MIX
}
```

### TRANSPOSER

```
{

}
```

### TREE

```
{
    v1:FLOW -> ?:FLOW,
    (v1:FLOW -> ?:FLOW)+
}
```

```
{
    ?:FLOW -> v1:FLOW,
    (?: FLOW -> v1:FLOW)+
}
```

### YTREE

```
{
    v1:FLOW -> ?:FLOW,
    (v1:FLOW -> ?:FLOW)+
}
```

```
{
    ?:FLOW -> v1:FLOW,
    (?: FLOW -> v1:FLOW)+
}
```