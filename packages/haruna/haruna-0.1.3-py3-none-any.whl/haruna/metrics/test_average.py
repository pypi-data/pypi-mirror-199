from .average import Average
from .average import ExponentialMovingAverage


def test_average():
    m = Average()
    m.update(1)
    m.update(2)
    m.update(3)
    m.update(4)
    assert m.value == 2.5


def test_exponential_moving_average():
    m = ExponentialMovingAverage(bias_correct=False)
    m.update(1)
    m.update(2)
    assert m.value == 1.25
