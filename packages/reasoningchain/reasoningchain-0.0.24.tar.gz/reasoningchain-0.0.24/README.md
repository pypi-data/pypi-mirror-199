# ReasoningChain

## 给接口增加本地缓存

```python3
from reasoningchain.cache.disk_cache import disk_cache

@disk_cache(cache_path=os.path.join(os.environ["HOME"], "some_path/some_name"), expire_time=864000)
def foobar(key:str):
    """do something"""
    pass
```

## 获取文本向量

```python3
from reasoningchain.api.closeai import batch_get_embeddings

embeddings = batch_get_embeddings(["hello", "world"], batch_size=16)
```

## 构建文本向量索引

```python3
from reasoningchain.index.doc_index import DocIndex

doc_index = DocIndex()
doc_index.build(doc_full_text)    # 构建索引
doc_index.save(index_file_path)   # 保存索引到文件

doc_index.load(index_file_path)   # 从文件加载索引

results = doc_index.search(query) # 查询索引
```

## 自定义langchain Tools

```python
from reasoningchain.custom_tools import custom_tool
from reasoningchain.custom_tools import get_all_tool_names
from reasoningchain.custom_tools import get_all_custom_tool_names
from reasoningchain.custom_tools import load_tools

# 增加自定义tool
@custom_tool(
    name = "{{Tool Name}}",
    description = "{{Tool Descriptions}}"
)
def tool_func(input_text:str, callback:callable=None) -> str:
    """do something"""
    pass

# 获取所有自定义的tool names
all_custom_tool_names = get_all_custom_tool_names()

# 获取所有tool names（包括自定义的tool 和 langchain中预定义的tool）
all_tool_names = get_all_tool_names()

# 加载tools
tools = load_tools(["BaiduSearchText", "GoogleSearchImage", "wikipedia"])
```

# 运行chain

* 代码中调用：
```python
import reasoningchain

final_answer = reasoningchain.run("介绍一下小度", tool_names=["BaiduSearchText"])

print(f"Final Answer:{final_answer}")
```

* 命令行：
```sh
# 单query
reasoningchain --tools "BaiduSearchText" --query "马斯克是谁?"

# 批量处理
cat queries.txt | reasoningchain --tools "BaiduSearchText"
```

* 启动WebUI服务：
```sh
reasoningchainui --port 8502
```

## 参数配置
```python3
# 通过环境变量设置参数

# 使用BaiduSearchText时需设置
os.environ['BAIDU_SEARCH_API'] = 'https://m.baidu.com/...'

# 使用openai相关接口时需设置
os.environ['OPENAI_API_KEY'] = '123'
# 需要对openai做代理时可设置
os.environ['OPENAI_API_BASE'] = '代理地址'

# 使用serpapi时需设置，包括google的搜索API
os.environ['SERPAPI_API_KEY'] = 'SERP API-KEY'

# 使用WOLFRAM ALPHA Tool时需设置
os.environ['WOLFRAM_ALPHA_APPID'] = 'walfram-alpha appid'

# 使用DuLLM时需设置
os.environ['DU_LLM_API'] = 'http://...' # 内部自定义LLM的API
```

