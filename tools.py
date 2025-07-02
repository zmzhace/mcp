#!/usr/bin/env python3
"""
MCP 工具模块
包含所有可用的工具函数
"""

import os
import json
import hashlib
import base64
import subprocess
import requests
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

# ==================== 参数模型 ====================

class HelloParams(BaseModel):
    name: str

class GetTimeParams(BaseModel):
    format: Optional[str] = "iso"

class CalculateParams(BaseModel):
    operation: str
    a: float
    b: float

class WeatherParams(BaseModel):
    city: str
    country: Optional[str] = "CN"

class TranslateParams(BaseModel):
    text: str
    target_lang: str = "en"
    source_lang: Optional[str] = "auto"

class FileReadParams(BaseModel):
    path: str
    encoding: Optional[str] = "utf-8"

class FileWriteParams(BaseModel):
    path: str
    content: str
    encoding: Optional[str] = "utf-8"

class FileListParams(BaseModel):
    path: str = "."

class HashParams(BaseModel):
    text: str
    algorithm: str = "md5"

class Base64Params(BaseModel):
    text: str
    encode: bool = True

class SystemInfoParams(BaseModel):
    pass

class ProcessInfoParams(BaseModel):
    name: Optional[str] = None

class NetworkCheckParams(BaseModel):
    url: str = "https://www.google.com"

class JokeParams(BaseModel):
    category: Optional[str] = "any"

# ==================== 工具函数 ====================

def hello(params: HelloParams) -> str:
    """返回一个问候消息"""
    return f"你好，{params.name}！欢迎使用MCP服务器！"

def get_time(params: GetTimeParams) -> str:
    """获取当前时间"""
    now = datetime.now()
    
    if params.format == "iso":
        time_string = now.isoformat()
    elif params.format == "local":
        time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif params.format == "timestamp":
        time_string = str(now.timestamp())
    else:
        time_string = now.isoformat()
    
    return f"当前时间: {time_string}"

def calculate(params: CalculateParams) -> str:
    """执行基本数学计算"""
    operation = params.operation.lower()
    a = params.a
    b = params.b
    
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("不能除以零")
        result = a / b
    else:
        raise ValueError("不支持的运算")
    
    return f"{a} {operation} {b} = {result}"

def get_weather(params: WeatherParams) -> str:
    """获取天气信息"""
    try:
        url = f"http://wttr.in/{params.city}?format=j1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data.get('current_condition', [{}])[0]
            
            weather_info = f"🌤️ {params.city} 天气信息:\n"
            weather_info += f"温度: {current.get('temp_C', 'N/A')}°C\n"
            weather_info += f"体感温度: {current.get('FeelsLikeC', 'N/A')}°C\n"
            weather_info += f"湿度: {current.get('humidity', 'N/A')}%\n"
            weather_info += f"天气: {current.get('lang_zh', [{}])[0].get('value', 'N/A')}\n"
            weather_info += f"风速: {current.get('windspeedKmph', 'N/A')} km/h"
            
            return weather_info
        else:
            return f"获取天气信息失败: {response.status_code}"
            
    except Exception as e:
        return f"获取天气信息时发生错误: {str(e)}"

