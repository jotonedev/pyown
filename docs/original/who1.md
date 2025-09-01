---
title: WHO 1 - LIGHTING
summary: Open Web Net messages for lighting system control and monitoring.
---

[Original Document](/assets/pdf/WHO_1.pdf)

## Introduction

This document describes the Open Web Net Message for WHO = 1 - LIGHTING. It contains abbreviations, WHAT/DIMENSION/WHERE tables, and allowed OPEN messages for command and event sessions, status requests, dimension writing and requests.

## Abbreviations

| Name              | Description                                         | Range of Values |
|:------------------|:----------------------------------------------------|:----------------|
| `<dimmerSpeed>`   | Turn off (or on) the light at a pre-established speed | `[0-255]`:<br>- 0 -> Last speed used<br>- 1-254 -> Actual speed<br>- 255 -> Default speed |
| `<dimmerLevel10>` | Dimmer's level                                      | `[2-10]`:<br>- 2 -> 20%<br>- 3 -> 30%<br>- 4 -> 40%<br>- 5 -> 50%<br>- 6 -> 60%<br>- 7 -> 70%<br>- 8 -> 80%<br>- 9 -> 90%<br>- 10 -> 100% |
| `<dimmerLevel100>` | The increase of the luminosity intensity of the light point; expressed as a percentage value | `[100-200]`:<br>- 100 -> Switching off<br>- 200 -> Maximum luminosity intensity |
| `<hour>`          | It indicates how many hours the actuator has to stay ON | `[0-255]` |
| `<min>`           | It indicates how many minutes the actuator has to stay ON | `[0-59]` |
| `<sec>`           | It indicates how many seconds the actuator has to stay ON | `[0-59]` |
| `<status>`        | It indicates the status of actuator or dimmer       | `[0-1]`:<br>- 0 -> OFF<br>- 1 -> ON |
| `<workingTime>`   | The working time of the device in hours             | `[1-100000]` |
| `<hue>`           | It indicates the Hue value of RGB light             | `[0-359]` |
| `<saturation>`    | It indicates the Saturation value of RGB light      | `[0-100]` |
| `<value>`         | It indicates the value (brightness of the color) of RGB light | `[0-100]` |
| `<wt>`            | It indicates the white temperature value of tunable white light in Mirek | `[1-65534]` |

## WHO 1

### WHAT Table

| Value    | Description                                           |
|:---------|:------------------------------------------------------|
| 0        | Turn off                                              |
| 0#x      | Turn off at x speed for step                          |
| 1        | Turn on                                               |
| 1#x      | Turn on at x speed for step                           |
| 2        | 20%                                                   |
| 3        | 30%                                                   |
| 4        | 40%                                                   |
| 5        | 50%                                                   |
| 6        | 60%                                                   |
| 7        | 70%                                                   |
| 8        | 80%                                                   |
| 9        | 90%                                                   |
| 10       | 100%                                                  |
| 11       | ON timed 1 Min                                        |
| 12       | ON timed 2 Min                                        |
| 13       | ON timed 3 Min                                        |
| 14       | ON timed 4 Min                                        |
| 15       | ON timed 5 Min                                        |
| 16       | ON timed 15 Min                                       |
| 17       | ON timed 30 Sec                                       |
| 18       | ON timed 0.5 Sec                                      |
| 20       | Blinking on 0.5 sec                                   |
| 21       | Blinking on 1 sec                                     |
| 22       | Blinking on 1.5 sec                                   |
| 23       | Blinking on 2 sec                                     |
| 24       | Blinking on 2.5 sec                                   |
| 25       | Blinking on 3 sec                                     |
| 26       | Blinking on 3.5 sec                                   |
| 27       | Blinking on 4 sec                                     |
| 28       | Blinking on 4.5 sec                                   |
| 29       | Blinking on 5 sec                                     |
| 30       | Up one level                                          |
| 30#x#y   | Up of x levels at y speed for step                    |
| 31       | Down one level                                        |
| 31#x#y   | Down of x levels at y speed for step                  |
| 1000     | It accepts a parameter that is the value of what table |

