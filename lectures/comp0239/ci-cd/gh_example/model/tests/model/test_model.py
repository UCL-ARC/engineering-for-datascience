from ...model import owain_multiply


def test_model_positive():
    assert (12 == owain_multiply(3, 4))


def test_model_negative():
    assert (-6 == owain_multiply(-2, 3))


def test_model_dblneg():
    assert (25 == owain_multiply(-5, -5))
