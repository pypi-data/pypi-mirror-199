#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import json
import random
import requests
import traceback
import sqlite3

from reasoningchain.executor.sandbox import execute_python
from reasoningchain.cache.disk_cache import disk_cache
from reasoningchain import api

from .base import custom_tool, CACHE_DIR

@disk_cache(cache_path=os.path.join(CACHE_DIR, "baidu_search_text.db"), expire_time=86400*2)
def baidu_search_text(query:str):
    return api.baidu.search_text(query)

@custom_tool(
    name = "BaiduSearchText",
    description = "A search engine. Useful for when you need to search textual information about facts and current events. Never use it to do math calculations. Input should be a query for the search engine."
)
def baidu_search_text_tool(query:str, callback:callable=None) -> str:
    query = query.strip()
    if not query:
        return "No invalid query. "
    result = baidu_search_text(query) # 空结果不缓存
    if result:
        if callback:
            result = callback(query, result)
        return '搜索结果：' + result.replace("\n", " ")
    return "Nothing is found. "

@disk_cache(cache_path=os.path.join(CACHE_DIR, "google_search_image.db"), expire_time=86400*7)
def google_search_image(query:str):
    return api.google.search_image(query)

@disk_cache(cache_path=os.path.join(CACHE_DIR, "google_search_map.db"), expire_time=86400*7)
def google_search_map(query:str, callback:callable=None):
    return api.google.search_map(query)

@custom_tool(
    name = "GoogleSearchImage",
    description = "A search engine for images. Useful for when you need to find an image or a picture from the web or you are asked what somebody or something looks like. Input should be a query for the image search engine."
)
def google_search_image_tool(query:str, callback:callable=None) -> str:
    query = query.strip()
    if not query:
        return "No invalid query. "
    results = google_search_image(query) # 空结果不缓存
    if not results:
        return "Nothing is found."
    url = results[int(random.random()*len(results))]["original"]
    if callback:
        url = callback(query, url)
    return "An image is found:" + url

@custom_tool(
    name = "GoogleSearchMap",
    description = "A search engine for locations on map. Useful for when you need to find the position of somewhere on the map. Input should be a query in Chinese for the map search engine."
)
def google_search_map_tool(query:str, callback:callable=None) -> str:
    query = query.strip()
    if not query:
        return "No invalid query. "
    loc = google_search_map(query) # 空结果不缓存
    if not loc:
        return "Nowhere is found."
    if callback is not None:
        loc = callback(query, loc)
    return 'I found the place, it\'s at %s, gps:{"latitude":%f, "longitude":%f}' % (loc['address'], loc['latitude'], loc['longitude'])

@custom_tool(
    name = "PythonExecutor",
    description = "A python code executor. Usefull for when you have a piece of python codes to execute. Input should be the codes to be executed. You can get the execution output by using print(). "
)
def python_executor_tool(codes:str, callback:callable=None):
    try:
        out = execute_python(codes)
        res = f'Execution output: {out}'
    except Exception as e:
        out = ''
        res = "Caught exception: " + str(e)
    if callback is not None:
        callback(codes, out)
    return res

@custom_tool(
    name = "Calculator",
    description = "A calculator. Usefull for when you need to solve a math problem. Input should be a piece of python codes. The codes should be a COMPLETE program with necessary modules included so I can execute it successfully. The final answer should be printed out to the console using print() function so we can get it. "
)
def python_calculator_tool(codes:str, callback:callable=None):
    try:
        out = execute_python(codes)
        res = f'Execution output: {out}'
    except Exception as e:
        out = ''
        res = "Caught exception: " + str(e)
    if callback is not None:
        callback(codes, out)
    return res