### DIMENSION Table

| Value | Description                                      |
|:------|:-------------------------------------------------|
| 1     | Set up the level at X speed                      |
| 2     | Temporization                                    |
| 3     | Required Only ON Light                           |
| 4     | Status dimmer 100 levels with ON/OFF speed      |
| 8     | Working time lamp                                |
| 9     | Max working time lamp                            |
| 12    | HSV* (only with F461 and RGB Lights)            |
| 14    | White Temperature* (only with F461 and Tunable White Lights) |

### WHERE Table

| Description    | Value |
|:---------------|:------|
| Interface      | Int = I3I4:<br>- I3 = 0; I4 [1-9]<br>- I3 = 1; I4 [1-5] |
| General        | - 0 -> General of system<br>- 0#4#<Int> -> General of local bus |
| Area           | A [00, 1-9, 100]:<br>- <A> -> Area of private riser<br>- <A>#4#<Int> -> Area of local bus |
| Group          | G [1-255]:<br>- #<G> -> Group of private riser<br>- #<G>#4#<Int> -> Group of local bus |
| Point to point | A; PL:<br>- A = 00; PL [01-15]<br>- A [1-9]; PL [1-9]<br>- A = 10; PL [01-15]<br>- A [01-09]; PL [10-15]<br>- <A><PL> -> Point to point of private riser<br>- <A><PL>#4#<Int> -> Point to point of local bus |

## Command Session - Light Devices

### Turn OFF - What = 0

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*0*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*0*<where>##`    |

### Turn ON - What = 1

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*1*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*1*<where>##`    |

### ON timed 1 min - What = 11

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*11*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### ON timed 2 min - What = 12

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*12*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### ON timed 3 min - What = 13

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*13*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### ON timed 4 min - What = 14

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*14*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### ON timed 5 min - What = 15

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*15*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### ON timed 15 min - What = 16

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*16*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### ON timed 30 sec - What = 17

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*17*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### ON timed 0.5 sec - What = 18

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*1*18*<where>##`        |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*1*<where>##`         |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### Blinking Commands

#### Blinking on 0.5 sec - What = 20

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*20*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*20*<where>##`   |

#### Blinking on 1 sec - What = 21

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*21*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*21*<where>##`   |

#### Blinking on 1.5 sec - What = 22

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*22*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*22*<where>##`   |

#### Blinking on 2 sec - What = 23

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*23*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*23*<where>##`   |

#### Blinking on 2.5 sec - What = 24

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*24*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*24*<where>##`   |

#### Blinking on 3 sec - What = 25

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*25*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*25*<where>##`   |

#### Blinking on 3.5 sec - What = 26

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*26*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*26*<where>##`   |

#### Blinking on 4 sec - What = 27

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*27*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*27*<where>##`   |

#### Blinking on 4.5 sec - What = 28

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*28*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*28*<where>##`   |

#### Blinking on 5 sec - What = 29

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*29*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*29*<where>##`   |

### Command translation - What = 1000

| Session Type | Direction       | Open Frame                     | Note |
|:-------------|:----------------|:-------------------------------|:-----|
| Command      | Client -> Server | `*1*1000#<what>*<where>##`     | This command is valid for dimmer too |
| Command      | Server -> Client | ACK                            |      |
| Event        | Server -> Client | `*1*1000#<what>*<where>##`     |      |

## Command Session - Dimmer/RGB/White Temperature Devices

### Turn OFF - What = 0

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*0*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*0*<where>##`    |

### Turn ON - What = 1

| Session Type | Direction       | Open Frame                    |
|:-------------|:----------------|:------------------------------|
| Command      | Client -> Server | `*1*1*<where>##`              |
| Command      | Server -> Client | ACK                           |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##` |

### Turn OFF at x SPEED for step - What = 0#

