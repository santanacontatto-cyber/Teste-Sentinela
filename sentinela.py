#!/usr/bin/env python3
"""Sentinela Continuity Packet v0 — local, deterministic, stdlib-only."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.2.0"
FORMAT = "sentinela-continuity-packet/v0"
KINDS = {"observation", "interpretation", "decision", "boundary", "correction"}
STATUS = {"active", "rejected", "superseded"}
REQUIRED = {"id","time","actor","kind","text","status","confidence","evidence","revises","prev_hash","hash"}
ID_RE = re.compile(r"^E\d{4,}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(entry):
    body = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256(canonical(body).encode()).hexdigest()


def load(path):
    p = Path(path)
    if not p.exists():
        return {"format": FORMAT, "entries": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save(path, packet):
    Path(path).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify(packet):
    errors, ids = [], set()
    if not isinstance(packet, dict): return ["packet must be object"]
    if packet.get("format") != FORMAT: errors.append("unsupported format")
    entries = packet.get("entries")
    if not isinstance(entries, list): return errors + ["entries must be list"]
    prev = "GENESIS"
    for i, e in enumerate(entries):
        where = f"entry[{i}]"
        if not isinstance(e, dict): errors.append(f"{where}: must be object"); continue
        missing = sorted(REQUIRED - set(e))
        if missing: errors.append(f"{where}: missing fields {','.join(missing)}")
        eid=e.get("id")
        if not isinstance(eid,str) or not ID_RE.match(eid): errors.append(f"{where}: invalid id")
        if eid in ids: errors.append(f"{where}: duplicate id")
        ids.add(eid)
        if not isinstance(e.get("actor"),str) or not e.get("actor").strip(): errors.append(f"{where}: invalid actor")
        if not isinstance(e.get("text"),str) or not e.get("text").strip(): errors.append(f"{where}: invalid text")
        if e.get("kind") not in KINDS: errors.append(f"{where}: invalid kind")
        if e.get("status") not in STATUS: errors.append(f"{where}: invalid status")
        c=e.get("confidence")
        if c is not None and (isinstance(c,bool) or not isinstance(c,(int,float)) or not 0 <= c <= 1): errors.append(f"{where}: invalid confidence")
        ev=e.get("evidence")
        if not isinstance(ev,list) or any(not isinstance(x,str) or not x.strip() for x in ev): errors.append(f"{where}: invalid evidence")
        if e.get("revises") is not None and (not isinstance(e.get("revises"),str) or e.get("revises") not in ids): errors.append(f"{where}: revises unknown/future id")
        if e.get("prev_hash") != prev: errors.append(f"{where}: broken chain")
        h=e.get("hash")
        if not isinstance(h,str) or not HASH_RE.match(h): errors.append(f"{where}: malformed hash")
        if h != digest(e): errors.append(f"{where}: hash mismatch")
        prev = h
    return errors


def append(path, kind, actor, text, status="active", revises=None, evidence=None, confidence=None):
    packet = load(path)
    errors = verify(packet)
    if errors: raise ValueError("packet invalid; refusing write: " + "; ".join(errors))
    if kind not in KINDS: raise ValueError("invalid kind")
    if status not in STATUS: raise ValueError("invalid status")
    if not isinstance(actor,str) or not actor.strip(): raise ValueError("actor required")
    if not isinstance(text,str) or not text.strip(): raise ValueError("text required")
    if confidence is not None and (isinstance(confidence,bool) or not isinstance(confidence,(int,float)) or not 0 <= confidence <= 1): raise ValueError("confidence must be 0..1")
    if evidence is not None and (not isinstance(evidence,list) or any(not isinstance(x,str) or not x.strip() for x in evidence)): raise ValueError("evidence must be non-empty strings")
    entries = packet["entries"]
    if revises and not any(x["id"] == revises for x in entries): raise ValueError("revises id not found")
    n = len(entries) + 1
    e = {
        "id": f"E{n:04d}", "time": datetime.now(timezone.utc).isoformat(),
        "actor": actor.strip(), "kind": kind, "text": text.strip(), "status": status,
        "confidence": confidence, "evidence": evidence or [], "revises": revises,
        "prev_hash": entries[-1]["hash"] if entries else "GENESIS"
    }
    e["hash"] = digest(e); entries.append(e); save(path, packet); return e


def current(packet):
    entries = packet.get("entries", [])
    replaced = {e.get("revises") for e in entries if e.get("status") == "active" and e.get("revises")}
    return [e for e in entries if e.get("status") == "active" and e.get("id") not in replaced]


def main():
    ap = argparse.ArgumentParser(prog="sentinela", description="Verifiable human-AI continuity packets")
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p=sub.add_parser("init"); p.add_argument("file")
    p=sub.add_parser("add"); p.add_argument("file"); p.add_argument("--kind",required=True,choices=sorted(KINDS)); p.add_argument("--actor",required=True); p.add_argument("--text",required=True); p.add_argument("--status",choices=sorted(STATUS),default="active"); p.add_argument("--revises"); p.add_argument("--evidence",action="append",default=[]); p.add_argument("--confidence",type=float)
    p=sub.add_parser("verify"); p.add_argument("file")
    p=sub.add_parser("current"); p.add_argument("file")
    a=ap.parse_args()
    try:
        if a.cmd=="init":
            if Path(a.file).exists(): raise ValueError("refusing to overwrite existing packet")
            save(a.file,{"format":FORMAT,"entries":[]}); print(a.file)
        elif a.cmd=="add": print(json.dumps(append(a.file,a.kind,a.actor,a.text,a.status,a.revises,a.evidence,a.confidence),ensure_ascii=False,indent=2))
        elif a.cmd=="verify":
            errors=verify(load(a.file)); print("PASS" if not errors else "FAIL\n"+"\n".join(errors)); sys.exit(bool(errors))
        elif a.cmd=="current":
            packet=load(a.file); errors=verify(packet)
            if errors: raise ValueError("packet invalid: "+"; ".join(errors))
            print(json.dumps(current(packet),ensure_ascii=False,indent=2))
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}",file=sys.stderr); sys.exit(2)
if __name__ == "__main__": main()
