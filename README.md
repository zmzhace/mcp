# MCP 服务器

这是一个使用 FastMCP 构建的功能丰富的 MCP (Model Context Protocol) 服务器。

## 功能

这个 MCP 服务器提供了以下工具：

### 🔧 基础工具
1. **hello** - 返回问候消息
   - 参数：`name` (字符串) - 要问候的人名

2. **getTime** - 获取当前时间
   - 参数：`format` (可选) - 时间格式 ('iso', 'local', 'timestamp')

3. **calculate** - 执行基本数学计算
   - 参数：
     - `operation` (字符串) - 运算类型 ('add', 'subtract', 'multiply', 'divide')
     - `a` (数字) - 第一个数字
     - `b` (数字) - 第二个数字

### 🌤️ 网络服务
4. **getWeather** - 获取天气信息
   - 参数：
     - `city` (字符串) - 城市名称
     - `country` (可选) - 国家代码，默认 "CN"

5. **translate** - 翻译文本
   - 参数：
     - `text` (字符串) - 要翻译的文本
     - `target_lang` (字符串) - 目标语言，默认 "en"
     - `source_lang` (可选) - 源语言，默认 "auto"

6. **checkNetwork** - 检查网络连接
   - 参数：
     - `url` (字符串) - 要检查的URL，默认 "https://www.google.com"

7. **getJoke** - 获取笑话
   - 参数：
     - `category` (可选) - 笑话类别，默认 "any"

### 📁 文件操作
8. **fileRead** - 读取本地文件
   - 参数：
     - `path` (字符串) - 文件路径
     - `encoding` (可选) - 文件编码，默认 "utf-8"

9. **fileWrite** - 写入本地文件
   - 参数：
     - `path` (字符串) - 文件路径
     - `content` (字符串) - 文件内容
     - `encoding` (可选) - 文件编码，默认 "utf-8"

10. **fileList** - 列出目录内容
    - 参数：
      - `path` (字符串) - 目录路径，默认 "."

### 🔐 加密工具
11. **hashText** - 对文本进行哈希计算
    - 参数：
      - `text` (字符串) - 要哈希的文本
      - `algorithm` (字符串) - 哈希算法 ('md5', 'sha1', 'sha256', 'sha512')，默认 "md5"

12. **base64Encode** - Base64编码或解码
    - 参数：
      - `text` (字符串) - 要处理的文本
      - `encode` (布尔值) - 是否编码，默认 true

### 💻 系统信息
13. **getSystemInfo** - 获取系统信息
    - 参数：无

14. **getProcessInfo** - 获取进程信息
    - 参数：
      - `name` (可选) - 进程名称，不提供则显示所有进程

## 安装

```bash
# 安装 uv (如果还没有安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建 Python 3.10 虚拟环境
source $HOME/.local/bin/env
uv venv --python 3.10

# 激活虚拟环境并安装依赖
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 运行

### 方法1：使用启动脚本
```bash
./start_server.sh
```

### 方法2：手动启动
```bash
source $HOME/.local/bin/env
source .venv/bin/activate
python main.py
```

### 后台运行
```bash
# 在后台启动服务器
nohup python main.py > mcp.log 2>&1 &

# 或者使用启动脚本
nohup ./start_server.sh > mcp.log 2>&1 &
```

## 测试

### 基本测试
```bash
# 运行基本测试（检查配置、依赖、启动）
python test_basic.py
```

### 停止服务器
```bash
./stop_server.sh
```

## 使用示例

### 基础工具
```json
{
  "name": "hello",
  "arguments": {
    "name": "张三"
  }
}
```

```json
{
  "name": "calculate",
  "arguments": {
    "operation": "add",
    "a": 10,
    "b": 5
  }
}
```

### 网络服务
```json
{
  "name": "getWeather",
  "arguments": {
    "city": "北京"
  }
}
```

```json
{
  "name": "translate",
  "arguments": {
    "text": "你好世界",
    "target_lang": "en"
  }
}
```

### 文件操作
```json
{
  "name": "fileList",
  "arguments": {
    "path": "/Users/username/Documents"
  }
}
```

```json
{
  "name": "fileWrite",
  "arguments": {
    "path": "test.txt",
    "content": "Hello World!"
  }
}
```

### 加密工具
```json
{
  "name": "hashText",
  "arguments": {
    "text": "Hello World",
    "algorithm": "sha256"
  }
}
```

### 系统信息
```json
{
  "name": "getSystemInfo",
  "arguments": {}
}
```

## 配置

服务器配置在 `main.py` 文件中，你可以根据需要修改服务器名称、版本和描述。

## 添加新工具

要添加新工具，在 `main.py` 文件中使用装饰器：

```python
@mcp.tool("toolName")
def tool_function(params: YourParamsModel) -> str:
    """工具描述"""
    # 工具逻辑
    return "返回内容"
```

## 依赖

- `fastmcp` - FastMCP 框架
- `pydantic` - 数据验证和设置管理
- `requests` - HTTP 请求库

## 日志

服务器运行时会输出日志到控制台。如果使用后台运行，日志会保存到 `mcp.log` 文件中。

## 文件结构

```
mcp/
├── main.py              # 主服务器文件
├── requirements.txt     # Python 依赖
├── start_server.sh      # 启动脚本
├── stop_server.sh       # 停止脚本
├── test_basic.py        # 基本测试脚本
├── README.md           # 文档
├── .gitignore          # Git 忽略文件
└── .venv/              # Python 虚拟环境
```

## 注意事项

1. **网络服务**：天气、翻译、笑话等功能需要网络连接
2. **文件权限**：文件操作工具需要适当的文件系统权限
3. **系统信息**：系统信息工具在 macOS 上工作最佳
4. **API 限制**：某些免费 API 可能有请求频率限制 