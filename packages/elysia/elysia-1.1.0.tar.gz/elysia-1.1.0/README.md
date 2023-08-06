# Elysia

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/elysia?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/elysia)
[![PyPI](https://img.shields.io/pypi/v/elysia?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/elysia)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/celsiusnarhwal/elysia?logo=github&color=orange&logoColor=white&style=for-the-badge)](https://github.com/celsiusnarhwal/elysia/releases)
[![PyPI - License](https://img.shields.io/pypi/l/elysia?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/elysia/blob/main/LICENSE.md)
[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)

Elysia is an addon for [_attrs_](https://attrs.org) that provides what I think is a better API for defining instance
attributes than _attrs_' own.

## Installation

```bash
pip install elysia
```

## Usage

Elysia's sole export is the `Fields` class, which wraps `attrs.field`, `attrs.setters`, and `attrs.validators` to
provide a more concise API for defining instance attributes.

Here's a brief example of a class created with _attrs_ and Elysia:

```python
from datetime import datetime

from attrs import define
from elysia import Fields


@define
class User:
    name: str = Fields.field()
    password: str = Fields.field(
        on_setattr=Fields.setters.validate,
        validator=Fields.validators.min_len(8)
    )

    created_at: datetime = Fields.attr(factory=datetime.utcnow, frozen=True)
```

The `User` class has two `__init__` arguments: `name` and `password`. Whenever set, `password` is validated to
ensure it's at least 8 characters long.

`User` also has a `created_at` attribute that can't set via an `__init__` argument. When a `User` object is
instantiated, `created_at` is set to the current time and cannot be changed afterwards.

### So...how does all that work, exactly?

Glad you asked.

There are two ways to define an attribute with Elysia: `Fields.field()` and `Fields.attr()`. `Fields.field()` defines
attributes that map to `__init__` arguments; `Fields.attr()` defines attributes that do not. Both are wrappers around
`attrs.field` and accept all the same arguments. Like `attrs.field`, all arguments to `Fields.field()`
and `Fields.attr()` are keyword-only.

Both methods also accept an optional, boolean, `frozen` argument. Setting it to `True` is a shortcut
for `on_setattr=attrs.setters.frozen` — that is, it freezes the attribute, raising an exception if you try to set it
after initialization.

> **Warning**
>
> Elysia is happy to combine `frozen=True` with anything else you pass to `on_setattr`, but `attrs.setters.frozen`
> will be applied _first_, which may not be what you expect.

Fields also provides access to _attrs_' setters and validators via `Fields.setters` and `Fields.validators`,
respectively. It makes no difference whether setters and validators are accessed through `Fields` or `attrs`. Do what
you like.

## License

Elysia is licensed under the [MIT License](https://github.com/celsiusnarhwal/elysia/blob/main/LICENSE.md).
