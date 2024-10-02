# OpenWebNet parser for Python

This is a Python library to connect and parse OpenWebNet messages from Bticino/Legrand gateways.

Currently, it's a WIP, but it's already able to connect to the gateway and parse some messages.

## What is OpenWebNet?

OpenWebNet is a home automation protocol developed by Bticino (now part of Legrand) to control domotic devices like
lights, shutters, heating, etc.
It was developed around 2000, and it's still used today in many installations.
It does not implement any encryption, so it's not secure to use it over the internet.
Also, many devices implement only the old password algorithm, which is easily bruteforceable.
So, when using OpenWebNet, be sure to use it only in a trusted network and taking security measures, like vlan
separation.

## License

This project is licensed under the GNU GPL v3 license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* [openwebnet documentation](https://developer.legrand.com/Documentation/)
* [old password algorithm](https://rosettacode.org/wiki/OpenWebNet_password#Python)
* [java implementation](https://github.com/mvalla/openwebnet4j/) used in OpenHab developed
  by [mvalla](https://github.com/mvalla)
* [another python implementation](https://github.com/karel1980/ReOpenWebNet) developed
  by [karel1980](https://github.com/karel1980)
