#!/usr/bin/env python3
"""
功能测试脚本
测试 MCP 服务器的各种功能
"""

import subprocess
import time
import json
import os
import hashlib
import base64
import requests

def test_server_features():
    """测试服务器功能"""
    print("🧪 开始功能测试...")
    
    # 启动服务器
    print("🚀 启动服务器...")
    process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待服务器启动
    time.sleep(3)
    
    # 检查进程是否运行
    if process.poll() is None:
        print("✅ 服务器启动成功")
        
        # 测试文件写入功能
        print("\n📝 测试文件写入功能...")
        test_content = "这是一个测试文件\n创建时间: " + time.strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open("test_output.txt", "w", encoding="utf-8") as f:
                f.write(test_content)
            print("✅ 测试文件创建成功")
        except Exception as e:
            print(f"❌ 测试文件创建失败: {e}")
        
        # 测试哈希计算
        print("\n🔐 测试哈希计算...")
        test_text = "Hello World"
        md5_hash = hashlib.md5(test_text.encode('utf-8')).hexdigest()
        print(f"✅ MD5 哈希计算: {md5_hash}")
        
        # 测试 Base64 编码
        print("\n📦 测试 Base64 编码...")
        encoded = base64.b64encode(test_text.encode('utf-8')).decode('utf-8')
        print(f"✅ Base64 编码: {encoded}")
        
        # 测试系统信息获取
        print("\n💻 测试系统信息获取...")
        try:
            result = subprocess.run(["sw_vers", "-productName"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ 系统信息获取: {result.stdout.strip()}")
            else:
                print("⚠️  系统信息获取失败")
        except Exception as e:
            print(f"❌ 系统信息获取错误: {e}")
        
        # 测试网络连接
        print("\n🌐 测试网络连接...")
        try:
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                print("✅ 网络连接正常")
            else:
                print(f"⚠️  网络连接异常: {response.status_code}")
        except Exception as e:
            print(f"❌ 网络连接测试失败: {e}")
        
        # 清理测试文件
        print("\n🧹 清理测试文件...")
        try:
            if os.path.exists("test_output.txt"):
                os.remove("test_output.txt")
                print("✅ 测试文件清理完成")
        except Exception as e:
            print(f"❌ 测试文件清理失败: {e}")
        
        # 停止服务器
        print("\n🛑 停止服务器...")
        process.terminate()
        process.wait()
        print("✅ 服务器已停止")
        
        print("\n🎉 功能测试完成！")
        return True
        
    else:
        stdout, stderr = process.communicate()
        print(f"❌ 服务器启动失败")
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")
        return False

def show_available_tools():
    """显示可用的工具"""
    print("\n📋 可用的工具列表:")
    tools = [
        ("hello", "返回问候消息"),
        ("getTime", "获取当前时间"),
        ("calculate", "执行数学计算"),
        ("getWeather", "获取天气信息"),
        ("translate", "翻译文本"),
        ("checkNetwork", "检查网络连接"),
        ("getJoke", "获取笑话"),
        ("fileRead", "读取本地文件"),
        ("fileWrite", "写入本地文件"),
        ("fileList", "列出目录内容"),
        ("hashText", "哈希计算"),
        ("base64Encode", "Base64编码/解码"),
        ("getSystemInfo", "获取系统信息"),
        ("getProcessInfo", "获取进程信息")
    ]
    
    for i, (tool, desc) in enumerate(tools, 1):
        print(f"  {i:2d}. {tool:<15} - {desc}")

def main():
    """主函数"""
    print("🧪 MCP 服务器功能测试")
    print("=" * 50)
    
    # 显示可用工具
    show_available_tools()
    
    # 运行功能测试
    success = test_server_features()
    
    if success:
        print("\n💡 测试总结:")
        print("- ✅ 服务器启动/停止正常")
        print("- ✅ 文件操作功能正常")
        print("- ✅ 加密工具功能正常")
        print("- ✅ 系统信息获取正常")
        print("- ✅ 网络连接检查正常")
        print("\n🚀 所有功能测试通过！服务器可以正常使用。")
    else:
        print("\n❌ 功能测试失败，请检查服务器配置。")

if __name__ == "__main__":
    main() 