---
title: WHO 2 - AUTOMATION
summary: Open Web Net messages for automation system control (shutters, blinds, etc.).
---

[Original Document](/assets/pdf/WHO_2.pdf)

## Introduction

This document describes the Open Web Net Message for WHO = 2 - AUTOMATION. It contains abbreviations, WHAT/DIMENSION/WHERE tables, and allowed OPEN messages for command and event sessions, status requests, dimension writing and requests.

## Abbreviations

| Name               | Description                                         | Range of Values |
|:-------------------|:----------------------------------------------------|:----------------|
| `<shutterStep>`    | Step for moving up/Down advanced shutter           | `[1-99];100`:<br>- `NULL` or `100` -> All opened<br>- `1-99` -> up of the value |
| `<shutterLevel>`   | Level in advanced shutter                          | `[0-100];255`:<br>- `0` -> All closed<br>- `1-99` -> Current position (%)<br>- `100` -> All opened<br>- `255` -> Unknown position |
| `<shutterStatus>`  | State of advanced shutter                          | `[10-14]`:<br>- `10` -> Stop<br>- `11` -> Up<br>- `12` -> Down<br>- `13` -> Step-by-Step Up<br>- `14` -> Step-by-Step Down |
| `<shutterInfo>`    | Device state/configuration for advanced shutter   | `0;[12-15]`:<br>- `0` -> Normal<br>- `12` -> PUL + Disabled<br>- `13` -> Disabled<br>- `14` -> Command not executed<br>- `15` -> PUL |
| `<shutterType>`    | Type of command to manage the priority in advanced shutter | `[0-1]`:<br>- `0` -> Clear priority<br>- `1` -> Set priority |
| `<shutterPriority>` | Priority level for advanced shutter               | Priority values:<br>- `p1` -> Safety priority<br>- `p2` -> High priority<br>- `p3` -> Medium priority<br><br>**Clear priority (shutterType = 0):**<br>- `0,p1=0,p2=0,p3=0` -> No effect on priority<br>- `0,p1=0,p2=0,p3=1` -> Clear Medium priority<br>- `0,p1=0,p2=1,p3=0` -> Clear High priority<br>- `0,p1=0,p2=1,p3=1` -> Clear High priority and medium priority<br>- `0,p1=1,p2=0,p3=0` -> Clear Safety priority<br>- `0,p1=1,p2=0,p3=1` -> Clear Safety priority and Medium priority<br>- `0,p1=1,p2=1,p3=0` -> Clear Safety priority and High priority<br>- `0,p1=1,p2=1,p3=1` -> Clear Safety priority, High priority and Medium priority<br><br>**Set priority (shutterType = 1):**<br>- `1,p1=0,p2=0,p3=0` -> No effect on priority<br>- `1,p1=0,p2=0,p3=1` -> Set Medium priority<br>- `1,p1=0,p2=1,p3=0` -> Set High priority<br>- `1,p1=0,p2=1,p3=1` -> Set High priority and medium priority<br>- `1,p1=1,p2=0,p3=0` -> Set Safety priority<br>- `1,p1=1,p2=0,p3=1` -> Set Safety priority and Medium priority<br>- `1,p1=1,p2=1,p3=0` -> Set Safety priority and High priority<br>- `1,p1=1,p2=1,p3=1` -> Set Safety priority, High priority and Medium priority |

## WHO 2

### WHAT Table

| Value | Description    | Parameters                                          | Set/On Parameters                                   |
|:------|:---------------|:----------------------------------------------------|:----------------------------------------------------|
| 0     | Stop           | -                                                   | -                                                   |
| 1     | Up             | -                                                   | -                                                   |
| 2     | Down           | -                                                   | -                                                   |
| 10    | StopAdvanced   | `[<shutterPriority>]`                               | `<shutterPriority>` `<shutterType>`                 |
| 11    | UpAdvanced     | `[<shutterStep>]` `[<shutterPriority>]`             | `<shutterStep>` `<shutterPriority>` `<shutterType>` |
| 12    | DownAdvanced   | `[<shutterStep>]` `[<shutterPriority>]`             | `<shutterStep>` `<shutterPriority>` `<shutterType>` |

### DIMENSION Table

| Value | Description     |
|:------|:----------------|
| 10    | ShutterStatus   |
| 11    | GoToLevel       |

### WHERE Table

