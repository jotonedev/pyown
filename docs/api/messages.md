---
title: Messages module
summary: Represents all the possible types of messages that can be sent or received.
---

This module represents all the possible types of messages that can be sent or received.

Generally, messages are composed of a series of specific tags, each of which represents a specific piece of information.
They follow the following structure:

```
*tag1*tag2*tag3*tagN##
```

Each tag can have a set of parameters that further define its meaning.


::: pyown.messages.base.parse_message


::: pyown.messages.base.BaseMessage
    options:
        show_inheritance_diagram: true

::: pyown.messages.base.GenericMessage
    options:
        show_inheritance_diagram: true

::: pyown.messages.ack.ACK
    options:
        show_inheritance_diagram: true

::: pyown.messages.nack.NACK
    options:
        show_inheritance_diagram: true


::: pyown.messages.normal.NormalMessage
    options:
        show_inheritance_diagram: true

::: pyown.messages.status.StatusRequest
    options:
        show_inheritance_diagram: true


::: pyown.messages.dimension.DimensionRequest
    options:
        show_inheritance_diagram: true

::: pyown.messages.dimension.DimensionWriting
    options:
        show_inheritance_diagram: true

::: pyown.messages.dimension.DimensionResponse
    options:
        show_inheritance_diagram: true