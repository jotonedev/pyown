from pyown.auth import own_calc_pass


def test_auth_v1():
    password = "12345"
    nonce = "844308954"

    assert own_calc_pass(password, nonce) == "4294506975"
