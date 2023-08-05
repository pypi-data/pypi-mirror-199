import os
import sys
import json
import traceback

from langchain.agents import tools
from langchain.llms.base import BaseLLM

from reasoningchain.executor.sandbox import execute_python
from reasoningchain.cache.disk_cache import disk_cache
from reasoningchain import api

CACHE_DIR = os.environ.get('REASONING_CHAIN_CACHE_PATH', os.path.join(os.environ['HOME'], '.cache'))
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)

CACHE_DIR = os.path.join(CACHE_DIR, 'reasoning_chain')
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)

custom_tool_map = {}
def custom_tool(name:str, description:str):
    def decorator(func:callable):
        custom_tool_map[name] = {
            'name': name,
            'description': description,
            'func': func,
        }
        return func
    return decorator

def get_all_custom_tool_names():
    return [k for k in custom_tool_map]

def get_all_custom_tool_info():
    return {name:info["description"] for name, info in custom_tool_map.items()}

def load_tool(name:str, callback=None, mock_output=None):
    tool_info = custom_tool_map[name]
    tool_func = custom_tool_map[name]['func']
    def func(query:str):
        if mock_output:
            if callback:
                return callback(query, mock_output)
            return mock_output
        if callback is not None:
            return tool_func(query, callback)
        else:
            return tool_func(query)
    return tools.Tool(
        name = name,
        description = tool_info['description'],
        func = func,
    )

def load_custom_tools(tool_names:list, callbacks:dict={}):
    tools = []
    for name in tool_names:
        callback = callbacks.get(name, None) if callbacks else None
        tool = load_tool(name, callback)
        tools.append(tool)
    return tools

def get_all_tool_names():
    from langchain import agents
    return get_all_custom_tool_names() + agents.get_all_tool_names()

def load_tools(tool_names:list, tool_callbacks:dict=None, llm:BaseLLM=None) -> list:
    from langchain import agents

    custom_tool_names = []
    predefined_tool_names = []
    all_agent_tool_names = agents.get_all_tool_names()
    for name in tool_names:
        name = name.strip()
        if not name:
            continue
        if name in get_all_custom_tool_names():
            custom_tool_names.append(name)
        elif name in all_agent_tool_names:
            predefined_tool_names.append(name)
        else:
            raise RuntimeError(f"Unknown tool name:[{name}]")

    tools = []
    if len(custom_tool_names) > 0:
        tools += load_custom_tools(custom_tool_names, tool_callbacks)

    if len(predefined_tool_names) > 0:
        from langchain.llms import OpenAI, OpenAIChat
        if llm is None:
            llm = OpenAIChat(temperature=0)
        tools += agents.load_tools(predefined_tool_names, llm)

    return tools

