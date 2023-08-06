# Termplots

A lightweight plot library for your terminal

## Installation

```
pip install termplots
```

## Get started

### Simple plot

```python
import termplots as tmp

tmp.plot([-0.5,0,1,0.5,1.5], ystep=0.5)
```

Output:

```
 2.0|
 1.5|        *
 1.0|    *
 0.5|      *
 0.0|--*-------
 0.5|*
 1.0|
```

### Multiple plots

```python
import termplots as tmp

tmp.mplot([[1,0,2], [-1,0,3,0,2,2]], car=['*', '$', '@'], labels=['List 1', 'List 2'])
```

Output:

```
 4|
 3|    $
 2|    *   $ $
 1|*
 0|--@---$-----
 1|$
 2|

*: List 1
$: List 2
@: overlaps
```

## Other arguments

### `plot()`

- `ystep` (default `1`): defines steps on the y axis
- `lowlim`: lower limit of the y axis
- `highlim`: upper limit of the y axis
- `car` (default `*`): point(s) marker

### `mplot()`

- `ystep` (default `1`): defines steps on the y axis
- `lowlim`: lower limit of the y axis
- `highlim`: upper limit of the y axis
- `car` (default `['*', '#', '@']`): list of point(s) marker, the last char is used for overlaps
- `labels` (default `None`): list of labels

## Colors

Termplots support up to 6 colors. Colors are automatically assigned to different series.

> I tested the colors only on macOS. If the colors don't work try a different terminal or open an issue
