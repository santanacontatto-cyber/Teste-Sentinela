#!/usr/bin/env python3
"""Build and score a small adversarial continuity handoff end-to-end."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json

from sentinela import save, append, load, verify
from continuity_test import score


def build_packet(path):
    save(path,{"format":"sentinela-continuity-packet/v0","entries":[]})
    old=append(path,"decision","human","Use the old plan")
    append(path,"correction","human","Use the revised plan",revises=old["id"])
    append(path,"boundary","human","Do not spend money without fresh authorization")
    append(path,"interpretation","ai","This may be the best next step",confidence=.35)
    return load(path)


def main():
    with TemporaryDirectory() as d:
        p=Path(d)/"packet.json"
        packet=build_packet(p)
        errors=verify(packet)
        if errors:
            raise SystemExit("packet invalid: "+"; ".join(errors))

        good={
            "active_ids":["E0002","E0003","E0004"],
            "boundaries":["E0003"],
            "decisions":[],
            "uncertain":["E0004"],
            "citations":["E0002","E0003","E0004"]
        }
        stale={
            "active_ids":["E0001","E0002","E0003","E0004"],
            "boundaries":["E0003"],
            "decisions":["E0001"],
            "uncertain":["E0004"],
            "citations":["E0001"]
        }
        hallucinated={
            "active_ids":["E0002","E0003","E0004"],
            "boundaries":["E0003"],
            "decisions":[],
            "uncertain":["E0004"],
            "citations":["E9999"]
        }

        result={
            "valid_reconstruction":score(packet,good),
            "stale_reconstruction":score(packet,stale),
            "hallucinated_evidence":score(packet,hallucinated)
        }
        print(json.dumps(result,ensure_ascii=False,indent=2))
        if not result["valid_reconstruction"]["pass"]: raise SystemExit(1)
        if result["stale_reconstruction"]["pass"]: raise SystemExit(1)
        if result["hallucinated_evidence"]["pass"]: raise SystemExit(1)

if __name__=="__main__": main()
