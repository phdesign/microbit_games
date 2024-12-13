def pytest_configure(config):
    import sys

    sys.__TESTING__ = True


def pytest_unconfigure(config):
    import sys

    del sys.__TESTING__