| Address Type | Description    | Value                                                               |
|:-------------|:---------------|:--------------------------------------------------------------------|
| SCS          | General        | `GEN=0`                                                             |
| SCS          | Ambient        | `A=[00, 1-9, 100]`                                                  |
| SCS          | Light Point    | `A; PL` where:<br>- `A=00` -> `PL=[01-15]`<br>- `A=[1-9]` -> `PL=[1-9]`<br>- `A=10` -> `PL=[01-15]`<br>- `A=[01-09]` -> `PL=[10-15]` |
| SCS          | Group          | `GR=#[1-255]`                                                       |
| SCS          | Local bus      | `APL#4#interface` where `Interface -> [0-1][1-9]`                   |

## Command Session - Base Motor Actuator

### Stop - What = 0

| Session Type | Direction        | Open Frame          | Note |
|:-------------|:-----------------|:--------------------|:-----|
| Command      | Client -> Server  | `*2*0*<where>##`    |      |
| Command      | Server -> Client  | ACK                 |      |
| Event        | Server -> Client  | `*2*0*<where>##`    | if `<where>=GR` -> you will have one frame with `<where>=GR` and as many frames as automation objects |

### Up - What = 1

| Session Type | Direction        | Open Frame          | Note |
|:-------------|:-----------------|:--------------------|:-----|
| Command      | Client -> Server  | `*2*1*<where>##`    |      |
| Command      | Server -> Client  | ACK                 |      |
| Event        | Server -> Client  | `*2*1000#<what>##`  | only if `<where>=APL` |
| Event        | Server -> Client  | `*2*1*<where>##`    | if `<where>=GR` -> you will have one frame with `<where>=GR` and as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`    | when the shutter reaches the maximum position<br>if `<where>=GEN,A,GR` -> you will have as many frames as automation objects |

### Down - What = 2

| Session Type | Direction        | Open Frame          | Note |
|:-------------|:-----------------|:--------------------|:-----|
| Command      | Client -> Server  | `*2*2*<where>##`    |      |
| Command      | Server -> Client  | ACK                 |      |
| Event        | Server -> Client  | `*2*1000#<what>##`  | only if `<where>=APL` |
| Event        | Server -> Client  | `*2*2*<where>##`    | if `<where>=GR` -> you will have one frame with `<where>=GR` and as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`    | when the shutter reaches the minimum position<br>if `<where>=GEN,A,GR` -> you will have as many frames as automation objects |

## Command Session - Advanced Motor Actuator

### Stop - What = 0

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*2*0*<where>##`                                                                |      |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*2*1000#<what>*<where>##`                                                      | only if `<where>=APL` |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | if `<where>=GEN,A,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | if `<where>=GEN,A,GR` -> you will have as many frames as automation objects |

### Up - What = 1

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*2*1*<where>##`                                                                |      |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*2*1000#<what>*<where>##`                                                      | only if `<where>=APL` |
| Event        | Server -> Client  | `*2*1*<where>##`                                                                | only if `<where>=GR` |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | only if `<where>=APL`<br>if `<where>=GEN,A,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*1*<where>##`                                                                | when the shutter reaches the maximum position<br>if `<where>=GEN,A,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | when the shutter reaches the maximum position<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | when the shutter reaches the maximum position<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |

### Down - What = 2

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*2*2*<where>##`                                                                |      |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*2*1000#<what>*<where>##`                                                      | only if `<where>=PL` |
| Event        | Server -> Client  | `*2*2*<where>##`                                                                | only if `<where>=GR` |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | only if `<where>=PL`<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*2*<where>##`                                                                | when the shutter reaches the minimum position<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | when the shutter reaches the minimum position<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | when the shutter reaches the minimum position<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |

### StopAdvanced - What = 10

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*2*10*#<shutterPriority>*<where>##`                                            |      |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*2*1000#10#<shutterPriority>#<shutterType>*<where>##`                          | only if `<where>=APL` |
| Event        | Server -> Client  | `*2*10#<shutterPriority>#<shutterType>*<where>##`                              | only if `<where>=A,GEN,GR` |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | if `<where>=A,GEN,GR` as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | if `<where>=A,GEN,GR` as many frames as automation objects |

