#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import json
import requests
import traceback
import asyncio
from typing import Union
from threading import Thread

from reasoningchain.cache.disk_cache import disk_cache

def generate_image(prompt:str):
    prompt = prompt.strip()
    if not prompt:
        return []

    req = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }
    res = request_api('/images/generations', req)
    if not res:
        return []

    res = json.loads(response.content)
    urls = []
    for item in res['data']:
        urls.append(item['url'])
    return urls

def get_embedding(text:str):
    try:
        text = text.strip()
        if not text:
            return None

        params = {
            "model": "text-embedding-ada-002",
            "input": text
        }
        res = request_api('/embeddings', params)
        if not res.get('data', None):
            return None
        return res['data'][0]['embedding']
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return None 

def chat(messages:Union[list,str], max_tokens=500, temperature=0.5):
    if isinstance(messages, str):
        messages = [{
            'role':'user',
            'content':messages,
        }]

    req = {
         "model": "gpt-3.5-turbo",
         "temperature": temperature,
         "max_tokens": max_tokens,
         "messages": messages
    }
    res = request_api("/chat/completions", req)
    if not res:
        return res
    print('closeai token usage:', json.dumps(res['usage'], ensure_ascii=False), file=sys.stderr)
    answer = res['choices'][0]['message']['content']
    return answer

@disk_cache(cache_path=os.path.join(os.environ['HOME'], '.cache/closeai/chat'), expire_time=864000)
def chat_with_cache(messages:Union[list,str], max_tokens=500, temperature=0.5):
    return chat(messages, max_tokens, temperature)

@disk_cache(cache_path=os.path.join(os.environ['HOME'], '.cache/closeai/text_embedding'), expire_time=8640000)
def get_embedding_with_cache(text:str):
    return get_embedding(text)

async def aget_embedding_with_cache(text:str):
    return get_embedding_with_cache(text)

def batch_get_embeddings(text_list:list, batch_size=8) -> list:
    print("batch_get_embeddings() ...")
    res = [None] * len(text_list)
    try:
        def task(i, text):
            res[i] = get_embedding_with_cache(text)
        for i in range(0, len(text_list), batch_size):
            threads = []
            for j, text in enumerate(text_list[i:i+batch_size]):
                thread = Thread(target=lambda:task(i+j, text))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
        return res
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        print(e, file=sys.stderr)
    return res

def batch_get_embeddings2(text_list:list, batch_size=8) -> list:
    res = []
    loop = asyncio.get_event_loop()
    try:
        for i in range(0, len(text_list), batch_size):
            tasks = []
            for text in text_list[i:i+batch_size]:
                tasks.append(asyncio.ensure_future(aget_embedding_with_cache(text)))

            results = loop.run_until_complete(asyncio.wait(tasks))
            for item in results[0]:
                res.append(item.result())
    except Exception as e:
        print(e, file=sys.stderr)
    loop.close()
    return res

def request_api(path, params):
    url = os.getenv("OPENAI_API_BASE")
    if not url:
        url = "https://api.openai.com/v1"
    url += path
    token = os.getenv('OPENAI_API_KEY')
    response = requests.post(url, json=params, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    })
    if response.status_code >= 300:
        print(f'Request "{path}" failed with status:{response.status_code}', file=sys.stderr)
        return None

    return json.loads(response.content)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd in ['emb', 'embedding']:
        text_list = []
        for line in sys.stdin:
            text = line.strip()
            if text:
                text_list.append(text)

        res = batch_get_embeddings(text_list)
        print(res)
        print(len(res))

