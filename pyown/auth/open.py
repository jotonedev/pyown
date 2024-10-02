__all__ = ["own_calc_pass"]


def own_calc_pass(password: str | int, nonce: str | int) -> str:  # noqa: C901
    """
    Encode the password using the OPEN algorithm.
    Source: https://rosettacode.org/wiki/OpenWebNet_password#Python

    Parameters:
        password (str | int): The password to encode, must be composed of only digits.
        nonce (str): The nonce received from the gateway.

    Returns:
        str: The encoded password.
    """
    start = True
    num1 = 0
    num2 = 0

    if isinstance(password, str):
        password = int(password)

    if isinstance(nonce, int):
        nonce = str(nonce)

    for c in nonce:
        if c != "0":
            if start:
                num2 = password
            start = False
        if c == '1':
            num1 = (num2 & 0xFFFFFF80) >> 7
            num2 = num2 << 25
        elif c == '2':
            num1 = (num2 & 0xFFFFFFF0) >> 4
            num2 = num2 << 28
        elif c == '3':
            num1 = (num2 & 0xFFFFFFF8) >> 3
            num2 = num2 << 29
        elif c == '4':
            num1 = num2 << 1
            num2 = num2 >> 31
        elif c == '5':
            num1 = num2 << 5
            num2 = num2 >> 27
        elif c == '6':
            num1 = num2 << 12
            num2 = num2 >> 20
        elif c == '7':
            num1 = num2 & 0x0000FF00 | ((num2 & 0x000000FF) << 24) | ((num2 & 0x00FF0000) >> 16)
            num2 = (num2 & 0xFF000000) >> 8
        elif c == '8':
            num1 = (num2 & 0x0000FFFF) << 16 | (num2 >> 24)
            num2 = (num2 & 0x00FF0000) >> 8
        elif c == '9':
            num1 = ~num2
        else:
            num1 = num2

        num1 &= 0xFFFFFFFF
        num2 &= 0xFFFFFFFF
        if c not in "09":
            num1 |= num2
        num2 = num1

    return str(num1)