### UpAdvanced - What = 11

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*2*11#<shutterStep>#<shutterPriority>*<where>##`                               |      |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*2*1000#11#<shutterPriority>#<shutterType>*<where>##`                          | only if `<where>=APL` |
| Event        | Server -> Client  | `*2*11#<shutterStep>#<shutterPriority>#<shutterType>*<where>##`                  | only if `<where>=A,GEN,GR` |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | only if `<where>=APL,GR`<br>if `<where>=GR` -> as many frames as automation objects |
| Event        | Server -> Client  | `*2*1*<where>##`                                                                | only if `<where>=APL,GR`<br>if `<where>=GR` -> as many frames as automation objects |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | when the shutter reaches the maximum position<br>if `<where>=A,GEN,GR` -> as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | when the shutter reaches the maximum position<br>if `<where>=A,GEN,GR` -> as many frames as automation objects |

### DownAdvanced - What = 12

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*2*12#<shutterStep>#<shutterPriority>*<where>##`                               |      |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*2*1000#12#<shutterPriority>#<shutterType>*<where>##`                          | only if `<where>=APL` |
| Event        | Server -> Client  | `*2*12#<shutterStep>#<shutterPriority>#<shutterType>*<where>##`                  | only if `<where>=A,GEN,GR` |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | only if `<where>=APL,GR`<br>if `<where>=GR` -> as many frames as automation objects |
| Event        | Server -> Client  | `*2*2*<where>##`                                                                | only if `<where>=APL, #G`<br>if `<where>=GR` -> as many frames as automation objects |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | when the shutter reaches the minimum position<br>if `<where>=A,GEN,GR` -> as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | when the shutter reaches the minimum position<br>if `<where>=A,GEN,GR` -> as many frames as automation objects |

## Status Request

### Base Motor Actuator

| Session Type | Direction        | Open Frame          | Note |
|:-------------|:-----------------|:--------------------|:-----|
| Command      | Client -> Server  | `*#2*<where>##`     |      |
| Command      | Server -> Client  | `*2*<what>*<where>##` | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Command      | Server -> Client  | ACK                 |      |
| Event        | Server -> Client  | `*2*<what>*<where>##` | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |

### Advanced Motor Actuator

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*#2*<where>##`                                                                 |      |
| Command      | Server -> Client  | `*2*<what>*<where>##`                                                           | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | if `<where>=A,GEN,GR` -> you will have as many frames as light points |
| Event        | Server -> Client  | `*2*<what>*<where>##`                                                           | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |

## Dimension Request

### ShutterStatus - Dimension = 10

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*#2*<where>*10##`                                                              |      |
| Command      | Server -> Client  | `*#2*<where>*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | when the shutter reaches the minimum/maximum position<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |

## Dimension Writing

### GoToLevel - Dimension = 11

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Command      | Client -> Server  | `*#2*<where>*#11#<shutterPriority>*<shutterLevel>##`                            |      |
| Command      | Server -> Client  | ACK                                                                             |      |
| Event        | Server -> Client  | `*#2*<where>*#11#<shutterPriority>#<shutterLevel>*<shutterType>##`               | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*<what>*<where>##`                                                           | when the level has been reached<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | when the level has been reached<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |
| Event        | Server -> Client  | `*2*0*<where>##`                                                                | when the level has been reached<br>if `<where>=A,GEN,GR` -> you will have as many frames as automation objects |

## Event Session

### Automation Status

| Session Type | Direction        | Open Frame           | Note |
|:-------------|:-----------------|:---------------------|:-----|
| Event        | Server -> Client  | `*2*<what>*<where>##` | Standard automation status change event |

### Advanced Shutter Status Change

| Session Type | Direction        | Open Frame                                                                      | Note |
|:-------------|:-----------------|:--------------------------------------------------------------------------------|:-----|
| Event        | Server -> Client  | `*#2*<where>*10*<shutterStatus>*<shutterLevel>*<shutterPriority>*<shutterInfo>##` | Advanced shutter status change with detailed information |

### Command Translation Events

| Session Type | Direction        | Open Frame                                      | Note |
|:-------------|:-----------------|:------------------------------------------------|:-----|
| Event        | Server -> Client  | `*2*1000#<what>*<where>##`                      | Command translation for base motor actuator |
| Event        | Server -> Client  | `*2*1000#<what>#<parameters>*<where>##`         | Command translation for advanced motor actuator |

---

## Copyright Notice

Copyright (C) 2015 [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com). All Rights Reserved.

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
