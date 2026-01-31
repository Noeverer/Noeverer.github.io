#!/usr/bin/env node

/**
 * 书籍生成器
 * 将标记为 book_chapter 的文章组合成书籍格式
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { generateBookChapters } = require('./control-access');

/**
 * 生成书籍的 HTML 格式
 */
function generateBookHTML(chapters) {
  let html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ante Liu's Blog Book</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .container {
      background-color: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 {
      color: #2c3e50;
      border-bottom: 2px solid #3498db;
      padding-bottom: 10px;
    }
    .chapter {
      margin-bottom: 40px;
      padding-bottom: 20px;
      border-bottom: 1px dashed #eee;
    }
    .chapter:last-child {
      border-bottom: none;
    }
    .chapter-header {
      background-color: #f8f9fa;
      padding: 10px 15px;
      border-left: 4px solid #3498db;
      margin-bottom: 15px;
    }
    .chapter-title {
      margin: 0;
      color: #2c3e50;
    }
    .chapter-meta {
      color: #7f8c8d;
      font-size: 0.9em;
      margin: 5px 0 0 0;
    }
    .toc {
      background-color: #f8f9fa;
      padding: 20px;
      border-radius: 5px;
      margin-bottom: 30px;
    }
    .toc h2 {
      margin-top: 0;
    }
    .toc ul {
      padding-left: 20px;
    }
    .toc li {
      margin-bottom: 8px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Ante Liu's Blog Book</h1>
    
    <div class="toc">
      <h2>目录</h2>
      <ul>
`;

  // 添加目录
  for (let i = 0; i < chapters.length; i++) {
    html += `        <li><a href="#chapter-${i}">${chapters[i].title}</a> <span class="chapter-meta">(${new Date(chapters[i].date).toLocaleDateString('zh-CN')})</span></li>\n`;
  }

  html += `      </ul>
    </div>
`;

  // 添加每个章节
  for (let i = 0; i < chapters.length; i++) {
    const chapter = chapters[i];
    const content = fs.readFileSync(chapter.path, 'utf8');
    const parsed = matter(content);
    
    // 简单的 Markdown 转 HTML（仅基本转换）
    let htmlContent = convertMarkdownToHtml(parsed.content);
    
    html += `    <div class="chapter" id="chapter-${i}">
      <div class="chapter-header">
        <h2 class="chapter-title">${chapter.title}</h2>
        <div class="chapter-meta">发布于 ${new Date(chapter.date).toLocaleDateString('zh-CN')} | 分类: ${chapter.category}</div>
      </div>
      <div class="chapter-content">
        ${htmlContent}
      </div>
    </div>\n`;
  }

  html += `  </div>
</body>
</html>`;

  return html;
}

/**
 * 简单的 Markdown 转 HTML 转换器
 */
function convertMarkdownToHtml(md) {
  let html = md;
  
  // 转换标题
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  
  // 转换粗体
  html = html.replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>');
  
  // 转换斜体
  html = html.replace(/\*(.*)\*/gim, '<em>$1</em>');
  
  // 转换链接
  html = html.replace(/\[(.*)\]\((.*)\)/gim, '<a href="$2">$1</a>');
  
  // 转换行内代码
  html = html.replace(/`(.*?)`/g, '<code>$1</code>');
  
  // 转换段落
  html = html.replace(/^\s*$/gim, '</p><p>');
  html = '<p>' + html + '</p>';
  
  // 替换多余的段落标签
  html = html.replace(/<\/p><p><\/p><p>/g, '</p><p>');
  
  // 转换列表
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)+/gim, '<ul>$&</ul>');
  
  return html;
}

/**
 * 生成书籍
 */
function generateBook() {
  console.log('正在生成书籍...');
  
  const chapters = generateBookChapters();
  
  if (chapters.length === 0) {
    console.log('没有找到标记为书籍章节的文章。请确保文章 front-matter 中包含 "book_chapter: true"');
    return;
  }
  
  console.log(`找到 ${chapters.length} 个章节`);
  
  const bookHtml = generateBookHTML(chapters);
  
  // 确保输出目录存在
  const outputDir = path.join(__dirname, '../../book-output');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // 写入文件
  const outputPath = path.join(outputDir, 'blog-book.html');
  fs.writeFileSync(outputPath, bookHtml);
  
  console.log(`书籍已生成: ${outputPath}`);
  
  // 同时生成一个 JSON 格式的目录
  const tocPath = path.join(outputDir, 'book-toc.json');
  fs.writeFileSync(tocPath, JSON.stringify(chapters, null, 2));
  console.log(`目录已生成: ${tocPath}`);
}

// 如果此文件被直接运行，则生成书籍
if (require.main === module) {
  generateBook();
}

module.exports = {
  generateBook,
  generateBookHTML,
  convertMarkdownToHtml
};