| Session Type | Direction       | Open Frame                                        |
|:-------------|:----------------|:--------------------------------------------------|
| Command      | Client -> Server | `*1*0#<dimmerSpeed>*<where>##`                   |
| Command      | Server -> Client | ACK                                               |
| Event        | Server -> Client | `*#1*<where>*1*<dimmerLevel100>*<dimmerSpeed>##` |

### Turn ON at x SPEED - What = 1#

| Session Type | Direction       | Open Frame                                        |
|:-------------|:----------------|:--------------------------------------------------|
| Command      | Client -> Server | `*1*1#<dimmerSpeed>*<where>##`                   |
| Command      | Server -> Client | ACK                                               |
| Event        | Server -> Client | `*#1*<where>*1*<dimmerLevel100>*<dimmerSpeed>##` |

### Dimmer Level Commands

#### 20% - What = 2

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*2*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*2*<where>##`    |

#### 30% - What = 3

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*3*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*3*<where>##`    |

#### 40% - What = 4

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*4*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*4*<where>##`    |

#### 50% - What = 5

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*5*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*5*<where>##`    |

#### 60% - What = 6

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*6*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*6*<where>##`    |

#### 70% - What = 7

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*7*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*7*<where>##`    |

#### 80% - What = 8

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*8*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*8*<where>##`    |

#### 90% - What = 9

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*9*<where>##`    |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*9*<where>##`    |

#### 100% - What = 10

| Session Type | Direction       | Open Frame          |
|:-------------|:----------------|:--------------------|
| Command      | Client -> Server | `*1*10*<where>##`   |
| Command      | Server -> Client | ACK                 |
| Event        | Server -> Client | `*1*10*<where>##`   |

### Dimmer Timed Commands

#### ON timed 1 min - What = 11

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*11*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*11*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

#### ON timed 2 min - What = 12

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*12*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*12*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

#### ON timed 3 min - What = 13

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*13*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*13*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

#### ON timed 4 min - What = 14

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*14*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*14*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

#### ON timed 5 min - What = 15

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*15*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*15*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

#### ON timed 15 min - What = 16

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*16*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*16*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

#### ON timed 30 sec - What = 17

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*17*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*17*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

#### ON timed 0.5 sec - What = 18

| Session Type | Direction       | Open Frame                         |
|:-------------|:----------------|:-----------------------------------|
| Command      | Client -> Server | `*1*18*<where>##`                  |
| Command      | Server -> Client | ACK                                |
| Event        | Server -> Client | `*1*18*<where>##`                  |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##`     |
| Event        | Server -> Client | `*1*<status>*<where>##`            |

### Level Control Commands

#### Up one level - What = 30

| Session Type | Direction       | Open Frame                              |
|:-------------|:----------------|:----------------------------------------|
| Command      | Client -> Server | `*1*30*<where>##`                       |
| Command      | Server -> Client | ACK                                     |
| Event        | Server -> Client | `*1*<dimmerLevel10 + 1>*<where>##`      |

#### Up of x levels at y SPEED for step - What = 30#x#y

| Session Type | Direction       | Open Frame                                        |
|:-------------|:----------------|:--------------------------------------------------|
| Command      | Client -> Server | `*1*30#<dimmerLevel10>#<dimmerSpeed>*<where>##`  |
| Command      | Server -> Client | ACK                                               |
| Event        | Server -> Client | `*#1*<where>*1*<dimmerLevel100>*<dimmerSpeed>##` |

#### Down one level - What = 31

| Session Type | Direction       | Open Frame                              |
|:-------------|:----------------|:----------------------------------------|
| Command      | Client -> Server | `*1*31*<where>##`                       |
| Command      | Server -> Client | ACK                                     |
| Event        | Server -> Client | `*1*<dimmerLevel10 - 1>*<where>##`      |

#### Down of x levels at y SPEED for step - What = 31#x#y

