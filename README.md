# OpenWebNet parser for Python

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyown?link=https%3A%2F%2Fpypi.org%2Fproject%2Fpyown%2F)
![PyPI - Status](https://img.shields.io/pypi/status/pyown?link=https%3A%2F%2Fpypi.org%2Fproject%2Fpyown%2F)
![PyPI - Version](https://img.shields.io/pypi/v/pyown?link=https%3A%2F%2Fpypi.org%2Fproject%2Fpyown%2F)

This is a Python library to connect and parse OpenWebNet messages from Bticino/Legrand gateways.

Currently, it is a WIP, but it is already able to connect to the gateway and manages lighting or automation devices.

[PyPI page](https://pypi.org/project/pyown/)

## What is OpenWebNet?

OpenWebNet is a home automation protocol developed by Bticino (now part of Legrand) to control domotic devices like
lights, shutters, heating, etc.
It was developed around 2000, and it's still used today in many installations.
It does not implement any encryption, so it is not secure to use it over the internet.
Also, many devices implement only the old password algorithm, which is easily bruteforceable.
So, when using OpenWebNet, be sure to use it only in a trusted network and taking security measures, like vlan
separation.

## Project structure

- [pyown](pyown) contains the library code
- [examples](examples) contains some examples on how to use the library
- [tests](tests) contains the tests for the library

### Library structure

- [items](pyown/items) contains the code for the various types of devices that can be controlled
- [client](pyown/client) used to connect to the gateway, manages the various types of sessions
- [auth](pyown/auth) implementation of the authentication algorithms
- [protocol](pyown/protocol) manages the sending and receive of the messages and the initial parsing
- [messages](pyown/messages) defines the various types of messages allowed by the protocol
- [tags](pyown/tags) defines the tags that compose a message

## License

This project is licensed under the GNU GPL v3 license—see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* [old openwebnet documentation](https://web.archive.org/web/20090311005636/http://www.myopen-bticino.it/openwebnet/openwebnet.php)
* [openwebnet documentation](https://developer.legrand.com/Documentation/)
* [another openwebnet documentation page](https://developer.legrand.com/local-interoperability/#PDF%20documentation)
* [old password algorithm](https://rosettacode.org/wiki/OpenWebNet_password#Python)
* [java implementation](https://github.com/mvalla/openwebnet4j/) used in OpenHab developed
  by [mvalla](https://github.com/mvalla)
* [another python implementation](https://github.com/karel1980/ReOpenWebNet) developed
  by [karel1980](https://github.com/karel1980)

## Disclaimer

- This library is not associated by any means with BTicino or Legrand companies
- The Open Web Net protocol is maintained and Copyright by BTicino/Legrand. The documentation of the protocol if freely
  accessible for developers on the Legrand developer website
- "Open Web Net", "SCS", "MyHOME_Up", "MyHOME", "MyHOME_Play" and "Living Now" are registered trademarks by
  BTicino/Legrand
