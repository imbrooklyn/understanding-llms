# SPDX-License-Identifier: Apache-2.0
"""Optional author-only extraction from a pinned CC BY 4.0 upstream Parquet.

Requires pyarrow==20.0.0 in a separate temporary author environment. Core tests
and notebooks read the checked-in JSON slice and never require this dependency.
"""
import hashlib
import json
from pathlib import Path
import sys

REVISION='f7d2896d2cc5d80f8b55c2bbc722613555233c25'
SHA256='4877bc46a40929f4082c3c79593700fb897b1d6c7f4c473032694a01322f5769'
URL=f'https://huggingface.co/datasets/lmsys/mt_bench_human_judgments/resolve/{REVISION}/data/human-00000-of-00001-25f4910818759289.parquet'


def extract(path):
    import pyarrow.parquet as pq
    path=Path(path)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=SHA256:raise ValueError('upstream_digest')
    selected=[];seen=set()
    for index,row in enumerate(pq.read_table(path).to_pylist()):
        if row['turn']!=1 or row['question_id'] in seen:continue
        size=sum(len(m['content']) for key in ['conversation_a','conversation_b'] for m in row[key][:2])
        if size>1800 or row['question_id']<100:continue
        row['conversation_a']=row['conversation_a'][:2];row['conversation_b']=row['conversation_b'][:2]
        selected.append(dict(source_row=index,**row));seen.add(row['question_id'])
        if len(selected)==4:break
    result=dict(version='human-calibration-v1',source=URL,revision=REVISION,source_sha256=SHA256,
                attribution='Zheng et al. / LMSYS, MT-Bench human judgments (2023)',license='CC-BY-4.0',
                selection='Before local Judge execution: first turn-1 row in source order for four distinct question IDs >=100 whose two first-turn conversations total <=1800 Unicode code points.',
                modifications='Select four records; retain only first-turn messages, preserving original strings and human labels. Public pseudonymous annotator IDs retained. No translation used for model evaluation.',
                limitations='One existing human vote per case; nonrepresentative short English convenience slice; not travel-domain factual labels; no majority adjudication.',cases=selected)
    root=Path(__file__).resolve().parents[2]
    (root/'data/part-viii/human-calibration-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__':extract(sys.argv[1])
