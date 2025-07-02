#!/usr/bin/env python3
"""
基本的 MCP 服务器测试脚本
"""

import subprocess
import time
import os

def test_server_startup():
    """测试服务器启动"""
    print("🧪 测试 MCP 服务器启动...")
    
    # 启动服务器
    print("🚀 启动服务器...")
    process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待一段时间
    time.sleep(5)
    
    # 检查进程是否还在运行
    if process.poll() is None:
        print("✅ 服务器启动成功，进程正在运行")
        
        # 停止服务器
        print("🛑 停止服务器...")
        process.terminate()
        process.wait()
        print("✅ 服务器已停止")
        return True
    else:
        stdout, stderr = process.communicate()
        print(f"❌ 服务器启动失败")
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")
        return False

def test_server_config():
    """测试服务器配置"""
    print("\n📋 测试服务器配置...")
    
    # 检查 main.py 文件是否存在
    if not os.path.exists("main.py"):
        print("❌ main.py 文件不存在")
        return False
    
    # 检查 requirements.txt 文件是否存在
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt 文件不存在")
        return False
    
    # 检查虚拟环境是否存在
    if not os.path.exists(".venv"):
        print("❌ 虚拟环境不存在")
        return False
    
    print("✅ 所有配置文件存在")
    return True

def test_dependencies():
    """测试依赖安装"""
    print("\n📦 测试依赖安装...")
    
    try:
        import fastmcp
        print("✅ fastmcp 已安装")
    except ImportError:
        print("❌ fastmcp 未安装")
        return False
    
    try:
        import pydantic
        print("✅ pydantic 已安装")
    except ImportError:
        print("❌ pydantic 未安装")
        return False
    
    return True

def main():
    """主函数"""
    print("🧪 开始基本测试...")
    
    tests = [
        ("配置检查", test_server_config),
        ("依赖检查", test_dependencies),
        ("服务器启动", test_server_startup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有基本测试通过！")
        print("\n💡 提示：")
        print("- 服务器可以正常启动")
        print("- 所有依赖已正确安装")
        print("- 配置文件完整")
        print("\n🚀 现在可以使用以下命令启动服务器：")
        print("  ./start_server.sh")
    else:
        print("⚠️  部分测试失败，请检查配置")

if __name__ == "__main__":
    main() 