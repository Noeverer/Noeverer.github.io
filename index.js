#!/usr/bin/env node

/**
 * 博客系统主入口点
 * 
 * 该程序用于启动和管理博客系统，包括：
 * - 启动 Hexo 服务器
 * - 处理内容转换
 * - 管理部署流程
 */

const fs = require('fs');
const path = require('path');
const { exec, spawn } = require('child_process');
const express = require('express');

// 检查是否安装了必要的依赖
function checkDependencies() {
  const deps = [
    { name: 'hexo', cmd: 'hexo --version' },
    { name: 'git', cmd: 'git --version' },
    { name: 'node', cmd: 'node --version' }
  ];

  for (const dep of deps) {
    try {
      require('child_process').execSync(dep.cmd, { stdio: 'pipe' });
      console.log(`✓ ${dep.name} 已安装`);
    } catch (e) {
      console.error(`✗ ${dep.name} 未安装`);
      return false;
    }
  }
  return true;
}

// 启动 Hexo 服务器
function startHexoServer(port = 4000) {
  console.log(`正在启动 Hexo 服务器，端口: ${port}`);
  
  const hexoProc = spawn('hexo', ['server', '-p', port.toString()], {
    cwd: path.join(__dirname, 'blog'),
    stdio: 'inherit'
  });

  hexoProc.on('error', (err) => {
    console.error('启动 Hexo 服务器时出错:', err.message);
  });

  hexoProc.on('close', (code) => {
    console.log(`Hexo 服务器已关闭，退出码: ${code}`);
  });

  return hexoProc;
}

// 生成静态文件
function generateStaticFiles() {
  return new Promise((resolve, reject) => {
    console.log('正在生成静态文件...');
    
    const genProc = spawn('hexo', ['generate'], {
      cwd: path.join(__dirname, 'blog'),
      stdio: 'inherit'
    });

    genProc.on('close', (code) => {
      if (code === 0) {
        console.log('静态文件生成完成');
        resolve();
      } else {
        reject(new Error(`生成失败，退出码: ${code}`));
      }
    });
  });
}

// 主程序
async function main() {
  console.log('博客系统启动器');
  console.log('================');
  
  // 检查依赖
  if (!checkDependencies()) {
    console.error('缺少必要依赖，退出...');
    process.exit(1);
  }

  // 解析命令行参数
  const args = process.argv.slice(2);
  
  if (args.includes('--serve') || args.includes('-s')) {
    // 启动服务器
    startHexoServer(args.find(arg => arg.startsWith('--port='))?.split('=')[1] || 4000);
  } else if (args.includes('--generate') || args.includes('-g')) {
    // 生成静态文件
    try {
      await generateStaticFiles();
      console.log('博客已生成到 public 目录');
    } catch (error) {
      console.error('生成失败:', error.message);
      process.exit(1);
    }
  } else if (args.includes('--new') || args.includes('-n')) {
    // 创建新文章
    const title = args[args.indexOf('--new') + 1] || args[args.indexOf('-n') + 1];
    if (!title) {
      console.error('请提供文章标题: node index.js --new "文章标题"');
      process.exit(1);
    }
    
    const newPostProc = spawn('hexo', ['new', title], {
      cwd: path.join(__dirname, 'blog'),
      stdio: 'inherit'
    });
    
    newPostProc.on('close', (code) => {
      if (code === 0) {
        console.log(`文章 "${title}" 已创建`);
      } else {
        console.error(`创建文章失败，退出码: ${code}`);
        process.exit(1);
      }
    });
  } else {
    console.log('用法:');
    console.log('  node index.js --serve [-p <端口>]  启动开发服务器');
    console.log('  node index.js --generate           生成静态文件');
    console.log('  node index.js --new "标题"         创建新文章');
    console.log('');
    console.log('示例:');
    console.log('  node index.js --serve --port=3000  在3000端口启动服务器');
    console.log('  node index.js -s                  启动服务器（默认端口4000）');
    console.log('  node index.js -g                  生成静态文件');
    console.log('  node index.js -n "新文章标题"      创建新文章');
  }
}

// 运行主程序
if (require.main === module) {
  main().catch(err => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = {
  checkDependencies,
  startHexoServer,
  generateStaticFiles
};