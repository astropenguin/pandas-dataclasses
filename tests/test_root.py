# dependencies
import pandas_dataclasses


# test functions
def test_author():
    assert (
        pandas_dataclasses.__author__
        == "Akio Taniguchi <taniguchi@a.phys.nagoya-u.ac.jp>"
    )


def test_version():
    assert pandas_dataclasses.__version__ == "0.1.0"
