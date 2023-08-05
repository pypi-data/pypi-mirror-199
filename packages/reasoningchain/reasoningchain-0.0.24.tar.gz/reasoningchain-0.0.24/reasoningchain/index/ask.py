#!/usr/bin/env python3

import os
import sys
import json
import tqdm
import re
import faiss
import click
import numpy as np
from typing import Union

from reasoningchain.doc_index import DocIndex
from reasoningchain.api import closeai

@click.command()
@click.option('--query', '-q', 'query', type=str, required=True)
@click.option('--index-path', '-p', 'index_path', type=str, required=True)
def main(query:str, index_path:str):
    doc_index = DocIndex()
    print(f"Loading index \x1b[32m{index_path}\x1b[0m ...")
    doc_index.load(index_path)
    print(f"Searching [\x1b[32m{query}\x1b[0m] ...")
    res = doc_index.search(query, 12)
    if not res:
        print("Nothing found", file=sys.stderr)
        return

    segs = []
    for item in sorted(res, key=lambda x:x['offset']):
        if len(segs) > 0 and segs[-1] == item['paragraph']:
            continue
        segs.append(item['paragraph'])

    episodes = '\n'.join([f'{i+1}) {v}' for i, v in enumerate(segs)])

    prompt = '问题相关剧情信息:{\n%s\n}\n\n问题: %s\n尽可能回答: ' % (episodes, query)

    print(f"prompt(length:{len(prompt)}):\n{prompt}")
    print()
    print("Requesting ChatGPT ...")
    res = closeai.chat(prompt, max_tokens=500)
    print(json.dumps(res, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()