@custom_tool(
    name = 'SearchStudentScores',
    description = "A search tool for query or calculating studentss examination scores. Useful for when you need to query or calcualate students examination scores. The scores data are stored in a MySQL database table named student_scores, and its columns includes (exam_year: year of examinations date. exam_date: examinations date.  teacher_name: teacher name of the examination course.  class_name: class name of the student.  student_name: student name. course_name: course name. score: score of the examination.) Input should be a SQL to retrieving or calculating the data you want. The output would be in json format. "
)
def search_student_scores_tool(sql:str, callback:callable=None) -> str:
    sql = sql.strip()
    if sql.endswith('"'):
        sql = sql[:-1]
    if not sql:
        return "I got empty input and can do nothing."

    try:
        conn = sqlite3.connect("/home/work/llmui/db/student_center.db")
        csr = conn.cursor()
        x = []
        y = []
        for date, score in csr.execute(sql):
            print(f'date:{date} score:{score}')
            x.append(date)
            y.append(score)
        res = {
            'x_name':'exam_date',
            'x_data': x,
            'y_name':'score',
            'y_data': y,
        }
        if callback is not None:
            res = callback(sql, res)
        return f'Here is the data you want in json format:' + json.dumps(res, ensure_ascii=False)
    except Exception as e:
        print("[SearchStudentScores::_run()] Caught exception:", e, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    return "I didn't find any data for your request."

class DBHelper:
    def __init__(self, dbname):
        self._dbname = dbname
        self._conn = sqlite3.connect(dbname)

    def execute(self, sql, commit=False):
        csr = self._conn.cursor()
        res = csr.execute(sql)
        if commit:
            self.commit()
        return res

    def commit(self):
        return self._conn.commit()

    def close(self):
        self._conn.close()


@disk_cache(cache_path=os.path.join(CACHE_DIR, "weather_forcast.db"), expire_time=7200)
def get_daily_weather_forecast(area_name):
    return api.weather.get_daily_weather_forecast(area_name)

@custom_tool(
    name = 'WeatherForecast',
    description = "A weather tool. Useful for when you need to answer questions about the weather or when you need to check what the weather will look like in the future. Input should be the date and the location in Chinese in format like this:(时间, 地点). "
)
def weather_forcast_tool(query:str, callback:callable=None):
    parts = query.split(',', 1)
    if len(parts) > 1:
        date, area_name = parts
    else:
        date = query
        area_name = ''
    area_name = area_name.strip(' "')
    date = date.strip(' "')
    if area_name.lower() == 'current location' or not area_name:
        area_name = '北京'
    print(f"[weather_forcast] area_name:{area_name}", file=sys.stderr)

    daily_weather_forcast = get_daily_weather_forecast(area_name)
    if not daily_weather_forcast:
        return 'Nothing is found. '

    if callback is not None:
        daily_weather_forcast = callback(query, daily_weather_forcast)

    weather = ''

    for i in range(len(daily_weather_forcast)):
        item = daily_weather_forcast[i]
        parts = [
            f'天气为{item["text_day"]}',
            f'最高气温{item["high_temp"]}摄氏度，最低气温{item["low_temp"]}摄氏度',
        ]
        if item.get('wc_day', None):
            parts.append(f'风速{item["wind_class_day"]}')
        if item.get('wd_day', None):
            parts.append(f'风向{item["wind_direction_day"]}')
        weather += item['date_name'] + '，'.join(parts) + '。'
    return weather

@custom_tool(
    name = "Scheduler",
    description = "A scheduler. Useful for when you need to query or manipulating schedules. Input should be the operation which should be one of [query, add, delete], time, content. "
)
def scheduler_tool(query:str, callback:callable=None) -> str:
    parts = query.split(',', 2)
    if len(parts) != 3:
        return "Sorry, I can not understand your input."

    op, tm, content = parts
    op = op.lower()
    if op == 'query':
        return 'Found a schedule on {tm.lower()}: travelling to Shanghai.'
    elif op == 'delete':
        return 'Schedule canceled.'
    elif op == 'add':
        return f'Schedule added on {tm.lower()}.'
    return "Sorry, operation \"{op}\" is not supported."


def _search_music(name):
    musics = {
        '爷爷的情书': {
            'type':'video',
            'alias':['A love letter from Grandpa', "Grandpa's Love Letter"],
            'url':'https://topcoder.top/static/videos/yydqs.mp4',
        },
        '半兽人': {
            'type':'video',
            'alias':['Half Beast', 'Half Orc'],
            'url':'https://topcoder.top/static/videos/banshouren.mp4',
        },
    }
    print(f"music name:[\x1b[32m{name}\x1b[0m]", file=sys.stderr)
    if name in musics:
        return musics[name]
    cname = name.lower().replace('-', ' ').strip()
    for k, v in musics.items():
        if name in k:
            return v
        for alias in v.get('alias', []):
            alias = alias.lower().replace('-', ' ').strip()
            if alias == cname:
                return v
    return None

@custom_tool(
    name = "MusicPlayer",
    description = (
        "A music player. "
        "Useful for when you have a piece of music or a song to search and play. "
        "Input should be name of the music or the song. "
    )
)
def music_player_tool(query:str, callback:callable=None) -> str:
    query = query.strip(' \n')
    if query.endswith('"'):
        query = query[:-1]
    name = query
    music = _search_music(name)
    if music:
        if callback:
            callback(query, music)
        return 'I found the music, and player starts playing it.'
    return "Sorry, I didn't found the music. Try again with a Chinese music name. "

@custom_tool(
    name = "BookTicket",
    description = (
        "A tool for booking tickets."
        "Useful for when you need to book or buy tickets. "
        "Input should be ticket type, destination, time. The ticket type should be one of [train, plane, entrance]. "
    )
)
def book_ticket_tool(query:str, callback:callable=None) -> str:
    parts = query.split(',', 2)
    if len(parts) != 3:
        return "Sorry, I can not understand your input."

    tt, destination, tm = parts
    tt = tt.lower()
    return 'The ticket has beend ordered successfully. '

@custom_tool(
    name = "HomeCircumstances",
    description = (
        "A tool for querying circumstances of home."
        "Useful for when you need to check the temperature of a room. "
        "Input should be the room name. "
    )
)
def home_circumstance_tool(query:str, callback:callable=None) -> str:
    query = query.strip(' "')
    return f'The temperature of {query} is 19 degrees. '

@custom_tool(
    name = "IOTControler",
    description = (
        "A tool for controling smart devices."
        "Useful for when you need to turn on or turn off a light, set up a air conditioning or other smart devices. "
        "Input should be the device name. "
    )
)
def iot_control_tool(query:str, callback:callable=None) -> str:
    query = query.strip(' "')
    return 'Operation success. '

@disk_cache(cache_path=os.path.join(CACHE_DIR, "closeai_generate_image.db"), expire_time=3600)
def generate_image(prompt):
    return api.closeai.generate_image(prompt)

@custom_tool(
    name = "OpenaiAIPainter",
    description = (
        "An AI painter. "
        "Useful for when you need to draw or paint or generate an image or a picture. With this tool, you are a painter and can paint or draw anything. "
        "Input should be a prompt for the AI painter depicting what image you want to draw. The output is the url of the image."
    )
)
def ai_paint(prompt:str, callback:callable=None) -> str:
    prompt = prompt.strip()
    if not prompt:
        return 'I got empty input and can do nothing.'

    urls = generate_image(prompt)
    if not urls:
        return "Error occured while drawing the image."

    res_url = urls[0]
    if callback:
        callback(prompt, res_url)
    return f"Here is the painted image's url:{res_url}"

@custom_tool(
    name="SendMessage",
    description="Message Sender. Useful for when you need to send a message to somebody. Input should be (user:the target user, mesage:the message to be sent). "
)
def send_message_tool(arg:str):
    to_user, message = arg.split(',', 1)
    print(f"sending message to \x1b[32m{to_user}\x1b[0m:{message}")
    return "The message has been sent successfully."

if __name__ == '__main__':
    print('custom tools:', get_all_custom_tool_names())

    def on_weather(query, result):
        print(f"on_weather()  query=[{query}]")
        print(f"on_weather() result=[{result}]")
        return result
    def on_ai_paint(query, result):
        print(f"on_ai_paint()  query=[{query}]")
        print(f"on_ai_paint() result=[{result}]")
        return result
    def on_search_text(query, result):
        print(f"on_search_text()  query=[{query}]")
        print(f"on_search_text() result=[{result}]")
        return result
    tools = load_tools(["AIPainter", "WeatherForecast", "BaiduSearchText"], {
        'AIPainter': on_ai_paint,
        'WeatherForecast': on_weather,
        'BaiduSearchText': on_search_text,
    })

    for tool in tools:
        print(tool.name)

