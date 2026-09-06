#!/usr/bin/env python3
"""Deterministic Continuity Test: score a reconstruction against a packet without calling any AI API."""
import argparse, json, sys
from sentinela import load, verify, current, effective_kind

ALLOWED_ANSWER_FIELDS={"active_ids","boundaries","decisions","uncertain","citations"}


def expected(packet):
    active=current(packet)
    return {
        "active_ids":[e["id"] for e in active],
        "boundaries":[e["id"] for e in active if effective_kind(e,packet)=="boundary"],
        "decisions":[e["id"] for e in active if effective_kind(e,packet)=="decision"],
        "uncertain":[e["id"] for e in active if e.get("confidence") is not None and e["confidence"] < 0.5]
    }


def score(packet, answer):
    packet_errors=verify(packet)
    if packet_errors: return {"score":0,"max_score":6,"pass":False,"packet_errors":packet_errors}
    if not isinstance(answer,dict): return {"score":0,"max_score":6,"pass":False,"answer_errors":["answer must be object"]}
    unknown=sorted(set(answer)-ALLOWED_ANSWER_FIELDS); missing=sorted(ALLOWED_ANSWER_FIELDS-set(answer)); answer_errors=[]
    if unknown: answer_errors.append("unsupported answer fields: "+",".join(unknown))
    if missing: answer_errors.append("missing answer fields: "+",".join(missing))
    exp=expected(packet); fields=list(exp); details={}; total=0
    for f in fields:
        got=answer.get(f); ok=isinstance(got,list) and set(got)==set(exp[f]) and len(got)==len(exp[f])
        details[f]={"pass":ok,"expected":exp[f],"got":got}; total+=int(ok)
    cited=answer.get("citations"); active_ids=exp["active_ids"]
    citations_ok=isinstance(cited,list) and len(cited)==len(set(cited)) and set(cited)==set(active_ids)
    details["citations"]={"pass":citations_ok,"expected_current_support":active_ids,"got":cited}; total+=int(citations_ok)
    schema_ok=not answer_errors; details["answer_schema"]={"pass":schema_ok,"errors":answer_errors}; total+=int(schema_ok)
    max_score=len(fields)+2
    return {"score":total,"max_score":max_score,"pass":total==max_score,"details":details}


def main():
    p=argparse.ArgumentParser(); p.add_argument("packet"); p.add_argument("answer"); a=p.parse_args()
    try:
        packet=load(a.packet); answer=json.loads(open(a.answer,encoding="utf-8").read())
    except (OSError,json.JSONDecodeError) as e:
        print(json.dumps({"pass":False,"error":str(e)},ensure_ascii=False,indent=2)); sys.exit(2)
    result=score(packet,answer); print(json.dumps(result,ensure_ascii=False,indent=2)); sys.exit(0 if result["pass"] else 1)
if __name__=="__main__": main()
