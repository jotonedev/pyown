---
title: WHO 0 - Scenarios
summary: Open frames implementation for Scenario scheduling through Scenarios modules.
---

[Original Document](/assets/pdf/WHO_0.pdf)

## Introduction

In this document you can find the Open frames which implement the Scenario scheduling through the Scenarios modules (F420/IR 3456).

## Compatible Hardware

| Brand     | Item             | Description                |
|:----------|:-----------------|:---------------------------|
| Legrand   | 03551            | Scenario module F420       |
|           | 88301            | IR interface 3456          |
| BTicino   | F420             | Scenario module            |
|           | IR interface 3456| IR interface               |

## Table WHAT

| Value | Description                          | Notes                      |
|:------|:-------------------------------------|:---------------------------|
| 1     | Scenario 1*                          |                            |
| 2     | Scenario 2*                          |                            |
| 3     | Scenario 3*                          |                            |
| 4     | Scenario 4*                          |                            |
| ...   | ...                                  |                            |
| 16    | Scenario 16*                         |                            |
| ...   | ...                                  |                            |
| 20    | Scenario 20**                        |                            |
|       | **Commands only for F420**           |                            |
| 40#X  | Start recording X scenario           | X = scenario number (1-16) |
| 41#X  | End recording X scenario             | X = scenario number (1-16) |
| 42    | Erase all the scenarios              |                            |
| 42#X  | Erase X scenario                     | X = scenario number (1-16) |
| 43    | Lock Scenarios central unit          |                            |
| 44    | Unlock Scenarios central unit        |                            |
| 45    | Unavailable Scenarios central unit   |                            |
| 46    | Memory full of Scenarios central unit|                            |

## Table WHERE

| Value | Description       |
|:------|:------------------|
| 01    | Control Panel 01  |
| 02    | Control Panel 02  |
| ...   | ...               |
| 99    | Control Panel 99  |

## Open Messages: Commands Session

### Scenario Activation Command (WHAT 1-16/20)

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Commands     | Client → Server| `*0*WHAT*WHERE##`     | **WHAT**: Enable selected scenario (1-16/20)                      |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |
| Commands     | Server → Client| `*#*1##` or `*#*0##`  | ACK: command sent to Bus / NACK: command not sent to Bus          |
| Events       | Server → Client| `*0*WHAT*WHERE##`     | Event notification                                                 |

> **Note**: For the module F420 (03551) it is available the configuration up to 16 different scenarios; on the other side the IR 3456 (88301) interface can handle up to 20 scenarios.

## Commands Only for Scenarios Module F420

> **Important**: Whether you have to program the scenario module you have to open a specific connection with this frame `*99*9##` (read the document OpenWebNet_introduction)

### Start Recording Scenarios (WHAT 40#1-40#20)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Commands     | Client → Server| `*0*40#X*WHERE##`     | Enable selected scenario X = (1-16)                               |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |
| Commands     | Server → Client| `*#*1##` or `*#*0##`  | ACK: command sent to Bus / NACK: command not sent to Bus          |
| Events       | Server → Client| `*0*40#X*WHERE##`     | Event notification                                                 |

### End Recording Scenarios (WHAT 41#1-41#20)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Commands     | Client → Server| `*0*41#X*WHERE##`     | Disable selected scenario X = (1-16)                              |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |
| Commands     | Server → Client| `*#*1##` or `*#*0##`  | ACK: command sent to Bus / NACK: command not sent to Bus          |
| Events       | Server → Client| `*0*41#X*WHERE##`     | Event notification                                                 |

### Erase All Scenarios (WHAT 42)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Commands     | Client → Server| `*0*42*WHERE##`       | Erase all scenarios                                                |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |
| Commands     | Server → Client| `*#*1##` or `*#*0##`  | ACK: command sent to Bus / NACK: command not sent to Bus          |
| Events       | Server → Client| `*0*42*WHERE##`       | Event notification                                                 |

### Erase Single Scenario X (WHAT 42#1-42#20)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Commands     | Client → Server| `*0*42#X*WHERE##`     | Erase the selected scenario X = (1-16)                            |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |
| Commands     | Server → Client| `*#*1##` or `*#*0##`  | ACK: command sent to Bus / NACK: command not sent to Bus          |
| Events       | Server → Client| `*0*42#X*WHERE##`     | Event notification                                                 |

