---
title: WHO 4 - Temperature Control
summary: Open Web Net messages for temperature control and thermoregulation systems.
---

[Original Document](/assets/pdf/WHO_4.pdf)

## Introduction

This document describes the Open Web Net Message for WHO = 4 - Temperature Control. It contains WHAT/DIMENSION/WHERE tables, and allowed OPEN messages for command and event sessions, status requests, dimension writing and requests.

## WHO 4 - Heating Adjustment

### WHAT Table

| Value     | Description                                                 |
|:----------|:------------------------------------------------------------|
| 0         | Conditioning Mode                                           |
| 1         | Heating Mode                                                |
| 102       | Anti Freeze                                                 |
| 202       | Thermal Protection                                          |
| 302       | Protection (generic)                                        |
| 103       | OFF – Heating Mode                                          |
| 203       | OFF – Conditioning Mode                                     |
| 303       | OFF (Generic)                                               |
| 110       | Manual-adjustment Mode – Heating                            |
| 210       | Manual-adjustment Mode – Conditioning                       |
| 310       | Manual-adjustment Mode (Generic)                            |
| 111       | Programming Mode – Heating                                  |
| 211       | Programming Mode - Conditioning                             |
| 311       | Programming Mode (generic)                                  |
| 115       | Holiday daily plan – Heating Mode                           |
| 215       | Holiday daily plan – Conditioning Mode                      |
| 315       | Holiday daily plan                                          |
| 13xxx     | Vacation scenario for xxx days – Heating mode (xxx=0…999)  |
| 23xxx     | Vacation scenario for xxx days – Conditioning mode (xxx=0….999) |
| 33xxx     | Vacation scenario for xxx days (xxx=0….999)                |
| 3000      | Vacation scenario disabled                                  |
| 11xx      | Heating program x (x=1…3)                                   |
| 21xx      | Conditioning program x (x=1…3)                              |
| 31xx      | Last activated program                                      |
| 3100      | Last activated program                                      |
| 12xx      | Scenario xx (xx=1…16)                                       |
| 22xx      | Scenario xx (xx=1...16)                                     |
| 32xx      | Last activated scenario                                     |
| 3200      | Last activated scenario                                     |
| 20        | Remote control disabled                                     |
| 21        | Remote control enabled                                      |
| 22        | At least one probe OFF                                      |
| 23        | At least one probe in Anti Freeze                          |
| 24        | At least one probe in Manual                                |
| 30        | Failure discovered                                          |
| 31        | Central Unit battery KO                                     |
| 40        | Release of sensor local adjustment                          |

### WHERE Table

| Value     | Description                                    |
|:----------|:-----------------------------------------------|
| 0         | General probes (all probes)                   |
| 1         | Zone 1 master probe                           |
| 2         | Zone 2 master probe                           |
| …         | …                                              |
| 10        | Zone 10 master probe                          |
| …         | …                                              |
| 99        | Zone 99 master probe                          |
| 001       | All probes (master and slave) belonging to Zone 1 |
| 002       | All probes (master and slave) belonging to Zone 2 |
| …         | …                                              |
| 010       | All probes (master and slave) belonging to Zone 10 |
| …         | …                                              |
| 099       | All probes (master and slave) belonging to Zone 99 |
| 101       | Probe 1 of Zone 1                             |
| 201       | Probe 2 of Zone 1                             |
| …         | …                                              |
| 801       | Probe 8 of Zone 1                             |
| 102       | Probe 1 of Zone 2                             |
| 202       | Probe 2 of Zone 2                             |
| …         | …                                              |
| 802       | Probe 8 of Zone 2                             |
| …         | …                                              |
| 199       | Probe 1 of Zone 99                            |
| 299       | Probe 2 of Zone 99                            |
| …         | …                                              |
| 899       | Probe 8 of Zone 99                            |
| #0        | Central Unit                                   |
| #1        | Zone 1 via Central Unit                       |
| #2        | Zone 2 via Central Unit                       |
| …         | …                                              |
| #10       | Zone 10 via Central Unit                      |
| …         | …                                              |
| #99       | Zone 99 via Central Unit                      |

### DIMENSION Table

