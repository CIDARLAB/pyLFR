

## Queries

Match queries for MINT Componnet library 2021 Spring

### PORT

```
{
    v1:IO
}
```

### MIXER

```
{
    v1:MIX
}
```

### DROPLET CAPACITANCE SENSOR

```
{
    v1:PROCESS
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

### DROPLET SPLITTER
```
{
    v1:DIVIDE
}
```

### FILTER

```
{
    v1:PROCESS
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

### Output MUX

### 1->2

```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo2 { "DISTRIBUTE_OR", "or_1" }
}
```

### 1->4

```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo2 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo3 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo4 { "DISTRIBUTE_OR", "or_1" }
}
```

### 1->8

```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo2 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo3 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo4 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo5 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo6 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo7 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo8 { "DISTRIBUTE_OR", "or_1" }
}
```


### 1->16

```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo2 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo3 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo4 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo5 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo6 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo7 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo8 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo9 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo10 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo11 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo12 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo13 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo14 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo15 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo16 { "DISTRIBUTE_OR", "or_1" }
}
```


### 1->32

```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo1 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo2 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo3 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo4 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo5 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo6 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo7 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo8 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo9 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo10 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo11 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo12 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo13 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo14 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo15 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo16 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo17 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo18 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo19 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo20 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo21 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo22 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo23 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo24 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo25 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo26 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo27 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo28 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo29 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo30 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo31 { "DISTRIBUTE_OR", "or_1" },
    v1 -> vo32 { "DISTRIBUTE_OR", "or_1" }
}
```

### Input MUX

### 2->1
```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    vi1 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi2 { "DISTRIBUTE_OR", "or_1" } -> v1
}
```

### 4->1
```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    vi1 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi2 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi3 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi4 { "DISTRIBUTE_OR", "or_1" } -> v1
}
```

### 8->1
```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    vi1 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi2 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi3 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi4 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi5 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi6 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi7 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi8 { "DISTRIBUTE_OR", "or_1" } -> v1
}
```

### 16->1
```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    vi1 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi2 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi3 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi4 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi5 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi6 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi7 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi8 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi9 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi10 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi11 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi12 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi13 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi14 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi15 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi16 { "DISTRIBUTE_OR", "or_1" } -> v1
}
```

### 32->1
```
{
    v1 { "DISTRIBUTE_OR", "or_1" },
    vi1 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi2 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi3 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi4 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi5 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi6 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi7 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi8 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi9 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi10 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi11 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi12 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi13 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi14 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi15 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi16 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi17 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi18 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi19 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi20 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi21 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi22 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi23 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi24 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi25 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi26 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi27 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi28 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi29 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi30 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi31 { "DISTRIBUTE_OR", "or_1" } -> v1,
    vi32 { "DISTRIBUTE_OR", "or_1" } -> v1
}
```


### PATTERN BASED

```
{
    ? { "or_1" } -> v1,
    (? { "or_1" } -> v1)+
}
```

```
{
    v1 -> ? { "or_1" },
    (v1 -> ? { "or_1" })+
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

### Output

### 1->2

```
{
    v1 -> vo1,
    v1 -> vo2
}
```

### 1->4

```
{
    v1 -> vo1,
    v1 -> vo2,
    v1 -> vo3,
    v1 -> vo4
}
```

### 1->8

```
{
    v1 -> vo1,
    v1 -> vo2,
    v1 -> vo3,
    v1 -> vo4,
    v1 -> vo5,
    v1 -> vo6,
    v1 -> vo7,
    v1 -> vo8
}
```


### 1->16

```
{
    v1 -> vo1,
    v1 -> vo2,
    v1 -> vo3,
    v1 -> vo4,
    v1 -> vo5,
    v1 -> vo6,
    v1 -> vo7,
    v1 -> vo8,
    v1 -> vo9,
    v1 -> vo10,
    v1 -> vo11,
    v1 -> vo12,
    v1 -> vo13,
    v1 -> vo14,
    v1 -> vo15,
    v1 -> vo16
}
```


### 1->32

```
{
    v1 -> vo1 ,
    v1 -> vo2 ,
    v1 -> vo3 ,
    v1 -> vo4 ,
    v1 -> vo5 ,
    v1 -> vo6 ,
    v1 -> vo7 ,
    v1 -> vo8 ,
    v1 -> vo9 ,
    v1 -> vo10 ,
    v1 -> vo11 ,
    v1 -> vo12 ,
    v1 -> vo13 ,
    v1 -> vo14 ,
    v1 -> vo15 ,
    v1 -> vo16 ,
    v1 -> vo17 ,
    v1 -> vo18 ,
    v1 -> vo19 ,
    v1 -> vo20 ,
    v1 -> vo21 ,
    v1 -> vo22 ,
    v1 -> vo23 ,
    v1 -> vo24 ,
    v1 -> vo25 ,
    v1 -> vo26 ,
    v1 -> vo27 ,
    v1 -> vo28 ,
    v1 -> vo29 ,
    v1 -> vo30 ,
    v1 -> vo31 ,
    v1 -> vo32 
}
```

### Input

### 2->1
```
{
    vi1  -> v1,
    vi2  -> v1
}
```

### 4->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1
}
```

### 8->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1,
    vi5  -> v1,
    vi6  -> v1,
    vi7  -> v1,
    vi8  -> v1
}
```

### 16->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1,
    vi5  -> v1,
    vi6  -> v1,
    vi7  -> v1,
    vi8  -> v1,
    vi9  -> v1,
    vi10  -> v1,
    vi11  -> v1,
    vi12  -> v1,
    vi13  -> v1,
    vi14  -> v1,
    vi15  -> v1,
    vi16  -> v1
}
```

