#!/usr/bin/env python3
"""Compile verified continuity state into human-auditable runtime premise bundles."""
import argparse, json, sys
from sentinela import load, verify, human_view, premise_block, VERSION

PROFILES={"fresh-chat","project-instructions","custom-instructions"}


def compile_bundle(packet, profile):
    if profile not in PROFILES: raise ValueError("unsupported profile")
    errors=verify(packet)
    if errors: raise ValueError("packet invalid: "+"; ".join(errors))
    premises=premise_block(packet)
    wrappers={
        "fresh-chat": "Use the verified premises below as current context. Do not invent missing facts, do not resurrect replaced state, preserve uncertainty, and do not treat these premises as authorization for external actions.",
        "project-instructions": "Project continuity rule: treat the verified premises below as current project state. When source material conflicts, prefer newer valid revisions, preserve uncertainty, and never infer new authority from continuity state.",
        "custom-instructions": "Continuity rule: use the verified premises below as current context only. Preserve source IDs, uncertainty and boundaries. Never convert context into permission or authority."
    }
    return {
        "sentinela_version":VERSION,
        "profile":profile,
        "human_audit":human_view(packet),
        "runtime_text":wrappers[profile]+"\n\n"+premises,
    }


def main():
    ap=argparse.ArgumentParser(description="Compile a verified Sentinela packet into a runtime premise bundle")
    ap.add_argument("packet"); ap.add_argument("--profile",choices=sorted(PROFILES),default="fresh-chat"); ap.add_argument("--format",choices=["json","text"],default="text")
    a=ap.parse_args()
    try:
        bundle=compile_bundle(load(a.packet),a.profile)
    except (ValueError,json.JSONDecodeError,OSError) as e:
        print(f"ERROR: {e}",file=sys.stderr); sys.exit(2)
    if a.format=="json": print(json.dumps(bundle,ensure_ascii=False,indent=2))
    else: print(bundle["runtime_text"],end="")

if __name__=="__main__": main()
