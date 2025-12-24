import threading
import pytest

@pytest.fixture(autouse=True)
def fail_on_thread_exception(monkeypatch):
    def excepthook(args):
        raise args.exc_value
    monkeypatch.setattr(threading, "excepthook", excepthook)