| Value | Description                        | Access |
|:------|:-----------------------------------|:-------|
| 0     | Measures Temperature               | R      |
| 11    | Fan coil Speed                     | R      |
| 12    | Complete probe status              | R      |
| 13    | Local set offset                   | R      |
| 14    | Set Point temperature              | R/W    |
| 19    | Valves status                      | R      |
| 20    | Actuator Status                    | R      |
| 22    | Split Control                      | R/W    |
| 30    | End date Holiday Scenario          | R/W    |

## Zone Setup Commands

### Manual Setting of Zone to Temperature

Set zone to a specific temperature in manual mode.

| Session Type | Direction       | Open Frame                           | Note |
|:-------------|:----------------|:-------------------------------------|:-----|
| Command      | Client → Server | `*#4*#<zone>*#14*<temp>*<mode>##`    | Set zone to temperature |
| Command      | Server → Client | ACK/NACK                             | |
| Event        | Server → Client | `*#4*<zone>*0*<temp>##`              | Temperature reading |
| Event        | Server → Client | `*4*<what>*#<zone>##`                | Operation mode |

Where:

- `<zone>` = [1-99] Zone number
- `<temp>` = Temperature in format CCCC (e.g., "0215" for 21.5°C)
- `<mode>` = 1 (heating), 2 (conditioning), 3 (generic)

### Set Zone in Automatic Mode

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Command      | Client → Server | `*4*311*#<zone>##`  | Set zone to automatic |
| Command      | Server → Client | ACK/NACK            | |
| Event        | Server → Client | `*4*<what>*#<zone>##` | Operation mode |

### Set Zone in OFF Mode

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Command      | Client → Server | `*4*303*#<zone>##`  | Turn off zone |
| Command      | Server → Client | ACK/NACK            | |
| Event        | Server → Client | `*4*303*<zone>##`   | |

### Set Zone in Anti-freeze Mode

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Command      | Client → Server | `*4*102*#<zone>##`  | Set anti-freeze mode |
| Command      | Server → Client | ACK/NACK            | |
| Event        | Server → Client | `*4*102*<zone>##`   | |

### Set Zone in Thermal Protection Mode

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Command      | Client → Server | `*4*202*#<zone>##`  | Set thermal protection |
| Command      | Server → Client | ACK/NACK            | |
| Event        | Server → Client | `*4*202*<zone>##`   | |

### Zone Local Release Probe

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Command      | Client → Server | `*4*40*<zone>##`    | Release local adjustment |
| Command      | Server → Client | ACK/NACK            | |
| Event        | Server → Client | `*4*<what>*<zone>##` | New mode |

## Status Request Commands

### Zone Temperature Request

| Session Type | Direction       | Open Frame               | Note |
|:-------------|:----------------|:-------------------------|:-----|
| Command      | Client → Server | `*#4*<zone>*0##`         | Request temperature |
| Command      | Server → Client | `*#4*<zone>*0*<temp>##`  | Temperature value |
| Command      | Server → Client | ACK                      | |

### Fan Coil Speed Request

| Session Type | Direction       | Open Frame                | Note |
|:-------------|:----------------|:--------------------------|:-----|
| Command      | Client → Server | `*#4*<zone>*11##`         | Request fan speed |
| Command      | Server → Client | `*#4*<zone>*11*<speed>##` | Speed value |
| Command      | Server → Client | ACK                       | |

Speed values:

- 0 = Auto
- 1 = Speed 1
- 2 = Speed 2  
- 3 = Speed 3
- 15 = OFF

### Zone Complete Status Request

| Session Type | Direction       | Open Frame                   | Note |
|:-------------|:----------------|:-----------------------------|:-----|
| Command      | Client → Server | `*#4*<zone>##`               | Request all zone info |
| Command      | Server → Client | `*#4*<zone>*0*<temp>##`      | Temperature |
| Command      | Server → Client | `*#4*<zone>*12*<temp>*3##`   | Adjusted temperature |
| Command      | Server → Client | `*4*<what>*<zone>##`         | Operation mode |
| Command      | Server → Client | `*#4*<zone>*13*<offset>##`   | Local offset |
| Command      | Server → Client | `*#4*<zone>*14*<setpoint>*3##` | Set point |
| Command      | Server → Client | ACK                          | |

