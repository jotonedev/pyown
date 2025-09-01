---
title: WHO 7 - Multimedia System
summary: Open Web Net messages for multimedia system control and monitoring.
---

[Original Document](/assets/pdf/WHO_7.pdf)

## Introduction

This document describes the Open Web Net Message for WHO = 7 - MULTIMEDIA SYSTEM. It contains all the OpenWebNet frames used to control the camera of the Video Door Entry system catalogue.

## Device Compatibility

| Brand    | Item   |
|:---------|:-------|
| Legrand  |        |
| BTicino  | F453AV |

## WHAT Table

| WHAT | Description                                                           |
|:-----|:----------------------------------------------------------------------|
| 0    | Receive Video                                                         |
| 9    | Free Audio/Video Resources                                            |
| 120  | Zoom In                                                               |
| 121  | Zoom Out                                                              |
| 130  | Increases X coordinate of the central part of the image to be zoomed  |
| 131  | Decreases X coordinate of the central part of the image to be zoomed  |
| 140  | Increases Y coordinate of the central part of the image to be zoomed  |
| 141  | Decreases Y coordinate of the central part of the image to be zoomed  |
| 150  | Increases luminosity                                                  |
| 151  | Decreases luminosity                                                  |
| 160  | Increases contrast                                                    |
| 161  | Decreases contrast                                                    |
| 170  | Increases color                                                       |
| 171  | Decreases color                                                       |
| 180  | Increases image quality                                               |
| 181  | Decreases image quality                                               |
| 311  | Display DIAL 1-1                                                      |
| 312  | Display DIAL 1-2                                                      |
| 313  | Display DIAL 1-3                                                      |
| 314  | Display DIAL 1-4                                                      |
| 321  | Display DIAL 2-1                                                      |
| 322  | Display DIAL 2-2                                                      |
| 323  | Display DIAL 2-3                                                      |
| 324  | Display DIAL 2-4                                                      |
| 331  | Display DIAL 3-1                                                      |
| 332  | Display DIAL 3-2                                                      |
| 333  | Display DIAL 3-3                                                      |
| 334  | Display DIAL 3-4                                                      |
| 341  | Display DIAL 4-1                                                      |
| 342  | Display DIAL 4-2                                                      |
| 343  | Display DIAL 4-3                                                      |
| 344  | Display DIAL 4-4                                                      |

## WHERE Table

| WHERE | Description |
|:------|:------------|
| 4000  | Camera 00   |
| 4001  | Camera 01   |
| 4002  | Camera 02   |
| 4003  | Camera 03   |
| ...   | ...         |
| 4099  | Camera 99   |

## Command Sessions

| Session Type | Direction        | Open Frame         | Notes                                       |
|:-------------|:-----------------|:-------------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*0*WHERE##`     | WHERE = [4000-5000]                         |
| Command      | Server -> Client | ACK or NACK        | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*0*WHERE##`     | WHERE = [4000-5000]                         |

### Free Video Channel / Free Audio and Video Resource Command - WHAT = 9

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*9*##`     |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*9*##`     |                                             |

### Zoom IN Command - WHAT = 120

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*120##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*120##`    |                                             |

### Zoom OUT Command - WHAT = 121

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*121##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*121##`    |                                             |

### Increase X Coordinate Command - WHAT = 130

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*130##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*130##`    |                                             |

### Decrease X Coordinate Command - WHAT = 131

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*131##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*131##`    |                                             |

### Increase Y Coordinate Command - WHAT = 140

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*140##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*140##`    |                                             |

### Decrease Y Coordinate Command - WHAT = 141

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*141##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*141##`    |                                             |

### Increase Luminosity Command - WHAT = 150

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*150##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*150##`    |                                             |

### Decrease Luminosity Command - WHAT = 151

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*151##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*151##`    |                                             |

### Increase Contrast Command - WHAT = 160

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*160##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*160##`    |                                             |

### Decrease Contrast Command - WHAT = 161

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*161##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*161##`    |                                             |

### Increase Color Command - WHAT = 170

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*170##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*170##`    |                                             |

### Decrease Color Command - WHAT = 171

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*171##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*171##`    |                                             |

### Increase Image Quality Command - WHAT = 180

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*180##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*180##`    |                                             |

### Decrease Image Quality Command - WHAT = 181

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*181##`    |                                             |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*181##`    |                                             |

### Display DIAL X-Y Command - WHAT = 3XY

| Session Type | Direction        | Open Frame    | Notes                                       |
|:-------------|:-----------------|:--------------|:--------------------------------------------|
| Command      | Client -> Server | `*7*3XY##`    | X and Y can be assigned these values: 11, 12, 13, 14; 21, 22, 23, 24; 31, 32, 33, 34; 41, 42, 43, 44 |
| Command      | Server -> Client | ACK or NACK   | ACK: if command sent to Bus; NACK: if command not sent to Bus |
| Event        | Server -> Client | `*7*3XY##`    | See upper comments                          |

## Video Server

The web server makes available the pictures coming from selected camera. The pictures are encapsulated in HTTP/HTTPS protocol and it is in JPEG format.

In particular, once the camera has been activated with the proper OpenWebNet command (`*7*0*where##`), the picture can be recovered at the following URL:

```http
https://IPaddress/telecamera.php?CAM_PASSWD=password
```

or

```http
http://IPaddress/telecamera.php?CAM_PASSWD=password
```

Where "IPaddress" is the URL of the web server (numeric or alphanumeric as well), and "password" is the password that must be activated and configured using the configuration software and/or through the web pages (in the "configuration" area of the web pages). Please see the device's manual for further details.

### HTTP Response Format

The answer is composed from a header followed by the image in JPEG format.
The header is composed:

```http
HTTP/1.1 200 OK\r\n\
Server: grabtofile\r\n\
Connection: close\r\n\
Content-Length: <length_image>\r\n\
Content-Type: image/jpeg\r\n\r\n
```

### Password-less Access

If no password is configured, the pictures can be recovered at the following URLs:

```http
https://IPaddress/telecamera.php
```

or

```http
http://IPaddress/telecamera.php
```

**We strongly suggest to configure a password.**

---

## Copyright Notice

Copyright (C) 2011 [`www.myopen-legrandgroup.com`](https://www.myopen-legrandgroup.com). All Rights Reserved.

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
