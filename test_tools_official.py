#!/usr/bin/env python3
"""
使用 fastmcp 官方客户端库测试所有工具
"""

import asyncio
from fastmcp import Client
from config import get_config, TOOL_CATEGORIES

async def test_tools():
    print("🧪 使用官方客户端测试 MCP 工具...")
    
    # 连接到 MCP 服务器
    async with Client("http://localhost:8000/mcp/") as client:
        print("✅ 已连接到 MCP 服务器")
        
        # 获取工具列表
        tools = await client.list_tools()
        print(f"📋 可用工具: {[tool.name for tool in tools]}")
        
        # 按分类测试工具
        config = get_config()
        tools_config = config['tools_config']
        categories = config['categories']
        
        for category, category_name in categories.items():
            category_tools = [name for name, cfg in tools_config.items() 
                            if cfg.get("category") == category and cfg.get("enabled", True)]
            
            if category_tools:
                print(f"\n📂 {category_name}:")
                
                for tool_name in category_tools[:2]:  # 每个分类只测试前2个工具
                    print(f"  🔹 测试 {tool_name}:")
                    
                    try:
                        result = await test_single_tool(client, tool_name)
                        print(f"    结果: {result}")
                    except Exception as e:
                        print(f"    ❌ 错误: {e}")

async def test_single_tool(client, tool_name):
    """测试单个工具"""
    test_params = {
        "hello": {"params": {"name": "测试用户"}},
        "getTime": {"params": {"format": "local"}},
        "calculate": {"params": {"operation": "add", "a": 5, "b": 3}},
        "getWeather": {"params": {"city": "Beijing"}},
        "translate": {"params": {"text": "Hello World", "target_lang": "zh"}},
        "fileList": {"params": {"path": "."}},
        "hashText": {"params": {"text": "test", "algorithm": "md5"}},
        "base64Encode": {"params": {"text": "Hello", "encode": True}},
        "getSystemInfo": {"params": {}},
        "getProcessInfo": {"params": {}},
        "checkNetwork": {"params": {"url": "https://www.google.com"}},
        "getJoke": {"params": {"category": "any"}}
    }
    
    if tool_name in test_params:
        result = await client.call_tool(tool_name, test_params[tool_name])
        return result.content[0].text if result.content else str(result.content)
    else:
        return "无测试参数"

def main():
    """主函数"""
    print("🚀 开始测试 MCP 工具...")
    print("=" * 60)
    
    try:
        asyncio.run(test_tools())
        print("\n" + "=" * 60)
        print("✅ 测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("💡 请确保 MCP 服务器正在运行")

if __name__ == "__main__":
    main() 