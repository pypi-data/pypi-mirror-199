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

from reasoningchain.api import closeai

class DocIndex:
    def __init__(self, embedding_engine='CLOSEAI'):
        self._sentences = None
        self._index = None
        self._enbedding_engine = embedding_engine

    def load(self, index_path):
        self._index = faiss.read_index(index_path + '.index')
        with open(index_path + '.sentences') as f:
            self._sentences = json.load(f)
        return self._index is not None and self._sentences is not None

    def save(self, index_path):
        with open(index_path + '.sentences', 'w') as f:
            f.write(json.dumps(self._sentences, ensure_ascii=False))
        return faiss.write_index(self._index, index_path + '.index')

    def _get_embedding(self, text):
        return closeai.get_embedding_with_cache(text)

    def build(self, doc:str, index_type:str='IVFFlat') -> bool:
        sentences = split_to_sentences(doc)
        dim = 0
        embs = []
        for item in tqdm.tqdm(sentences):
            emb = self._get_embedding(item['text'])
            if not emb:
                print(f"Failed to get embedding for sentence:{item['text']}", file=sys.stderr)
                continue

            if not dim:
                dim = len(emb)

            embs.append(emb)
        embs = np.array(embs)

        #index = faiss.index_factory(dim, index_type)
        quantizer = faiss.IndexFlatL2(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, len(sentences), faiss.METRIC_L2)
        index.train(embs)
        index.add(embs)
        self._index = index
        self._sentences = sentences
        return True

    def search(self, query, topk=10):
        query = query.strip()
        if not query:
            return []
        emb = self._get_embedding(query)
        if not emb:
            raise RuntimeError("Failed to get embedding for " + query)
        emb = np.array([emb])
        self._index.nprobe = topk
        D, I = self._index.search(emb, topk)
        res = []
        for i in range(len(I[0])):
            idx = int(I[0][i])
            if idx < 0:
                continue
            sent = self._sentences[idx]
            res.append({
                'sentence': sent,
                'distance': float(D[0][i]),
            })
        return res

    def get_by_index(self, index):
        if index >= 0 and index < len(self._sentences):
            return self._sentences[index]
        return None

def split_to_sentences(text:str):
    sep = set(['\n', '. ', '! ', '? ', '。', '！', '？', '; ', '；'])
    start = 0
    i = 0
    docid = 1
    res = [] # 腾出0号位置
    last_para = [0, -1]
    while i < len(text):
        if text[i] not in sep: 
            i += 1
            continue
        para_start = -1
        while i < len(text) and text[i] in sep:
            if text[i] == '\n':
                if last_para[1] == -1:
                    last_para[1] = i
                para_start = i + 1
            i += 1
        sentence = text[start:i].strip()
        if i > 0 and text[i-1] == '\n':
            para_offset = i-1
        if len(sentence) > 2:
            res.append({
                'text':sentence,
                'offset':start,
                'paragraph': last_para,
            })
            docid += 1
        start = i
        if para_start >= 0:
            last_para = [para_start, -1]
    if start < len(text):
        last_para[1] = len(text)
        sentence = text[start:].strip()
        if len(sentence) > 2:
            res.append({
                'text':sentence,
                'offset':start,
                'paragraph': last_para,
            })
    return res

@click.command()
@click.argument("mode")
@click.option('--doc', '-d', 'doc_file_path', type=str, required=True)
@click.option('--index-type', '-t', 'index_type', type=str, default='FlatL2', required=False)
@click.option('--index-path', '-p', 'index_path', type=str, required=True)
def build_index(mode:str, doc_file_path:str, index_type:str, index_path:str):
    doc_index = DocIndex()
    with open(doc_file_path) as f:
        text = f.read()
        print("Building index...")
        doc_index.build(text)
        doc_index.save(index_path)
    print(f"Index has been saved to \x1b[32m{index_path}\x1b[0m")

@click.command()
@click.argument("mode")
@click.option('--query', '-q', 'query', type=str, required=True)
@click.option('--index-path', '-p', 'index_path', type=str, required=True)
def search_index(mode:str, query:str, index_path:str):
    doc_index = DocIndex()
    print(f"Loading index \x1b[32m{index_path}\x1b[0m ...")
    doc_index.load(index_path)
    print(f"Searching [\x1b[32m{query}\x1b[0m] ...")
    res = doc_index.search(query)
    if res:
        print('Results:')
        print(json.dumps(res, indent=4, ensure_ascii=False))
    else:
        print("Nothing found", file=sys.stderr)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode.startswith('-'):
        mode = 'search'
    if mode == 'build':
        build_index()
    elif mode == 'search':
        search_index()
    sys.exit()
    query = sys.argv[1] if len(sys.argv) > 1 else None

    index_path = "./chatgpt_news.index"
    doc_index = DocIndex()
    if os.path.isfile(index_path + '.doc'):
        doc_index.load(index_path)
    else:
        print("Reading text...")
        text = ''
        for line in sys.stdin:
            text += line

        print(text)
        #sentences = split_to_sentences(text)
        #print(json.dumps(sentences, indent=4, ensure_ascii=False))

        doc_index.build(text)
        doc_index.save(index_path)

    if query:
        res = doc_index.search(query)
        print(json.dumps(res, indent=4, ensure_ascii=False))

