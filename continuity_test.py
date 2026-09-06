#!/usr/bin/env python3
"""Deterministic Continuity Test: score a reconstruction against a packet without calling any AI API."""
import argparse, json, sys
from sentinela import load, verify, current


def expected(packet):
    active=current(packet)
    return {
        "active_ids":[e["id"] for e in active],
        "boundaries":[e["id"] for e in active if e["kind"]=="boundary"],
        "decisions":[e["id"] for e in active if e["kind"]=="decision"],
        "uncertain":[e["id"] for e in active if e.get("confidence") is not None and e["confidence"] < 0.5]
    }


def score(packet, answer):
    exp=expected(packet); fields=list(exp); details={}; total=0
    for f in fields:
        got=answer.get(f)
        ok=isinstance(got,list) and set(got)==set(exp[f]) and len(got)==len(exp[f])
        details[f]={"pass":ok,"expected":exp[f],"got":got}; total+=int(ok)
    cited=answer.get("citations",[])
    known={e["id"] for e in packet["entries"]}
    citations_ok=isinstance(cited,list) and all(x in known for x in cited)
    details["citations"]={"pass":citations_ok,"unknown":[] if citations_ok else [x for x in cited if x not in known] if isinstance(cited,list) else ["not-a-list"]}
    total+=int(citations_ok)
    return {"score":total,"max_score":len(fields)+1,"pass":total==len(fields)+1,"details":details}


def main():
    p=argparse.ArgumentParser(); p.add_argument("packet"); p.add_argument("answer"); a=p.parse_args()
    packet=load(a.packet); errors=verify(packet)
    if errors: print(json.dumps({"pass":False,"packet_errors":errors},indent=2)); sys.exit(2)
    answer=json.loads(open(a.answer,encoding="utf-8").read())
    result=score(packet,answer); print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(0 if result["pass"] else 1)
if __name__=="__main__": main()
