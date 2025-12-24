import sys
import threading
import pytest

_original_start = threading.Thread.start
_original_excepthook = threading.excepthook


def pytest_configure():
    def patched_start(self, *args, **kwargs):
        self._pytest_nodeid = getattr(
            threading.current_thread(), "_pytest_nodeid", None
        )
        return _original_start(self, *args, **kwargs)

    threading.Thread.start = patched_start

    def excepthook(args):
        nodeid = getattr(args.thread, "_pytest_nodeid", "UNKNOWN")
        print(
            "\n[pytest-thread-warning]",
            f"Background thread exception from test: {nodeid}",
            f"Thread: {args.thread.name}",
            f"Exception: {args.exc_value}",
            sep="\n",
            file=sys.stderr,
        )

    threading.excepthook = excepthook


def pytest_unconfigure():
    threading.Thread.start = _original_start
    threading.excepthook = _original_excepthook


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    threading.current_thread()._pytest_nodeid = item.nodeid
    yield