### Zone Set Point Temperature Request

| Session Type | Direction       | Open Frame                     | Note |
|:-------------|:----------------|:-------------------------------|:-----|
| Command      | Client → Server | `*#4*<zone>*14##`              | Request set point |
| Command      | Server → Client | `*#4*<zone>*14*<temp>*3##`     | Set point temperature |
| Command      | Server → Client | ACK                            | |

### Zone Valves Status Request

| Session Type | Direction       | Open Frame                      | Note |
|:-------------|:----------------|:--------------------------------|:-----|
| Command      | Client → Server | `*#4*<zone>*19##`               | Request valve status |
| Command      | Server → Client | `*#4*<zone>*19*<CV>*<HV>##`     | Valve status |
| Command      | Server → Client | ACK                             | |

Valve status values:

- 0 = OFF
- 1 = ON
- 2 = Opened
- 3 = Closed
- 4 = Stop
- 5 = OFF Fan Coil
- 6 = ON speed 1
- 7 = ON speed 2
- 8 = ON speed 3

## Central Unit Commands

### Manual Setting of Central Unit

| Session Type | Direction       | Open Frame                      | Note |
|:-------------|:----------------|:--------------------------------|:-----|
| Command      | Client → Server | `*#4*#0*#14*<temp>*<mode>##`    | Set central unit temperature |
| Command      | Server → Client | ACK/NACK                        | |
| Event        | Server → Client | `*4*<what>*#0##`                | Operation mode |

### Set Central Unit OFF

| Session Type | Direction       | Open Frame     | Note |
|:-------------|:----------------|:---------------|:-----|
| Command      | Client → Server | `*4*303*#0##`  | Turn off central unit |
| Command      | Server → Client | ACK/NACK       | |
| Event        | Server → Client | `*4*303*#0##`  | |

### Weekly Program Activation

| Session Type | Direction       | Open Frame           | Note |
|:-------------|:----------------|:---------------------|:-----|
| Command      | Client → Server | `*4*<program>*#0##`  | Activate weekly program |
| Command      | Server → Client | ACK/NACK             | |
| Event        | Server → Client | `*4*<program>*#0##`  | |

Program values:

- 1101-1103 = Heating programs 1-3
- 2101-2103 = Conditioning programs 1-3
- 3101-3103 = Generic programs 1-3

### Scenario Activation

| Session Type | Direction       | Open Frame           | Note |
|:-------------|:----------------|:---------------------|:-----|
| Command      | Client → Server | `*4*<scenario>*#0##` | Activate scenario |
| Command      | Server → Client | ACK/NACK             | |
| Event        | Server → Client | `*4*<scenario>*#0##` | |

Scenario values:

- 1201-1216 = Heating scenarios 1-16
- 2201-2216 = Conditioning scenarios 1-16
- 3201-3216 = Generic scenarios 1-16

### Holiday Mode Commands

#### Holiday Mode with Weekly Program Return

| Session Type | Direction       | Open Frame                    | Note |
|:-------------|:----------------|:------------------------------|:-----|
| Command      | Client → Server | `*4*115#<program>*#0##`       | Heating holiday mode |
| Command      | Client → Server | `*4*215#<program>*#0##`       | Conditioning holiday mode |
| Command      | Client → Server | `*4*315#<program>*#0##`       | Generic holiday mode |
| Command      | Server → Client | ACK/NACK                      | |

#### N Days Holiday Mode

| Session Type | Direction       | Open Frame                      | Note |
|:-------------|:----------------|:--------------------------------|:-----|
| Command      | Client → Server | `*4*<days>#<program>*#0##`      | N days holiday |
| Command      | Server → Client | ACK/NACK                        | |

Where:

- `<days>` = 13001-13255 (heating), 23001-23255 (conditioning), 33001-33255 (generic)
- `<program>` = 3101-3103

### Holiday Mode Deactivation

| Session Type | Direction       | Open Frame              | Note |
|:-------------|:----------------|:------------------------|:-----|
| Command      | Client → Server | `*4*3000*#0##`          | Deactivate holiday mode |
| Command      | Client → Server | `*4*3000#<program>*#0##`| Deactivate with specific program |
| Command      | Server → Client | ACK/NACK                | |

