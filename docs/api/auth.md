---
title: Auth module
summary: Provides the authentication mechanism for the OpenWebNet gateway.
---

The Auth module provides the authentication mechanism for the OpenWebNet gateway.
OpenWebNet allows for two types of authentication: open algorithm and hmac algorithm.

The open algorithm is the simplest one and is used by the majority of the gateways, but it's not officially documented.

The hmac algorithm is used by the latest gateways,
and the [documentation](https://developer.legrand.com/uploads/2019/12/Hmac.pdf) is available.


::: pyown.auth.open.own_calc_pass


::: pyown.auth.hmac.client_hmac

::: pyown.auth.hmac.server_hmac

::: pyown.auth.hmac.compare_hmac

::: pyown.auth.hmac.create_key

::: pyown.auth.hmac.hex_to_digits

::: pyown.auth.hmac.digits_to_hex


::: pyown.auth.enum.AuthAlgorithm
