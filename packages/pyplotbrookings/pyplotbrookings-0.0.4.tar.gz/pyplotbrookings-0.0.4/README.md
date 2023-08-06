# pyplotbrookings <img src="figures/logo.png" align="right" width="120"/>

## Overview

`pyplotbrookings` is a `matplotlib` extension which implements the Brookings
style guide. It offers several color palettes, a custom theme, and a few
helper functions. `pyplotbrookings` is a python implementation of `ggbrookings`, 
an R extension for `ggplot`.

## Installation

Currently `pyplotbrookings` now a python package, it can be downloaded with `pip`!
The accepted alias for for `pyplotbrookings` is `ppb`. For example,
```python
import pyplotbrookings as ppb
```


## Usage

The `pyplotbrookings` package has a few simple user facing functions:

-   `set_theme()` overrides the default `matplotlib` theme for a
    custom one which adheres to the Brookings style guide.

-   `set_palette()` sets the `matplotlib` color cycler to one of
    several color palettes that are consistent with the Brookings brand
    and designed to provide color accessiblity.

-   `add_title()` adds titles and subtitles to a plot that are consistent 
    with Brookings brand guidelines. 

-   `add_logo()` adds a program/center logo to your plots after saving
    them. 

-   `get_camp()` returns a continuous palette (or color map) using one of
    the color Brookings color palettes.

-   `view_palette()` helper function that previews a color palette showing 
    both the order of palette and the appropriate text color that can be applied
    to each color.

-   `import_roboto()` imports and overrides the default `matplotlib` font (sans serif)
    to Roboto. Note, Roboto fonts come with this module so no additional font
    download is necessary. 

-   `figure()` creates a `matplotlib` figure in one of the standard Brookings sizes.

-   `save()` saves a figure in the Brookings advised dpi values depending on content type.


Palette dictionaries (`palettes` and `extended_palettes`) for `pyplotbrookings` can also be 
used directly but **only** for lookup and **not** assignment.

## Examples

Examples can be found in the attached Jupyter Notebook.