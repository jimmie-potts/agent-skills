#!/usr/bin/env python3
"""Count a matched instruction trace and its literal message samples.

Read only the caller-supplied JSON and explicit Markdown paths under one source
checkout. Emit a receipt to stdout. No execution, network, discovery or writes.
This measures text exposure, not behavioral correctness, tokens or runtime cost.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

FIXED_INPUT = "tests/fixtures/workflow-evaluation/context-reporting-cases.md"


def size(text):
    return {"bytes": len(text.encode("utf-8")), "words": len(text.split())}


def total(records):
    return {unit: sum(record[unit] for record in records)
            for unit in ("bytes", "words")}


def source_path(root, name):
    path = PurePosixPath(name)
    if (path.is_absolute() or ".." in path.parts or str(path) != name
            or not (name == "AGENTS.md" or name.startswith("skills/"))
            or path.suffix != ".md"):
        raise ValueError(f"Not a canonical instruction path: {name}")
    candidate = root.resolve() / name
    if candidate.resolve() != candidate:
        raise ValueError(f"Instruction is not a canonical file path: {name}")
    return candidate


def measure(root, response, revision):
    cases = response["cases"]
    expected = {(f"L{i}", host) for i in range(1, 6)
                for host in ("codex", "claude")}
    identities = [(case["id"], case["host"]) for case in cases]
    if len(identities) != 10 or set(identities) != expected:
        raise ValueError("Require each of L1-L5 on codex and claude exactly once")
    inventory = {}

    def read(name):
        if name not in inventory:
            raw = source_path(root, name).read_bytes()
            inventory[name] = dict(size(raw.decode("utf-8")),
                                   sha256=hashlib.sha256(raw).hexdigest())
        return inventory[name]

    def exposure(names):
        unique = sorted(set(names))
        return {"paths": unique, **total([read(name) for name in unique])}

    records = []
    declared_sources = set(response["sources"])
    for case in cases:
        if not set(case["reads"]) <= declared_sources:
            raise ValueError("Case reads absent from declared actual sources")
        messages = {name: size(case[name]) for name in ("brief", "return")}
        messages["updates"] = [dict(event=item["event"], **size(item["text"]))
                               for item in case["updates"]]
        records.append({"id": case["id"], "host": case["host"],
                        "coordinator_actual": exposure(case["reads"]),
                        "worker_proposed": exposure(case["worker_reads"]),
                        "messages": messages})
    external = [name for name in response["sources"] if name.startswith("external:")]
    fixed_inputs = [name for name in response["sources"] if name == FIXED_INPUT]
    actual_union = exposure([name for name in response["sources"]
                             if name not in external + fixed_inputs])
    proposed_union = exposure([name for case in cases for name in case["worker_reads"]])
    return {
        "source_revision": revision,
        "method": "UTF-8 bytes and len(text.split()); whole files; deduplicate per case/role",
        "cases": records,
        "actual_union": actual_union,
        "external_sources_excluded": external,
        "fixed_inputs_excluded": fixed_inputs,
        "worker_proposed_union": proposed_union,
        "combined_union": exposure(list(inventory)),
        "source_inventory": dict(sorted(inventory.items())),
        "exclusions": "Fixed inputs, JSON keys, bookkeeping, and host/system/tool text; see raw response for external reads",
        "limitations": "Source revision is caller supplied; inspect Git state independently. Proposed child reads and simulated messages are not native host measurements.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_root", type=Path)
    parser.add_argument("response", type=Path)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    response = json.loads(args.response.read_text(encoding="utf-8"))
    print(json.dumps(measure(args.source_root, response, args.revision),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
