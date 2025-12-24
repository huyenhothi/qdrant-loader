import threading
import pytest

_current_test = None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    global _current_test
    _current_test = item.nodeid
    yield
    _current_test = None


@pytest.fixture(scope="session", autouse=True)
def fail_on_thread_exception():
    original_hook = threading.excepthook

    def excepthook(args):
        raise RuntimeError(
            f"Background thread exception in test: {_current_test}"
        ) from args.exc_value

    threading.excepthook = excepthook
    yield
    threading.excepthook = original_hook
