#!/usr/bin/env python3
"""
MCP HTTP 服务器主文件
使用标准 MCP 协议，提供丰富的工具功能
"""

import asyncio
from fastmcp import FastMCP
from config import ServerConfig, get_config
from tools import register_tools

async def main():
    """主函数"""
    # 获取配置
    config = get_config()
    
    # 创建 FastMCP 实例
    mcp = FastMCP(
        name=ServerConfig.NAME,
        version=ServerConfig.VERSION,
        instructions=ServerConfig.DESCRIPTION
    )
    
    # 注册所有工具
    register_tools(mcp)
    
    print("🚀 启动 MCP HTTP 服务器...")
    print(f"📋 服务器名称: {ServerConfig.NAME}")
    print(f"📋 版本: {ServerConfig.VERSION}")
    print(f"📋 描述: {ServerConfig.DESCRIPTION}")
    print(f"🌐 服务地址: http://{ServerConfig.HOST}:{ServerConfig.PORT}/mcp/")
    print(f"🔧 可用工具数量: {len(get_config()['tools_config'])}")
    
    # 启动 HTTP 服务器
    await mcp.run_http_async(
        host=ServerConfig.HOST,
        port=ServerConfig.PORT,
        show_banner=True,
        log_level=ServerConfig.LOG_LEVEL
    )

if __name__ == "__main__":
    asyncio.run(main()) 