| Session Type | Direction       | Open Frame                                        |
|:-------------|:----------------|:--------------------------------------------------|
| Command      | Client -> Server | `*1*31#<dimmerLevel10>#<dimmerSpeed>*<where>##`  |
| Command      | Server -> Client | ACK                                               |
| Event        | Server -> Client | `*#1*<where>*1*<dimmerLevel100>*<dimmerSpeed>##` |

## Status Request

### Light status request command

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*#1*<where>##`          |
| Command      | Server -> Client | `*1*<status>*<where>##`  |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*1*<status>*<where>##`  |

### Dimmer/RGB/Tunable White status request command

| Session Type | Direction       | Open Frame                    |
|:-------------|:----------------|:------------------------------|
| Command      | Client -> Server | `*#1*<where>##`               |
| Command      | Server -> Client | `*1*<dimmerLevel10>*<where>##` |
| Command      | Server -> Client | ACK                           |
| Event        | Server -> Client | `*1*<dimmerLevel10>*<where>##` |

## Dimension Writing

### Set up the level at X speed - Dimension = 1

| Session Type | Direction       | Open Frame                                        |
|:-------------|:----------------|:--------------------------------------------------|
| Command      | Client -> Server | `*#1*<where>#1*<dimmerLevel100>*<dimmerSpeed>##` |
| Command      | Server -> Client | ACK                                               |
| Event        | Server -> Client | `*#1*<where>*1*<dimmerLevel100>*<dimmerSpeed>##` |

### Temporization command - Dimension = 2

| Session Type | Direction       | Open Frame                                       |
|:-------------|:----------------|:-------------------------------------------------|
| Command      | Client -> Server | `*#1*<where>*#2*<hour>*<min>*<sec>##`           |
| Command      | Server -> Client | ACK                                              |
| Event        | Server -> Client | `*1*<status>*<where>##`                         |
| Event        | Server -> Client | `*#1*<where>*#2*<dimmerLevel100>*<dimmerSpeed>##` (only for dimmer) |

### Max working time lamp - Dimension = 9

| Session Type | Direction       | Open Frame                        |
|:-------------|:----------------|:----------------------------------|
| Command      | Client -> Server | `*#1*<where>*#9*<workingTime>##`  |
| Command      | Server -> Client | ACK                               |
| Event        | Server -> Client | `*#1*<where>*#9*<workingTime>##`  |

### HSV command - Dimension = 12 [only for RGB Lights]

| Session Type | Direction       | Open Frame                                   |
|:-------------|:----------------|:---------------------------------------------|
| Command      | Client -> Server | `*#1*<where>#12*<hue>*<saturation>*<value>##` |
| Command      | Server -> Client | ACK                                          |
| Event        | Server -> Client | `*#1*<where>*12*<hue>*<saturation>*<value>##` |

### White Temperature command - Dimension = 14 [only for Tunable White Lights]

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*#1*<where>#14*<wt>##`  |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*#1*<where>*14*<wt>##`  |

## Dimension Request

### Set up the level at X speed - Dimension = 1

| Session Type | Direction       | Open Frame                                        |
|:-------------|:----------------|:--------------------------------------------------|
| Command      | Client -> Server | `*#1*<where>*1##`                                |
| Command      | Server -> Client | ACK                                               |
| Event        | Server -> Client | `*#1*<where>*1*<dimmerLevel100>*<dimmerSpeed>##` |

### Temporization request - Dimension = 2

| Session Type | Direction       | Open Frame                             |
|:-------------|:----------------|:---------------------------------------|
| Command      | Client -> Server | `*#1*<where>*2##`                      |
| Command      | Server -> Client | ACK                                    |
| Event        | Server -> Client | `*#1*<where>*2*<hour>*<min>*<sec>##`   |

### Required Only ON Light - Dimension = 3

| Session Type | Direction       | Open Frame                                            |
|:-------------|:----------------|:------------------------------------------------------|
| Command      | Client -> Server | `*#1*<where>*3##`                                     |
| Command      | Server -> Client | `*1*<dimmerLevel10>*<where>##` (only if some dimmer is ON) |
| Command      | Server -> Client | `*1*<status>*12<where>##` (only if some lights is ON, status=1) |
| Command      | Server -> Client | ACK                                                   |

