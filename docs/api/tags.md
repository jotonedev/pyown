---
title: Tags module
summary: Defines all the basic building blocks for every message.
---

This module defines all the basic building blocks for every message.
Each message is composed of a series of tags, each of which represents a specific piece of information.
Tags can be of different types, such as `Who`, `What`, `Where`, `Dimension`, and `Value`.
Each tag can have a set of parameters that further define its meaning.

::: pyown.tags.base.VALID_TAG_CHARS

::: pyown.tags.base.is_valid_tag

::: pyown.tags.base.Tag

::: pyown.tags.base.TagWithParameters
    options:
        show_inheritance_diagram: true


::: pyown.tags.who.Who
    options:
        show_inheritance_diagram: true

::: pyown.tags.what.What
    options:
        show_inheritance_diagram: true

::: pyown.tags.where.Where
    options:
        show_inheritance_diagram: true


::: pyown.tags.dimension.Dimension
    options:
        show_inheritance_diagram: true

::: pyown.tags.base.Value
    options:
        show_inheritance_diagram: true