### Set Holiday Deadline

#### Set Holiday Date

| Session Type | Direction       | Open Frame                          | Note |
|:-------------|:----------------|:------------------------------------|:-----|
| Command      | Client → Server | `*#4*#0*#30*<day>*<month>*<year>##` | Set holiday end date |
| Command      | Server → Client | ACK/NACK                            | |

#### Set Holiday Time

| Session Type | Direction       | Open Frame                       | Note |
|:-------------|:----------------|:---------------------------------|:-----|
| Command      | Client → Server | `*#4*#0*#31*<hour>*<minutes>##`  | Set holiday end time |
| Command      | Server → Client | ACK/NACK                         | |

## Central Unit Status Requests

### Zone Operation Mode Request

| Session Type | Direction       | Open Frame            | Note |
|:-------------|:----------------|:----------------------|:-----|
| Command      | Client → Server | `*#4*#<zone>##`       | Request zone mode via central unit |
| Command      | Server → Client | `*4*<what>*#<zone>##` | Zone operation mode |
| Command      | Server → Client | ACK                   | |

### Central Unit Operation Mode Request

| Session Type | Direction       | Open Frame        | Note |
|:-------------|:----------------|:------------------|:-----|
| Command      | Client → Server | `*#4*#0##`        | Request central unit mode |
| Command      | Server → Client | `*4*<what>*#0##`  | Central unit mode |
| Command      | Server → Client | ACK               | |

### Holiday Deadline Requests

#### Holiday Date Request

| Session Type | Direction       | Open Frame                          | Note |
|:-------------|:----------------|:------------------------------------|:-----|
| Command      | Client → Server | `*#4*#0*30##`                       | Request holiday end date |
| Command      | Server → Client | `*#4*#0*30*<day>*<month>*<year>##`  | Holiday end date |
| Command      | Server → Client | ACK                                 | |

#### Holiday Time Request

| Session Type | Direction       | Open Frame                       | Note |
|:-------------|:----------------|:---------------------------------|:-----|
| Command      | Client → Server | `*#4*#0*31##`                    | Request holiday end time |
| Command      | Server → Client | `*#4*#0*31*<hour>*<minutes>##`   | Holiday end time |
| Command      | Server → Client | ACK                              | |

## Split Control Commands

### Split Control Request (Dimension 22)

| Session Type | Direction       | Open Frame                                | Note |
|:-------------|:----------------|:------------------------------------------|:-----|
| Command      | Client → Server | `*#4*3#<zone>#<actuator>*22##`            | Request split status |
| Command      | Server → Client | `*#4*3#<zone>#<actuator>*22*<mode>*<sp>*<vel>*<swing>##` | Split status |
| Command      | Server → Client | ACK                                       | |

### Split Control Set (Dimension 22)

| Session Type | Direction       | Open Frame                                | Note |
|:-------------|:----------------|:------------------------------------------|:-----|
| Command      | Client → Server | `*#4*3#<zone>#<actuator>*#22*<mode>*<sp>*<vel>*<swing>##` | Set split parameters |
| Command      | Server → Client | ACK/NACK                                  | |

Split parameters:

- `<mode>`: 0=Off, 1=Winter, 2=Summer, 3=Fan, 4=Dehumidification, 5=Auto
- `<sp>`: Set point temperature (000-1270 representing 0.0°C to 127.0°C in 0.5°C steps)
- `<vel>`: 0=Auto, 1=Min, 2=Medium, 3=Max, 4=Silent
- `<swing>`: 0=Off, 1=On

## Event Session Messages

### Zone Temperature Change

| Session Type | Direction       | Open Frame              | Note |
|:-------------|:----------------|:------------------------|:-----|
| Event        | Server → Client | `*#4*<zone>*0*<temp>##` | Temperature reading |

### Zone Operation Mode Change

| Session Type | Direction       | Open Frame            | Note |
|:-------------|:----------------|:----------------------|:-----|
| Event        | Server → Client | `*4*<what>*<zone>##`  | Zone mode change |

### Central Unit Mode Change

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Event        | Server → Client | `*4*<what>*#0##`    | Central unit mode change |

### Split Status Change

