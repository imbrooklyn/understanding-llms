# SPDX-License-Identifier: Apache-2.0
"""Record every fixed generation-policy attempt on the retained final MG-2 model."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/mini-gpt'))
import torch
from model import create_model, config
from tokenizer import load
from generate import generate


def run(write=False):
    fixture = json.loads((ROOT/'data/part-v/generation-tasks.json').read_text())
    tokenizer = load(ROOT)
    model = create_model(config())
    model.load_state_dict(torch.load(ROOT/fixture['checkpoint'],map_location='cpu',weights_only=True))
    rows = []
    for task in fixture['tasks']:
        for locale,prompt in task['prompt'].items():
            for policy in fixture['policies']:
                for seed in fixture['seeds']:
                    output = generate(model,tokenizer,prompt,mode=policy['mode'],temperature=policy['temperature'],
                                      top_k=policy['top_k'],seed=seed,max_new=fixture['max_new_tokens'])
                    rows.append(dict(task=task['id'],locale=locale,policy=policy['id'],seed=seed,output=output,
                                     strict_match=output['valid_utf8'] and output['completion'].strip() in task.get('accepted',[])))
    inputs=['data/part-v/generation-tasks.json',fixture['checkpoint'],'data/mini-gpt/tokenizer.json','data/mini-gpt/config.json',
            'code/mini-gpt/generate.py','code/mini-gpt/model.py','code/mini-gpt/tokenizer.py','code/part-v/generation_matrix.py']
    result=dict(version='generation-run-v1',recorded_at=datetime.now(timezone.utc).isoformat(),
                environment=dict(python=platform.python_version(),torch=torch.__version__,device='cpu',dtype='float64',threads=1),
                inputs_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},rows=rows)
    if write:
        (ROOT/'data/part-v/generation-run.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    result=run(parser.parse_args().write)
    for row in result['rows']:
        print(json.dumps({key:row[key] for key in ['task','locale','policy','seed']} | {'completion':row['output']['completion'],'stop':row['output']['stop'],'valid_utf8':row['output']['valid_utf8'],'strict_match':row['strict_match']},ensure_ascii=False))
