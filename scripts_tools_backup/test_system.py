#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统测试脚本 - 验证所有组件是否正常工作
"""

import sys
import os
from pathlib import Path
import subprocess


def run_command(cmd):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "命令超时"
    except Exception as e:
        return False, "", str(e)


def test_python_version():
    """测试Python版本"""
    print("测试 Python 版本...")
    success, stdout, stderr = run_command("python3 --version")
    if success:
        print(f"  ✓ {stdout.strip()}")
        return True
    else:
        print(f"  ✗ 失败: {stderr}")
        return False


def test_python_deps():
    """测试Python依赖"""
    print("\n测试 Python 依赖...")
    deps = ['bs4', 'git']
    all_ok = True

    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} 未安装")
            all_ok = False

    return all_ok


def test_node_version():
    """测试Node.js版本"""
    print("\n测试 Node.js 版本...")
    success, stdout, stderr = run_command("node --version")
    if success:
        print(f"  ✓ {stdout.strip()}")
        return True
    else:
        print(f"  ✗ 失败: {stderr}")
        return False


def test_npm_version():
    """测试npm版本"""
    print("\n测试 npm 版本...")
    success, stdout, stderr = run_command("npm --version")
    if success:
        print(f"  ✓ {stdout.strip()}")
        return True
    else:
        print(f"  ✗ 失败: {stderr}")
        return False


def test_hexo_cli():
    """测试Hexo CLI"""
    print("\n测试 Hexo CLI...")
    success, stdout, stderr = run_command("hexo version")
    if success:
        print("  ✓ Hexo CLI 已安装")
        return True
    else:
        print(f"  ✗ Hexo CLI 未安装")
        return False


def test_git_version():
    """测试Git版本"""
    print("\n测试 Git 版本...")
    success, stdout, stderr = run_command("git --version")
    if success:
        print(f"  ✓ {stdout.strip()}")
        return True
    else:
        print(f"  ✗ 失败: {stderr}")
        return False


def test_project_structure():
    """测试项目结构"""
    print("\n测试项目结构...")
    required_files = [
        'html2hexo.py',
        'deploy_helper.py',
        '.github/workflows/hexo-deploy.yml'
    ]

    required_dirs = [
        'source/_posts',
        'themes'
    ]

    all_ok = True

    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} 不存在")
            all_ok = False

    for dir in required_dirs:
        if Path(dir).exists():
            print(f"  ✓ {dir}/")
        else:
            print(f"  ✗ {dir}/ 不存在")
            all_ok = False

    return all_ok


def test_converter_import():
    """测试转换器导入"""
    print("\n测试转换器导入...")
    try:
        sys.path.insert(0, str(Path.cwd()))
        import html2hexo
        print("  ✓ 转换器模块导入成功")
        return True
    except Exception as e:
        print(f"  ✗ 导入失败: {e}")
        return False


def test_main_components():
    """测试主要组件"""
    print("\n测试主要组件...")

    try:
        sys.path.insert(0, str(Path.cwd()))
        from html2hexo import (
            MarkdownConverter,
            ThemeRecommender,
            GitBranchManager,
            GitHubActionsGenerator,
            HTML2HexoController
        )
        print("  ✓ MarkdownConverter")
        print("  ✓ ThemeRecommender")
        print("  ✓ GitBranchManager")
        print("  ✓ GitHubActionsGenerator")
        print("  ✓ HTML2HexoController")
        return True
    except Exception as e:
        print(f"  ✗ 组件导入失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("HTML to Hexo 系统测试")
    print("=" * 60)

    tests = [
        ("Python版本", test_python_version),
        ("Python依赖", test_python_deps),
        ("Node.js版本", test_node_version),
        ("npm版本", test_npm_version),
        ("Hexo CLI", test_hexo_cli),
        ("Git版本", test_git_version),
        ("项目结构", test_project_structure),
        ("转换器导入", test_converter_import),
        ("主要组件", test_main_components)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ✗ 测试异常: {e}")
            results.append((name, False))

    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status:10} {name}")

    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 通过")

    if passed == total:
        print("\n✅ 所有测试通过！系统已准备就绪。")
        print("\n下一步:")
        print("  1. 运行转换: python3 html2hexo.py")
        print("  2. 启动服务器: python3 deploy_helper.py serve")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查上述错误。")
        print("\n建议运行安装脚本:")
        print("  bash install.sh")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
