from src.utils import time_to_hour


def test_time_convert_to_hours():
    assert time_to_hour("10:05:20") == round(10.088888889, 2)
