## Spreader

A fast spreadsheet logic library. 

[![License](https://img.shields.io/badge/license-BSD-brightgreen.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![pypi](https://img.shields.io/pypi/v/eg.spreader)](https://pypi.org/project/eg.spreader)
[![python](https://img.shields.io/badge/python->=3.7-blue.svg)](https://www.python.org)
<!--https://img.shields.io/pypi/pyversions/eg.spreader -->

<!-- References -->

[dynamicformulas]: <https://support.microsoft.com/en-us/office/dynamic-array-formulas-and-spilled-array-behavior-205c6b06-03ba-4151-89a1-87a7eb36e531> (Dynamic Array Formulas)

<!--  End References -->

Spreader is a zero dependency library that implements spreadsheet logic - reading and writing data and formulas into cells, automatic recalculation, copying and moving cells, adding and deleting rows and columns and so on. It does not implement any spreadsheet UI. 
It is currently in alpha stage.

## Install

Spreader is a C++ library. Binary wheels are provided for common configurations on macOS and Windows.
If you are on another platform or have an uncommon configuration `pip` will build the module from 
source. 
In order for a build from source to succeed you will need 
- Working C++ compiler supporting C++20 standard
  - Linux: GCC 11.3 or above
  - macOS: Xcode 14 or above 
  - Windows: Visual Studio 2022 or above 
- On Linux you will also need Python development support (the python-dev or python3-dev package in most Linux distributions). 
No further external dependencies are required. 

To install the module

```bash
pip install eg.spreader
```

## Quick start

```python
from eg.spreader import Sheet
...

#Create a new sheet
sheet = Sheet()
#Set a cell to contain plain value. Instead of "A2" 
#you can also say Point(x=0, y=1) or just (0, 1) or [0, 1]. 
#Columns are x and rows y, zero-based
sheet.setValueCell("A2", "Hello ")
sheet.setValueCell("B3", "World!")
#Set a cell to contain formula
sheet.setFormulaCell("A1", "A2 & B3")
#Read calculated formula result
val = s.getValue("A1")
#val is "Hello Wolrd!" here
```

## Limits

Maximum possible size of a sheet is currently 65536 x 2147483648 (e.g. 2<sup>16</sup> x 2<sup>31</sup>) cells. 
You can query this value via `Sheet.maxSize` property. 
Note that currently, sheets are held entirely in memory (there is no 'offloading' of unused data to some kind of storage).
Thus, depending on how much memory you have available the actual limit on how big a sheet you will be able to create might
be lower than maximum.

There is no hard limit on things like:
- Maximum length of cell's string value
- Maximum number of function arguments (for functions that support variable number of arguments like `SUM`)
- Maximum level of nesting in formulas
or anything else in the library. Instead, those are limited by available memory. In practice such limit is quite a bit larger than
traditional `255` of Excel.


## Cell and Area coordinates

Cell coordinates in the API can be given in the usual "A1", "B2" format. Alternatively, and slightly faster, you can use `Point(x=..., y=...)` objects or `(x, y)` tuples or `[x, y]` lists. In the later case `x` and `y` are zero based so `Point(x=0, y=0)` and `(0, 0)` correspond to "A1".

Similarly area coordinates can be given either as "A1:B2" or as `Rect(Point(x=..., y=...), Size(width=..., height=...))` or as
`(x, y, width, height)` or `[x, y, width, height]`, whichever suits your needs more. As with individual cells, using "A1:B2" format is slightly slower.

## Cell values

Spreader supports the following cell value types: `None` (e.g. blank cell), `bool`, `float`, `str` and instances of its own
`ErrorValue` class. All known errors are available as constants from `Errors` class (e.g. `Errors.InvalidReference`) and represent the usual spreadsheet #-errors (e.g. `#REF!`).

Numbers contained in a cell are never NaNs and never infinite. Setting a NaN or infinite value cell will result in an `ErrorValue` instead.

Strings you set into a cell via `sheet.setValueCell()` call do not need to be escaped - they are always taken to be literal. 
For example `sheet.setValueCell("A1", "=3")` will result in a cell holding literal "=3" value as if you typed `'=3` in Excel
or other spreadsheets. 

## Supported formulas

Spreader supports all the operators (e.g. `=`, `+`, `>`, `*` etc.) supported by Excel. 

[Dynamic array formulas][dynamicformulas] are fully supported. Therefor there is no need for `ARRAYFORMULA` and it isn't recognized.

The following functions are currently implemented:
<details>
  <summary>Expand</summary>

* **A** \
ADDRESS, AVERAGE, AVERAGEA, AVERAGEIF
* **C** \
CEIL, CHOOSE, COLUMN, CONCAT, CONCATENATE, COUNT, COUNTA
* **D** \
DATE, DATEDIF, DAY, DAYS
* **E** \
EDATE, EOMONTH, ERROR.TYPE
* **F** \
FIND, FLOOR
* **H** \
HLOOKUP, HOUR
* **I** \
IF, INDEX, INDIRECT, INT, ISBLANK, ISERR, ISERROR, ISEVEN, ISLOGICAL, ISNA, ISNONTEXT, ISNUMBER, ISODD, ISOWEEKNUM, ISTEXT
* **L** \
LEFT, LEN, LOWER  
* **M** \
MATCH, MAX, MAXA, MID, MIN, MINA, MINUTE, MOD, MONTH, MROUND
* **N** \
NOT, NOW
* **O** \
OR
* **R** \
REPLACE, RIGHT, ROUND, ROUNDDOWN, ROUNDUP, ROW
* **S** \
SECOND, SIGN, STDEV, STDEV.P, STDEV.S, STDEVA, STDEVP, STDEVPA, SUBSTITUTE, SUM, SUMIF, SWITCH
* **T** \
TIME, TODAY, TRANSPOSE, TRIM
* **U** \
UPPER
* **V** \
VLOOKUP
* **W** \
WEEKDAY, WEEKNUM
* **X** \
XOR
* **Y** \
YEAR
</details>

## Recalculation

By default sheet recalculation is automatic. You can suspend it using `sheet.suspendRecalc()` and resume it again using
`sheet.resumeRecalc()`. Suspend calls can nest and each is "undone" by a corresponding resume. While suspended you can 
manually recalculate a sheet using `sheet.recalculate()`.

## Manipulating sheet size

Similar to how visual spreadsheets behave sheet size (as returned by `sheet.size()`) is dynamic and you don't manipulate 
it directly. When you set any cell to a non-null value sheet automatically expands to encompass it if it is outside
the current size. It doesn't automatically contract, however. To reduce size you can use `sheet.deleteColumns()` and
`sheet.deleteRows()` calls. Those, as well as `sheet.insertColumns()` and `sheet.insertRows()` can be used to 
delete/insert rows and columns anywhere in the sheet. Just like in visual spreadsheets all the references in formulas
will be automatically adjusted to account for insertion or deletion.

## Copying and moving cells

Normal copying and moving semantics of spreadsheets are also fully supported. You can use:
- `sheet.copyCell()` to copy a single cell to a single cell or area. 
- `sheet.copyCells()` (note the plural) to copy an area to another location given by its top left corner
- `sheet.moveCell()` to move a single cell to a new location (also a single cell)
- `sheet.moveCells()` to move a cell area to a new location given by its top left corner

For all these calls the formula references are adjusted in normal spreadsheet fashion.


## Roadmap and missing features

Spreader is currently in alpha - implemented features work and work well but many desirable things are missing.
The following features are currently on the roadmap:

- Change notifications to enable clients to react to cells changed during recalculation
- Ability to associate abstract formatting information with cells rows and columns. Spreader itself doesn't care
about formatting - it just needs to keep track of it for clients to act upon.
  - Support conditional formatting formulas. Similar to above associate opaque format with boolean formulas and tell
  the client which one to use.
- Support optional undo. It needs to be optional because it will slow things down and not all clients need it.
- Support more functions in formulas
- Support localized formula input. Currently formula syntax must use US English syntax: `.` as decimal separator, `,` to separate
arguments. Excel allows using `,` and `;` for languages that use comma as decimal separator.
- Serialization/deserialization. Likely in `xlsx` and `json`.
- Maybe: support manipulating very large spreadsheets by offloading parts of them to persistent 
storage and not keeping everything in memory.
- Maybe: support doing spreadsheet math using decimals rather than doubles.