### Working time lamp - Dimension = 8

| Session Type | Direction       | Open Frame                        |
|:-------------|:----------------|:----------------------------------|
| Command      | Client -> Server | `*#1*<where>*8##`                 |
| Command      | Server -> Client | `*#1*<where>*8*<workingTime>##`   |
| Command      | Server -> Client | ACK                               |
| Event        | Server -> Client | `*#1*<where>*8*<workingTime>##`   |

### Max working time lamp - Dimension = 9

| Session Type | Direction       | Open Frame                        |
|:-------------|:----------------|:----------------------------------|
| Command      | Client -> Server | `*#1*<where>*9##`                 |
| Command      | Server -> Client | `*#1*<where>*9*<workingTime>##`   |
| Command      | Server -> Client | ACK                               |
| Event        | Server -> Client | `*#1*<where>*9*<workingTime>##`   |

### HSV request - Dimension = 12 [only for RGB Lights]

| Session Type | Direction       | Open Frame                                   |
|:-------------|:----------------|:---------------------------------------------|
| Command      | Client -> Server | `*#1*<where>*12##`                           |
| Command      | Server -> Client | ACK                                          |
| Event        | Server -> Client | `*#1*<where>*12*<hue>*<saturation>*<value>##` |

### Tunable White request - Dimension = 14 [only for Tunable White Lights]

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Command      | Client -> Server | `*#1*<where>*14##`       |
| Command      | Server -> Client | ACK                      |
| Event        | Server -> Client | `*#1*<where>*14*<wt>##`  |

## Event Session

### Light status

| Session Type | Direction       | Open Frame           |
|:-------------|:----------------|:---------------------|
| Event        | Server -> Client | `*1*<what>*<where>##` |

### Luminous intensity change

| Session Type | Direction       | Open Frame                                        |
|:-------------|:----------------|:--------------------------------------------------|
| Event        | Server -> Client | `*#1*<where>*1*<dimmerLevel100>*<dimmerSpeed>##` |

### Light temporization

| Session Type | Direction       | Open Frame                             |
|:-------------|:----------------|:---------------------------------------|
| Event        | Server -> Client | `*#1*<where>*2*<hour>*<min>*<sec>##`   |

### HSV change [only for RGB Lights]

| Session Type | Direction       | Open Frame                                   |
|:-------------|:----------------|:---------------------------------------------|
| Event        | Server -> Client | `*#1*<where>*12*<hue>*<saturation>*<value>##` |

### White Temperature change [only for Tunable White Lights]

| Session Type | Direction       | Open Frame               |
|:-------------|:----------------|:-------------------------|
| Event        | Server -> Client | `*#1*<where>*14*<wt>##`  |

## WHO 14

### WHAT Table

| Value | Description |
|:------|:------------|
| 0     | Disable     |
| 1     | Enable      |

### WHERE Table

| Description    | Value |
|:---------------|:------|
| General        | - 0 -> General of system |
| Area           | A [00, 1-9, 100]:<br>- <A> -> Area |
| Point to point | A; PL:<br>- <A><PL> -> Point to point |

## Special Commands

### Disable - What = 0

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Command      | Client -> Server | `*14*0*<where>##`   | if the command is addressed to APL there won't be any answer in the monitor session. |
| Command      | Server -> Client | ACK                 |      |
| Event        | Server -> Client | `*14*0*<where>##`   |      |

### Enable - What = 1

| Session Type | Direction       | Open Frame          | Note |
|:-------------|:----------------|:--------------------|:-----|
| Command      | Client -> Server | `*14*1*<where>##`   | if the command is addressed to APL there won't be any answer in the monitor session. |
| Command      | Server -> Client | ACK                 |      |
| Event        | Server -> Client | `*14*1*<where>##`   |      |

---

## Copyright Notice

Copyright (C) 2024 [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com). All Rights Reserved.

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