### Lock Scenario Central Unit (WHAT 43)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Commands     | Client → Server| `*0*43*WHERE##`       | Lock scenarios central unit                                        |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |
| Commands     | Server → Client| `*#*1##` or `*#*0##`  | ACK: command sent to Bus / NACK: command not sent to Bus          |
| Events       | Server → Client| `*0*43*WHERE##`       | Event notification                                                 |

### Unlock Scenarios Central Unit (WHAT 44)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Commands     | Client → Server| `*0*44*WHERE##`       | Unlock scenarios central unit                                      |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |
| Commands     | Server → Client| `*#*1##` or `*#*0##`  | ACK: command sent to Bus / NACK: command not sent to Bus          |
| Events       | Server → Client| `*0*44*WHERE##`       | Event notification                                                 |


## Open Messages: Events Sessions

### Enable Scenarios (WHAT 1-16/20)

> **Note**: For the module F420 (03551) it is available the configuration up to 16 different scenarios; on the other side the IR 3456 (88301) interface can handle up to 20 scenarios.

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Events       | Server → Client| `*0*WHAT*WHERE##`     | Enable selected scenario (1-16)                                   |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |

### Start Programming Scenarios (WHAT 40#1 – 40#16)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Events       | Server → Client| `*0*40#X*WHERE##`     | Start programming the selected scenario X = (1-16)                |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |

### End Programming Scenarios (WHAT 41#1 – 41#16)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Events       | Server → Client| `*0*41#X*WHERE##`     | End programming the selected scenario X = (1-16)                  |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |

### Erase All Scenarios (WHAT 42)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Events       | Server → Client| `*0*42*WHERE##`       | Erase all the scenarios                                            |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |

### Erase Single Scenario X (WHAT 42#1-42#16)

> **Note**: Only with F420 (03551) because the 3456 (88301) module doesn't support this frame

| Session Type | Direction      | Open Frame            | Notes                                                              |
|:-------------|:---------------|:----------------------|:-------------------------------------------------------------------|
| Events       | Server → Client| `*0*42#X*WHERE##`     | Erase the selected scenario X = (1-16)                            |
|              |                |                       | **WHERE**: 01-99 (Scenario module Point to Point)                 |
|              |                |                       | **WHERE**: 01-99#4#I (Scenario module on Local Bus level 4 with Interface I) |

## Notes

- In the F420 (03551) it is possible to program up to 16 scenarios.
- In the IR 3456 (88301) it is possible to recall up to 20 different scenarios.

---

## Copyright Notice

Copyright (C) 2010 [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com). All Rights Reserved.

## License

By using and/or copying this document, you (the licensee) agree that you have read, understood, and will comply with the following terms and conditions:

Permission to copy, and distribute the contents of this document, in any medium for any purpose and without fee or royalty is hereby granted, provided that you include the following on ALL copies of the document, or portions thereof, that you use:

- A link or URL to the [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com).
- The copyright notice of the original author, or if it doesn't exist, a notice (hypertext is preferred, but a textual representation is permitted) of the form: "Copyright (C) [date-of-document] [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com). All Rights Reserved.

When space permits, inclusion of the full text of this NOTICE should be provided. We request that authorship attribution be provided in any software, documents, or other items or products that you create pursuant to the implementation of the contents of this document, or any portion thereof.

Any contributions to the document (i.e. translation, modifications, improvements, etc) has to be submitted to and accepted by the My Open staff (using the forum of the community or sending an email via the [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com) dedicated section) . Once the improvement has been accepted the new release will be published in the My Open Community web site.

## Disclaimers

THIS DOCUMENT IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, OR TITLE; THAT THE CONTENTS OF THE DOCUMENT ARE SUITABLE FOR ANY PURPOSE; NOR THAT THE IMPLEMENTATION OF SUCH CONTENTS WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE DOCUMENT OR THE PERFORMANCE OR IMPLEMENTATION OF THE CONTENTS THEREOF.

The name and trademarks of copyright holders may NOT be used in advertising or publicity pertaining to this document or its contents without specific, written prior permission. Title to copyright in this document will at all times remain with copyright holders.
