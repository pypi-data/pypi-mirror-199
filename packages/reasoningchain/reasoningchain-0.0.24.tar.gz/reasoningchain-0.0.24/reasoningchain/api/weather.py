#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import json
import requests
import traceback
import shelve

from langchain.tools.base import BaseTool

def get_area_code(area_name) -> None:
    if not area_name:
        return None

    api_key = os.environ.get('WEATHER_API_KEY', None)
    if not api_key:
        return None

    url = 'https://eolink.o.apispace.com/456456/function/v001/city?items=10&area=china&withPoi=false&location=' + area_name
    try:
        resp = requests.get(url, headers={
            'X-APISpace-Token': api_key,
            'Authorization-Type':'apikey',
        })
        if resp.status_code >= 300:
            print(f"Request weather api failed, http status code:{resp.status_code}", file=sys.stderr)
            return None

        res = json.loads(resp.content)
        if type(res) is not dict or res.get('status', -1) != 0:
            print(f'Failed to request area codeof [{area_name}], response:{resp.content}', file=sys.stderr)
            return ''

        area_code = res['areaList'][0]['areacode'].strip()
        #print(f'Got area code [{area_code}] of [{area_name}] ...', file=sys.stderr)
        return area_code
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return None

def get_daily_weather_forecast(area_name):
    area_name = area_name.strip(' "')
    if not area_name:
        return []

    api_key = os.environ.get('WEATHER_API_KEY', None)
    if not api_key:
        return []

    #print(f"[get_daily_weather_info] area_name:{area_name}", file=sys.stderr)
    area_code = get_area_code(area_name)
    if not area_code:
        return []

    url = 'https://eolink.o.apispace.com/456456/weather/v001/day?days=5&areacode=' + area_code
    try:
        resp = requests.get(url, headers={
            'X-APISpace-Token': api_key,
            'Authorization-Type':'apikey',
        })
        if resp.status_code >= 300:
            print(f"Request weather api failed, http status code:{resp.status_code}", file=sys.stderr)
            return []
        res = json.loads(resp.content)
        if type(res) is not dict or len(res.get('result', [])) == 0:
            return []
        res_list = []
        day_names = ['明天', '后天', '大后天', '4天后']
        fcsts = res['result']['daily_fcsts']
        for i in range(len(fcsts)):
            item = fcsts[i]
            res_list.append({
                'date':item['date'],
                'date_name': day_names[i] if i < len(day_names) else f'{i+1}天后',
                'text_day':item['text_day'],
                'text_night':item['text_night'],
                'high_temp':item['high'],
                'low_temp':item['low'],
                'wind_class_day':item['wc_day'],
                'wind_class_night':item['wc_night'],
                'wind_direction_day':item['wd_day'],
                'wind_direction_night':item['wd_night'],
            })
        return res_list
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return None

if __name__ == '__main__':
    query = sys.argv[1]
    res = get_daily_weather_forecast(query)
    print(json.dumps(res, indent=4, ensure_ascii=False))

