#!/usr/bin/env python3
"""Print a section's prompt as a cold run gets it: the run.md block, with the folder and the one rule a test adds.

Usage: python3 llm/brief.py SECTION [--repo PATH]

Paste the output into a fresh session of the model run.md names (or pass it to
your agent harness). The rule added: never open a key, a README or a run file
under llm/, since a run that has seen the key tests nothing. A block that runs kit tools
writes them as KIT/tools/...; this fills in the kit's folder (WSS_KIT, or the kit
beside this repo).
"""
import argparse, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument('section')
ap.add_argument('--repo', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
a = ap.parse_args()
run = open(os.path.join(a.repo, 'llm', a.section, 'run.md'), encoding='utf-8').read()
m = re.search(r'```text\n(.*?)\n```', run, re.S)
if not m:
    sys.exit(f'no text block in llm/{a.section}/run.md')
print(f'Work in the folder {a.repo}; every path below is from there. '
      'Never open any file named answers.md, README.md, run.md or score.py under llm/, nor anything under runs/ but your own output.\n')
block = m.group(1)
if 'KIT/' in block:
    kit = os.environ.get('WSS_KIT') or next((c for c in (os.path.join(os.path.dirname(a.repo), n) for n in ('world-saga-seed', 'story-kit'))
                                             if os.path.exists(os.path.join(c, 'tools', 'links.py'))), None)
    if not kit:
        sys.exit('this prompt runs kit tools: set WSS_KIT to the kit folder')
    block = block.replace('KIT/', kit.rstrip('/') + '/')
print(block)