def translate(params: TranslateParams) -> str:
    """翻译文本"""
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params_dict = {
            'client': 'gtx',
            'sl': params.source_lang,
            'tl': params.target_lang,
            'dt': 't',
            'q': params.text
        }
        
        response = requests.get(url, params=params_dict, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            translated_text = ''.join([sentence[0] for sentence in data[0] if sentence[0]])
            return f"翻译结果:\n原文: {params.text}\n译文: {translated_text}"
        else:
            return f"翻译失败: {response.status_code}"
            
    except Exception as e:
        return f"翻译时发生错误: {str(e)}"

def file_read(params: FileReadParams) -> str:
    """读取本地文件"""
    try:
        if not os.path.exists(params.path):
            return f"❌ 文件不存在: {params.path}"
        
        with open(params.path, 'r', encoding=params.encoding) as f:
            content = f.read()
        
        return f"文件 {params.path} 内容:\n{content}"
        
    except PermissionError:
        return f"❌ 没有权限读取文件: {params.path}"
    except UnicodeDecodeError:
        return f"❌ 文件编码错误: {params.path}"
    except Exception as e:
        return f"❌ 读取文件时发生错误: {str(e)}"

def file_write(params: FileWriteParams) -> str:
    """写入本地文件"""
    try:
        os.makedirs(os.path.dirname(params.path), exist_ok=True)
        
        with open(params.path, 'w', encoding=params.encoding) as f:
            f.write(params.content)
        
        return f"✅ 文件已写入: {params.path}"
        
    except PermissionError:
        return f"❌ 没有权限写入文件: {params.path}"
    except Exception as e:
        return f"❌ 写入文件时发生错误: {str(e)}"

def file_list(params: FileListParams) -> str:
    """列出目录内容"""
    try:
        if not os.path.exists(params.path):
            return f"❌ 路径不存在: {params.path}"
        
        items = os.listdir(params.path)
        files = []
        dirs = []
        
        for item in items:
            item_path = os.path.join(params.path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append(f"📄 {item} ({size} bytes)")
            elif os.path.isdir(item_path):
                dirs.append(f"📁 {item}/")
        
        result = f"目录 {params.path} 内容:\n"
        if dirs:
            result += "\n文件夹:\n" + "\n".join(dirs)
        if files:
            result += "\n文件:\n" + "\n".join(files)
        
        return result
        
    except PermissionError:
        return f"❌ 没有权限访问目录: {params.path}"
    except Exception as e:
        return f"❌ 列出目录时发生错误: {str(e)}"

def hash_text(params: HashParams) -> str:
    """对文本进行哈希计算"""
    try:
        text = params.text.encode('utf-8')
        algorithm = params.algorithm.lower()
        
        if algorithm == "md5":
            hash_obj = hashlib.md5(text)
        elif algorithm == "sha1":
            hash_obj = hashlib.sha1(text)
        elif algorithm == "sha256":
            hash_obj = hashlib.sha256(text)
        elif algorithm == "sha512":
            hash_obj = hashlib.sha512(text)
        else:
            return f"❌ 不支持的哈希算法: {algorithm}"
        
        hash_result = hash_obj.hexdigest()
        return f"{algorithm.upper()} 哈希值: {hash_result}"
        
    except Exception as e:
        return f"❌ 计算哈希时发生错误: {str(e)}"

def base64_encode(params: Base64Params) -> str:
    """Base64编码或解码"""
    try:
        if params.encode:
            encoded = base64.b64encode(params.text.encode('utf-8')).decode('utf-8')
            return f"Base64 编码结果: {encoded}"
        else:
            decoded = base64.b64decode(params.text.encode('utf-8')).decode('utf-8')
            return f"Base64 解码结果: {decoded}"
            
    except Exception as e:
        return f"❌ Base64 操作时发生错误: {str(e)}"

def get_system_info(params: SystemInfoParams) -> str:
    """获取系统信息"""
    try:
        info = {}
        
        # CPU 信息
        try:
            result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                info["CPU"] = result.stdout.strip()
        except:
            info["CPU"] = "未知"
        
        # 内存信息
        try:
            result = subprocess.run(["sysctl", "-n", "hw.memsize"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                mem_bytes = int(result.stdout.strip())
                mem_gb = mem_bytes / (1024**3)
                info["内存"] = f"{mem_gb:.1f} GB"
        except:
            info["内存"] = "未知"
        
        # 操作系统信息
        try:
            result = subprocess.run(["sw_vers", "-productName"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                os_name = result.stdout.strip()
                result = subprocess.run(["sw_vers", "-productVersion"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    os_version = result.stdout.strip()
                    info["操作系统"] = f"{os_name} {os_version}"
        except:
            info["操作系统"] = "未知"
        
        result = "系统信息:\n"
        for key, value in info.items():
            result += f"  {key}: {value}\n"
        
        return result
        
    except Exception as e:
        return f"❌ 获取系统信息时发生错误: {str(e)}"

def get_process_info(params: ProcessInfoParams) -> str:
    """获取进程信息"""
    try:
        if params.name:
            result = subprocess.run(
                ["ps", "aux", "|", "grep", params.name],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                return f"进程 {params.name} 信息:\n{result.stdout}"
            else:
                return f"未找到进程: {params.name}"
        else:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.split('\n')[:10]
                return f"系统进程信息 (前10个):\n" + "\n".join(lines)
            else:
                return "获取进程信息失败"
                
    except Exception as e:
        return f"❌ 获取进程信息时发生错误: {str(e)}"

def check_network(params: NetworkCheckParams) -> str:
    """检查网络连接"""
    try:
        response = requests.get(params.url, timeout=10)
        
        if response.status_code == 200:
            return f"✅ 网络连接正常，可以访问 {params.url}"
        else:
            return f"⚠️  网络连接异常，状态码: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return f"❌ 网络连接超时，无法访问 {params.url}"
    except requests.exceptions.ConnectionError:
        return f"❌ 网络连接失败，无法访问 {params.url}"
    except Exception as e:
        return f"❌ 检查网络时发生错误: {str(e)}"

def get_joke(params: JokeParams) -> str:
    """获取笑话"""
    try:
        url = "https://v2.jokeapi.dev/joke/Any"
        if params.category != "any":
            url = f"https://v2.jokeapi.dev/joke/{params.category}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('type') == 'single':
                return f"😄 笑话:\n{data.get('joke', '没有找到笑话')}"
            elif data.get('type') == 'twopart':
                setup = data.get('setup', '')
                delivery = data.get('delivery', '')
                return f"😄 笑话:\n{setup}\n{delivery}"
            else:
                return "没有找到笑话"
        else:
            return f"获取笑话失败: {response.status_code}"
            
    except Exception as e:
        return f"获取笑话时发生错误: {str(e)}"

# ==================== 工具注册函数 ====================

def register_tools(mcp_server):
    """注册所有工具到 MCP 服务器"""
    mcp_server.tool("hello")(hello)
    mcp_server.tool("getTime")(get_time)
    mcp_server.tool("calculate")(calculate)
    mcp_server.tool("getWeather")(get_weather)
    mcp_server.tool("translate")(translate)
    mcp_server.tool("fileRead")(file_read)
    mcp_server.tool("fileWrite")(file_write)
    mcp_server.tool("fileList")(file_list)
    mcp_server.tool("hashText")(hash_text)
    mcp_server.tool("base64Encode")(base64_encode)
    mcp_server.tool("getSystemInfo")(get_system_info)
    mcp_server.tool("getProcessInfo")(get_process_info)
    mcp_server.tool("checkNetwork")(check_network)
    mcp_server.tool("getJoke")(get_joke) 