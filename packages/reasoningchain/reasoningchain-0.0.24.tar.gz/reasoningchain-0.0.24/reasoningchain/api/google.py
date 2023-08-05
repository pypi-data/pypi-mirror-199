#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import json
import requests
import traceback

SERP_GOOGLE_SEARCH_MAP_URL = 'https://serpapi.com/search.json?api_key=85f7bf8cfdbaa036ea99a228eabb93cfc1a0bdb1736308e8dffe3efa3cb6d6de&engine=google_maps&type=search&q='
SERP_GOOGLE_SEARCH_IMAGE_URL = 'https://serpapi.com/search?api_key=85f7bf8cfdbaa036ea99a228eabb93cfc1a0bdb1736308e8dffe3efa3cb6d6de&device=desktop&engine=google&google_domain=google.com&tbs=images&tbm=isch&q='

def search_map(query):
    query = query.strip()
    if not query:
        return ""
    try:
        url = SERP_GOOGLE_SEARCH_MAP_URL + query
        response = requests.get(url)
        if response.status_code >= 300:
            return None
        res = json.loads(response.content)
        loc = res['place_results']
        return {
            'address': loc['address'],
            'latitude': loc['gps_coordinates']['latitude'],
            'longitude': loc['gps_coordinates']['longitude'],
        }
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    return None

def search_image(query):
    try:
        query = query.strip()
        if not query:
            return []

        url = SERP_GOOGLE_SEARCH_IMAGE_URL + query
        response = requests.get(url)
        res = json.loads(response.content)
        if response.status_code >= 300:
            return []
        pics = []
        imgs = res['images_results']
        for i in range(min(10, len(imgs))):
            item = imgs[i]
            #print(json.dumps(item,indent=4,ensure_ascii=False))
            pics.append({
                'title':item['title'],
                'thumbnail': item['thumbnail'],
                'original':  item['original'],
                'width': item['original_width'],
                'height': item['original_height'],
            })
        return pics
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return []

if __name__ == '__main__':
    query = sys.argv[1]
    res = search_google_image(query)
    print(json.dumps(res, indent=4, ensure_ascii=False))

