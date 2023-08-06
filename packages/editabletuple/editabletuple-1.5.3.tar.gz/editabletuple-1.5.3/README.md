# editabletuple

- [Overview](#overview)
- [Examples](#examples)
- [API](#api)
    - [Notes](#notes)

## Overview

This module provides the `editabletuple()` and `editableobject()` functions.

The `editabletuple()` function is used tor creating classes with a fixed
sequence of fields, similar to a namedtuple, except editable.

Each instance of a class created by the `editabletuple()` function's fields
can be accessed by index `et[i]` (or by slice), or by fieldname `et.name`.
Although fields can be read and written, they cannot be added or deleted.
Since instances are mutable they can't be used in sets or as dict keys.

If you provide a validator, it will be used when new instances are created
and updated.

The `editableobject()` function creates classes very similar to those
created by `editabletuple()`. The essential difference is that
``editableobject()``'s class's instances don't support indexing or
iteration, so support only fieldname access. They also have an addtional
`totuple` property (not needed for ``editabletuple()``s since `tuple(et)` is
sufficient due to their iteration support).

See the function docstrings for examples and more about the editabletuple
and editableobject APIs.

To install just use `python3 -m pip install editabletuple`. (See
[PyPI](https://pypi.org/project/editabletuple/).)

Or just copy the `editabletuple.py` file which is self-contained and depends
only on the standard library.

## Examples

### Example #1: no defaults; no validator

    >>> Options = editabletuple('Options', 'maxcolors shape zoom restore')
    >>> options = Options(5, 'square', 0.9, True)
    >>> options
    Options(maxcolors=5, shape='square', zoom=0.9, restore=True)
    >>> options.maxcolors = 7
    >>> options[-1] = False
    >>> options[2] -= 0.1
    >>> options
    Options(maxcolors=7, shape='square', zoom=0.8, restore=False)

### Example #2: with defaults but no validator

    >>> Rgb = editabletuple('Rgb', 'red green blue', defaults=(0, 0, 0))
    >>> black = Rgb()
    >>> black
    Rgb(red=0, green=0, blue=0)
    >>> navy = Rgb(blue=128)
    >>> navy
    Rgb(red=0, green=0, blue=128)
    >>> violet = Rgb(238, 130, 238)
    >>> violet
    Rgb(red=238, green=130, blue=238)

### Example #3: with defaults and a validator

If you provide a validator function, it will be called whenever an attempt
is made to set a value, whether at construction time or later by `et[i] =
value` or `et.fieldname = value`. It is passed an attribute `name` and an
attribute `value`. It should check the value and either return the value (or
an acceptable alternative value) which will be the one actually set, or
raise a `ValueError`.

    >>> def validate_rgba(name, value):
    ...     if name == 'alpha':
    ...         if not (0.0 <= value <= 1.0):
    ...             return 1.0 # silently default to opaque
    ...     elif not (0 <= value <= 255):
    ...         raise ValueError(f'color value must be 0-255, got {value}')
    ...     return value # must return a valid value or raise ValueError
    >>>
    >>> Rgba = editabletuple('Rgba', 'red', 'green', 'blue', 'alpha',
    ...                      defaults=(0, 0, 0, 1.0), validator=validate_rgba)
    >>> black = Rgba()
    >>> black
    Rgba(red=0, green=0, blue=0, alpha=1.0)
    >>> seminavy = Rgba(blue=128, alpha=0.5)
    >>> seminavy
    Rgba(red=0, green=0, blue=128, alpha=0.5)
    >>> violet = Rgba(238, 130, 238, alpha=2.5) # alpha too big
    >>> violet
    Rgba(red=238, green=130, blue=238, alpha=1.0)
    >>>
    >>> color = Rgba(green=99)
    >>> color
    Rgba(red=0, green=99, blue=0, alpha=1.0)
    >>> assert color.green == 99
    >>> color.red = 128
    >>> assert color[2] == 0
    >>> color[2] = 240
    >>> assert color[2] == 240
    >>> color[-1] = 0.5
    >>> color
    Rgba(red=128, green=99, blue=240, alpha=0.5)
    >>> color[1] = 299
    Traceback (most recent call last):
        ...
    ValueError: color value must be 0-255, got 299
    >>> color.blue = -65
    Traceback (most recent call last):
        ...
    ValueError: color value must be 0-255, got -65

These examples—and several others—are in the module's function's
docstrings.

### API

**`def editabletuple(classname, *fieldnames, defaults=None, validator=None,
                    doc=None):`**

Creates a new class called `classname` with the given `fieldnames`, optional
``defaults``, optional ``validator``, and optional ``doc`` docstring.

Instances of the class behave almost exactly like
``collections.namedtuple``'s except that fields may be set as well as get
using their index position or fieldname. They support `len()`, `in`, the
comparison operators, and are iterable—which means they can be converted to
a `list` or `tuple` by passing to either's eponymous factory function. They
also provide an `.asdict` property, and also an `update()` method that
accepts _`name=value`_ arguments.

**`def editableobject(classname, *fieldnames, defaults=None, validator=None,
                     doc=None):`**

Creates a new class called `classname` with the given `fieldnames`, optional
``defaults``, optional ``validator``, and optional ``doc`` docstring.

Instances of the class have fields which can get and set by fieldname. They
support the comparison operators and `.astuple` and `.asdict` properties,
the former returning a `tuple` of the instance's values, the latter a `dict`
of fielname-value  items. It also has an `update()` method that accepts
_`name=value`_ arguments.

#### Notes

I can't work out how to make `editabletuple` and `editableobject`
_instances_ picklable. Patches or suggestions on how to do this would be
welcome.

---

**License: GPLv3**