| Session Type | Direction       | Open Frame                                | Note |
|:-------------|:----------------|:------------------------------------------|:-----|
| Event        | Server → Client | `*#4*3#<zone>#<actuator>*22*<mode>*<sp>*<vel>*<swing>##` | Split status change |

## WHO 1004 - Temperature Control Diagnostics

### WHERE Table (Diagnostics)

| Value | Description                |
|:------|:---------------------------|
| 1-99  | Zone 1-99 master probe    |
| #0    | Central unit               |
| #1-99 | Zone 1-99 via central unit|

### DIMENSION Table (Diagnostics)

| Value | Description                              | Access |
|:------|:-----------------------------------------|:-------|
| 7     | Central Unit Diagnostic                  | R      |
| 11    | Central Unit Auto diagnostic             | R      |
| 20    | Probe diagnostic (only zones with failures) | R   |
| 21    | Probe diagnostic (all zones)             | R      |
| 22    | Auto diagnostic of failures              | R      |
| 23    | Number of zone with failures             | R      |

### Diagnostic Commands

#### Central Unit Diagnostic Request

| Session Type | Direction       | Open Frame               | Note |
|:-------------|:----------------|:-------------------------|:-----|
| Command      | Client → Server | `*#1004*#0*7##`          | Request central unit diagnostic |
| Command      | Server → Client | `*#1004*#0*7*<bits>##`   | Diagnostic bits |
| Command      | Server → Client | ACK                      | |

#### Zone Diagnostic Request

| Session Type | Direction       | Open Frame                    | Note |
|:-------------|:----------------|:------------------------------|:-----|
| Command      | Client → Server | `*#1004*#<zone>*21##`         | Request zone diagnostic |
| Command      | Server → Client | `*#1004*#<zone>*21*<bits>##`  | Diagnostic bits |
| Command      | Server → Client | ACK                           | |

#### Failure Count Request

| Session Type | Direction       | Open Frame                              | Note |
|:-------------|:----------------|:----------------------------------------|:-----|
| Command      | Client → Server | `*#1004*#0*23##`                        | Request failure count |
| Command      | Server → Client | `*#1004*#0*23*<no_answer>*<failures>##` | Failure counts |
| Command      | Server → Client | ACK                                     | |

### Diagnostic Event Messages

#### Central Unit Diagnostic

| Session Type | Direction       | Open Frame               | Note |
|:-------------|:----------------|:-------------------------|:-----|
| Event        | Server → Client | `*#1004*#0*7*<bits>##`   | Central unit diagnostic |
| Event        | Server → Client | `*#1004*#0*11*<bits>##`  | Central unit auto-diagnostic |

#### Zone Diagnostic

| Session Type | Direction       | Open Frame                    | Note |
|:-------------|:----------------|:------------------------------|:-----|
| Event        | Server → Client | `*#1004*#<zone>*21*<bits>##`  | Zone diagnostic |
| Event        | Server → Client | `*#1004*#<zone>*22*<bits>##`  | Zone auto-diagnostic |

#### Failure Count

| Session Type | Direction       | Open Frame                              | Note |
|:-------------|:----------------|:----------------------------------------|:-----|
| Event        | Server → Client | `*#1004*#0*23*<no_answer>*<failures>##` | Failure count change |

## Temperature Format

Temperature values are represented as 4-digit strings:

- Format: `c1c2c3c4`
- `c1` = Always 0 (positive temperature indicator)
- `c2c3` = Temperature integer part (05-40 for set points, 00-50 for measurements)
- `c4` = Decimal part (0.1°C step for measurements, 0.5°C step for set points)

Examples:

- `0215` = 21.5°C
- `0200` = 20.0°C
- `0055` = 5.5°C

## Local Offset Values

Local offset represents the knob position on thermostats:

| Value | Description    |
|:------|:---------------|
| 00    | Knob on 0      |
| 01    | Knob on +1°C   |
| 11    | Knob on -1°C   |
| 02    | Knob on +2°C   |
| 12    | Knob on -2°C   |
| 03    | Knob on +3°C   |
| 13    | Knob on -3°C   |
| 4     | Local OFF      |
| 5     | Local protection |

---

## Copyright Notice

Copyright (C) 2013 [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com). All Rights Reserved.

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