### 32->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1,
    vi5  -> v1,
    vi6  -> v1,
    vi7  -> v1,
    vi8  -> v1,
    vi9  -> v1,
    vi10  -> v1,
    vi11  -> v1,
    vi12  -> v1,
    vi13  -> v1,
    vi14  -> v1,
    vi15  -> v1,
    vi16  -> v1,
    vi17  -> v1,
    vi18  -> v1,
    vi19  -> v1,
    vi20  -> v1,
    vi21  -> v1,
    vi22  -> v1,
    vi23  -> v1,
    vi24  -> v1,
    vi25  -> v1,
    vi26  -> v1,
    vi27  -> v1,
    vi28  -> v1,
    vi29  -> v1,
    vi30  -> v1,
    vi31  -> v1,
    vi32  -> v1
}
```




### Pattern Based
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

### Output

### 1->2

```
{
    v1 -> vo1,
    v1 -> vo2
}
```

### 1->4

```
{
    v1 -> vo1,
    v1 -> vo2,
    v1 -> vo3,
    v1 -> vo4
}
```

### 1->8

```
{
    v1 -> vo1,
    v1 -> vo2,
    v1 -> vo3,
    v1 -> vo4,
    v1 -> vo5,
    v1 -> vo6,
    v1 -> vo7,
    v1 -> vo8
}
```


### 1->16

```
{
    v1 -> vo1,
    v1 -> vo2,
    v1 -> vo3,
    v1 -> vo4,
    v1 -> vo5,
    v1 -> vo6,
    v1 -> vo7,
    v1 -> vo8,
    v1 -> vo9,
    v1 -> vo10,
    v1 -> vo11,
    v1 -> vo12,
    v1 -> vo13,
    v1 -> vo14,
    v1 -> vo15,
    v1 -> vo16
}
```


### 1->32

```
{
    v1 -> vo1 ,
    v1 -> vo2 ,
    v1 -> vo3 ,
    v1 -> vo4 ,
    v1 -> vo5 ,
    v1 -> vo6 ,
    v1 -> vo7 ,
    v1 -> vo8 ,
    v1 -> vo9 ,
    v1 -> vo10 ,
    v1 -> vo11 ,
    v1 -> vo12 ,
    v1 -> vo13 ,
    v1 -> vo14 ,
    v1 -> vo15 ,
    v1 -> vo16 ,
    v1 -> vo17 ,
    v1 -> vo18 ,
    v1 -> vo19 ,
    v1 -> vo20 ,
    v1 -> vo21 ,
    v1 -> vo22 ,
    v1 -> vo23 ,
    v1 -> vo24 ,
    v1 -> vo25 ,
    v1 -> vo26 ,
    v1 -> vo27 ,
    v1 -> vo28 ,
    v1 -> vo29 ,
    v1 -> vo30 ,
    v1 -> vo31 ,
    v1 -> vo32 
}
```

### Input

### 2->1
```
{
    vi1  -> v1,
    vi2  -> v1
}
```

### 4->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1
}
```

### 8->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1,
    vi5  -> v1,
    vi6  -> v1,
    vi7  -> v1,
    vi8  -> v1
}
```

### 16->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1,
    vi5  -> v1,
    vi6  -> v1,
    vi7  -> v1,
    vi8  -> v1,
    vi9  -> v1,
    vi10  -> v1,
    vi11  -> v1,
    vi12  -> v1,
    vi13  -> v1,
    vi14  -> v1,
    vi15  -> v1,
    vi16  -> v1
}
```

### 32->1
```
{
    vi1  -> v1,
    vi2  -> v1,
    vi3  -> v1,
    vi4  -> v1,
    vi5  -> v1,
    vi6  -> v1,
    vi7  -> v1,
    vi8  -> v1,
    vi9  -> v1,
    vi10  -> v1,
    vi11  -> v1,
    vi12  -> v1,
    vi13  -> v1,
    vi14  -> v1,
    vi15  -> v1,
    vi16  -> v1,
    vi17  -> v1,
    vi18  -> v1,
    vi19  -> v1,
    vi20  -> v1,
    vi21  -> v1,
    vi22  -> v1,
    vi23  -> v1,
    vi24  -> v1,
    vi25  -> v1,
    vi26  -> v1,
    vi27  -> v1,
    vi28  -> v1,
    vi29  -> v1,
    vi30  -> v1,
    vi31  -> v1,
    vi32  -> v1
}
```

### Pattern based


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