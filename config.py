#!/usr/bin/env python3
"""
MCP 服务器配置文件
"""

import os
from typing import Dict, Any

# ==================== 服务器配置 ====================

class ServerConfig:
    """服务器配置"""
    
    # 基本配置
    NAME = "my-mcp-server"
    VERSION = "1.0.0"
    DESCRIPTION = "功能丰富的 MCP 服务器，提供多种实用工具"
    
    # HTTP 服务器配置
    HOST = "0.0.0.0"
    PORT = 8000
    
    # 日志配置
    LOG_LEVEL = "INFO"
    DEBUG = False
    
    # 安全配置
    ALLOWED_ORIGINS = ["*"]  # CORS 配置
    MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB
    
    # 超时配置
    REQUEST_TIMEOUT = 30  # 秒
    TOOL_TIMEOUT = 60  # 秒

# ==================== 工具配置 ====================

class ToolConfig:
    """工具配置"""
    
    # 天气 API 配置
    WEATHER_API_URL = "http://wttr.in"
    WEATHER_TIMEOUT = 10
    
    # 翻译 API 配置
    TRANSLATE_API_URL = "https://translate.googleapis.com/translate_a/single"
    TRANSLATE_TIMEOUT = 10
    
    # 笑话 API 配置
    JOKE_API_URL = "https://v2.jokeapi.dev/joke"
    JOKE_TIMEOUT = 10
    
    # 文件操作配置
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_EXTENSIONS = [".txt", ".json", ".py", ".md", ".log"]
    RESTRICTED_PATHS = ["/etc", "/var", "/usr", "/bin", "/sbin"]
    
    # 网络检查配置
    DEFAULT_NETWORK_TEST_URL = "https://www.google.com"
    NETWORK_TIMEOUT = 10

# ==================== 环境配置 ====================

class EnvironmentConfig:
    """环境配置"""
    
    # 开发环境
    DEVELOPMENT = {
        "debug": True,
        "log_level": "DEBUG",
        "host": "localhost",
        "port": 8000
    }
    
    # 生产环境
    PRODUCTION = {
        "debug": False,
        "log_level": "INFO",
        "host": "0.0.0.0",
        "port": 8000
    }
    
    # 测试环境
    TESTING = {
        "debug": True,
        "log_level": "DEBUG",
        "host": "localhost",
        "port": 8001
    }

# ==================== 工具列表配置 ====================

TOOLS_CONFIG = {
    "hello": {
        "description": "返回一个问候消息",
        "category": "basic",
        "enabled": True
    },
    "getTime": {
        "description": "获取当前时间",
        "category": "basic",
        "enabled": True
    },
    "calculate": {
        "description": "执行基本数学计算",
        "category": "basic",
        "enabled": True
    },
    "getWeather": {
        "description": "获取天气信息",
        "category": "external",
        "enabled": True
    },
    "translate": {
        "description": "翻译文本",
        "category": "external",
        "enabled": True
    },
    "fileRead": {
        "description": "读取本地文件",
        "category": "file",
        "enabled": True
    },
    "fileWrite": {
        "description": "写入本地文件",
        "category": "file",
        "enabled": True
    },
    "fileList": {
        "description": "列出目录内容",
        "category": "file",
        "enabled": True
    },
    "hashText": {
        "description": "对文本进行哈希计算",
        "category": "utility",
        "enabled": True
    },
    "base64Encode": {
        "description": "Base64编码或解码",
        "category": "utility",
        "enabled": True
    },
    "getSystemInfo": {
        "description": "获取系统信息",
        "category": "system",
        "enabled": True
    },
    "getProcessInfo": {
        "description": "获取进程信息",
        "category": "system",
        "enabled": True
    },
    "checkNetwork": {
        "description": "检查网络连接",
        "category": "network",
        "enabled": True
    },
    "getJoke": {
        "description": "获取笑话",
        "category": "entertainment",
        "enabled": True
    }
}

# ==================== 工具分类 ====================

TOOL_CATEGORIES = {
    "basic": "基础工具",
    "external": "外部服务",
    "file": "文件操作",
    "utility": "实用工具",
    "system": "系统信息",
    "network": "网络工具",
    "entertainment": "娱乐工具"
}

# ==================== 配置获取函数 ====================

def get_config(env: str = None) -> Dict[str, Any]:
    """获取配置"""
    if env is None:
        env = os.getenv("MCP_ENV", "development").lower()
    
    config = {
        "server": ServerConfig,
        "tools": ToolConfig,
        "environment": EnvironmentConfig,
        "tools_config": TOOLS_CONFIG,
        "categories": TOOL_CATEGORIES
    }
    
    # 根据环境设置配置
    if env == "production":
        config.update(EnvironmentConfig.PRODUCTION)
    elif env == "testing":
        config.update(EnvironmentConfig.TESTING)
    else:
        config.update(EnvironmentConfig.DEVELOPMENT)
    
    return config

def get_enabled_tools() -> list:
    """获取启用的工具列表"""
    return [name for name, config in TOOLS_CONFIG.items() if config.get("enabled", True)]

def get_tools_by_category(category: str) -> list:
    """根据分类获取工具列表"""
    return [name for name, config in TOOLS_CONFIG.items() 
            if config.get("category") == category and config.get("enabled", True)] 