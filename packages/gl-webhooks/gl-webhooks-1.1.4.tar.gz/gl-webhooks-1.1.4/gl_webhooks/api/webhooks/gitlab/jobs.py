import contextlib
import json
import os
import tempfile
from multiprocessing.managers import SharedMemoryManager

from filelock import FileLock
from flasket import endpoint
from flasket.clients.gitlab import HookEvents, webhook


# TODO: Move to controller
def action_jobs_file(app, callback):
    # Get a unique ID from app.config
    key = app.config["UNIQUE_KEY"]
    filepath = os.path.join(tempfile.gettempdir(), f"gl-webhooks.jobs.{key}.json")
    lockfile = filepath + ".lock"

    with FileLock(lockfile):
        data = {}
        with contextlib.suppress(FileNotFoundError) as ctx:
            with open(filepath) as fd:
                data = json.load(fd)

        if callback:
            data = callback(data)
            with open(filepath, mode="w") as fd:
                json.dump(data, fd, indent=2, sort_keys=True)

        return data


@webhook([HookEvents.JOB_HOOK])
def monitor(app, body):
    build_id = str(body["build_id"])
    build_status = body["build_status"]

    def action(data):
        last_status = data.get(build_id, "absent")

        if build_status in ["created"]:
            # Purge completed actions from list
            data = {k: v for k, v in data.items() if v not in ["failed", "success", "canceled"]}
        elif build_status in ["pending"] and last_status in ["absent", "created"]:
            data[build_id] = build_status
        elif build_status in ["running"] and last_status in ["absent", "created", "pending"]:
            data[build_id] = build_status
        elif build_status in ["failed", "success", "canceled"]:
            data[build_id] = build_status
        return data

    data = action_jobs_file(app, action)
    pending = len([True for v in data.values() if v == "pending"])
    running = len([True for v in data.values() if v == "running"])

    return {
        "pending": pending,
        "running": running,
    }, 200
