"""Run the fixed first-action pilot through a supplied stateless model adapter.

Pass a JSON config (model, settings, timeout_seconds, evidence), an output
directory, and an adapter command after --adapter. Each process gets one
request as JSON on stdin and emits raw model text on stdout (exit 0).
Exit 75 explicitly signals a retryable transport error. Other failures stop
for reconciliation. Do not put credentials in command arguments or config.
"""

import argparse
import fcntl
import hashlib
import json
import subprocess
from pathlib import Path

from plan_handoff_pilot import make_plan
from report_handoff_pilot import audit


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n"


def save(path, content):
    temp = path.with_suffix(".tmp")
    temp.write_text(content, encoding="utf-8")
    temp.replace(path)


def run(config, directory, adapter, limit):
    if (
        not config["model"] or not isinstance(config["settings"], dict)
        or config["timeout_seconds"] <= 0 or config["evidence"] not in ("synthetic", "model")
        or limit <= 0
    ):
        raise ValueError("Set model, settings, evidence, timeout_seconds and a positive limit")
    plan = list(make_plan())
    manifest = {
        "config": config,
        "adapter": adapter,
        "plan_sha256": hashlib.sha256(encode(plan).encode()).hexdigest(),
    }
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "run.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest_path = directory / "manifest.json"
        ledger_path = directory / "ledger.jsonl"
        pending_path = directory / "pending.json"
        if manifest_path.exists():
            if json.loads(manifest_path.read_text()) != manifest:
                raise ValueError("The registered plan, config or adapter differs")
        else:
            if ledger_path.exists() or pending_path.exists():
                raise ValueError("Existing execution data has no manifest")
            save(manifest_path, encode(manifest))
        if pending_path.exists():
            raise ValueError("A dispatch is unresolved. Reconcile pending.json against adapter records.")
        records = (
            [json.loads(line) for line in ledger_path.read_text().splitlines()]
            if ledger_path.exists() else []
        )
        audit(records)
        by_id = {record["run_id"]: record for record in records}
        dispatched = 0
        for request in plan:
            run_id = request["run_id"]
            record = by_id.get(run_id, {"run_id": run_id, "attempts": []})
            attempts = record["attempts"]
            while len(attempts) < 2 and (not attempts or "transport_error" in attempts[-1]):
                if dispatched == limit:
                    return audit(records)
                number = len(attempts) + 1
                save(pending_path, encode({"run_id": run_id, "attempt": number}))
                result = subprocess.run(
                    adapter, input=encode({"config": config, "request": request, "attempt": number}),
                    text=True, encoding="utf-8", capture_output=True,
                    timeout=config["timeout_seconds"],
                )
                if result.returncode not in (0, 75):
                    raise ValueError(f"Adapter exit {result.returncode} for {run_id}; reconcile dispatch")
                attempts.append(
                    {"response": result.stdout} if result.returncode == 0
                    else {"transport_error": "adapter_exit_75"}
                )
                if run_id not in by_id:
                    by_id[run_id] = record
                    records.append(record)
                save(ledger_path, "".join(encode(row) for row in records))
                pending_path.unlink()
                dispatched += 1
        return audit(records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--limit", type=int, default=160, help="Maximum dispatches in this invocation")
    parser.add_argument("--adapter", nargs=argparse.REMAINDER, required=True)
    args = parser.parse_args()
    if not args.adapter:
        parser.error("--adapter requires a command")
    result = run(json.loads(args.config.read_text()), args.directory, args.adapter, args.limit)
    print(encode(result), end="")
