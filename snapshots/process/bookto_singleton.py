#!/usr/bin/env python3
"""Kernel-backed singleton ownership for Bookto production loops."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from types import FrameType
from typing import TextIO


def try_process_lock(path: Path) -> TextIO | None:
    """Return an owned lock handle, or None when another process owns it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+", encoding="utf-8")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return None
    handle.seek(0)
    handle.truncate()
    json.dump({"pid": os.getpid(), "acquired_at": time.time()}, handle)
    handle.write("\n")
    handle.flush()
    os.fsync(handle.fileno())
    return handle


def run_locked(argv: list[str]) -> int:
    """Run one command while retaining a kernel lock and forwarding stop signals."""
    parser = argparse.ArgumentParser()
    parser.add_argument("lock_path", type=Path)
    parser.add_argument("command", nargs="+")
    args = parser.parse_args(argv)
    lock = try_process_lock(args.lock_path)
    if lock is None:
        print('{"status":"DUPLICATE_PROCESS_SUPPRESSED"}', flush=True)
        return 0
    with lock:
        child = subprocess.Popen(args.command)

        def forward(signum: int, _frame: FrameType | None) -> None:
            if child.poll() is None:
                child.send_signal(signum)

        for signum in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, forward)
        return child.wait()


if __name__ == "__main__":
    raise SystemExit(run_locked(sys.argv[1:]))
