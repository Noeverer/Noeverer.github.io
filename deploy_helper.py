#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署辅助脚本 - 简化部署流程
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DeployHelper:
    """部署辅助工具"""

    def __init__(self):
        self.base_dir = Path.cwd()

    def run_command(self, command: str, check: bool = True) -> bool:
        """执行shell命令"""
        logger.info(f"执行命令: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=check,
                capture_output=True,
                text=True
            )
            if result.stdout:
                logger.info(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"命令执行失败: {e}")
            if e.stderr:
                logger.error(e.stderr)
            return False

    def install_python_deps(self):
        """安装Python依赖"""
        logger.info("安装Python依赖...")
        return self.run_command("pip3 install beautifulsoup4 GitPython")

    def install_hexo_deps(self):
        """安装Hexo依赖"""
        logger.info("安装Hexo依赖...")
        success = self.run_command("npm install -g hexo-cli")
        if success:
            return self.run_command("npm install")
        return False

    def run_conversion(self):
        """运行HTML转换"""
        logger.info("运行HTML转换...")
        return self.run_command("python3 html2hexo.py")

    def build_site(self):
        """构建Hexo站点"""
        logger.info("构建Hexo站点...")
        self.run_command("hexo clean")
        return self.run_command("hexo generate")

    def start_local_server(self, port: int = 4000):
        """启动本地服务器"""
        logger.info(f"启动本地服务器，端口: {port}")
        logger.info("访问 http://localhost:4000")
        logger.info("按 Ctrl+C 停止服务器")
        self.run_command(f"hexo server -p {port}", check=False)

    def create_post(self, title: str):
        """创建新文章"""
        logger.info(f"创建新文章: {title}")
        return self.run_command(f"hexo new '{title}'")

    def init_hexo(self):
        """初始化Hexo"""
        logger.info("初始化Hexo...")
        if (self.base_dir / '_config.yml').exists():
            logger.info("Hexo已初始化")
            return True
        return self.run_command("hexo init . --force")

    def deploy_github_pages(self):
        """部署到GitHub Pages"""
        logger.info("部署到GitHub Pages...")
        return self.run_command("hexo deploy")

    def show_status(self):
        """显示状态"""
        logger.info("Hexo状态信息")
        logger.info("=" * 50)

        # 检查文件
        files = {
            '_config.yml': 'Hexo配置',
            'package.json': 'npm配置',
            'html2hexo.py': '转换脚本',
            '.github/workflows/hexo-deploy.yml': 'GitHub Actions'
        }

        for file, desc in files.items():
            status = "✓" if (self.base_dir / file).exists() else "✗"
            logger.info(f"{status} {desc} ({file})")

        # 检查目录
        dirs = {
            'source/_posts': '文章目录',
            'public': '构建输出',
            'node_modules': '依赖包'
        }

        for dir, desc in dirs.items():
            status = "✓" if (self.base_dir / dir).exists() else "✗"
            logger.info(f"{status} {desc} ({dir})")

    def full_setup(self):
        """完整设置流程"""
        logger.info("=" * 50)
        logger.info("开始完整设置")
        logger.info("=" * 50)

        steps = [
            ("安装Python依赖", self.install_python_deps),
            ("安装Hexo依赖", self.install_hexo_deps),
            ("运行HTML转换", self.run_conversion),
            ("构建Hexo站点", self.build_site)
        ]

        failed_steps = []
        for step_name, step_func in steps:
            logger.info(f"\n执行步骤: {step_name}")
            if not step_func():
                failed_steps.append(step_name)
                logger.error(f"步骤失败: {step_name}")
            else:
                logger.info(f"步骤完成: {step_name}")

        logger.info("\n" + "=" * 50)
        if failed_steps:
            logger.error(f"设置完成，但以下步骤失败: {', '.join(failed_steps)}")
            return False
        else:
            logger.info("✅ 所有设置步骤完成！")
            return True


def main():
    parser = argparse.ArgumentParser(description='Hexo部署辅助工具')
    parser.add_argument('command', choices=[
        'setup', 'convert', 'build', 'serve', 'deploy',
        'new', 'status', 'init', 'full'
    ], help='要执行的命令')

    parser.add_argument('--title', type=str, help='文章标题（用于new命令）')
    parser.add_argument('--port', type=int, default=4000, help='服务器端口（用于serve命令）')

    args = parser.parse_args()

    helper = DeployHelper()

    commands = {
        'setup': lambda: helper.full_setup(),
        'convert': helper.run_conversion,
        'build': helper.build_site,
        'serve': lambda: helper.start_local_server(args.port),
        'deploy': helper.deploy_github_pages,
        'new': lambda: helper.create_post(args.title) if args.title else logger.error("需要指定--title"),
        'status': helper.show_status,
        'init': helper.init_hexo,
        'full': lambda: helper.full_setup()
    }

    result = commands[args.command]()
    sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()
