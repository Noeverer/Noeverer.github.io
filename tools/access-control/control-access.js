#!/usr/bin/env node

/**
 * 博客访问控制脚本
 * 用于管理文章的发布权限和访问级别
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// 配置参数
const POSTS_DIR = path.join(__dirname, '../../blog/source/_posts');
const ACCESS_LEVELS = ['public', 'registered', 'premium', 'private'];

// 默认配置
const DEFAULT_ACCESS = {
  published: true,
  access_level: 'public',
  book_chapter: false
};

/**
 * 读取所有文章
 */
function getAllPosts(dir = POSTS_DIR) {
  const posts = [];
  
  function walkDir(currentPath) {
    const items = fs.readdirSync(currentPath);
    
    for (const item of items) {
      const fullPath = path.join(currentPath, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        walkDir(fullPath);
      } else if (item.endsWith('.md')) {
        posts.push(fullPath);
      }
    }
  }
  
  walkDir(dir);
  return posts;
}

/**
 * 更新文章的访问控制信息
 */
function updatePostAccess(postPath, updates) {
  const content = fs.readFileSync(postPath, 'utf8');
  const parsed = matter(content);
  
  // 合并更新
  const newFrontMatter = { ...DEFAULT_ACCESS, ...parsed.data, ...updates };
  
  // 保存更新后的内容
  const updatedContent = matter.stringify(parsed.content, newFrontMatter);
  fs.writeFileSync(postPath, updatedContent);
  
  console.log(`Updated: ${postPath}`);
  console.log(`New front-matter:`, newFrontMatter);
}

/**
 * 检查文章访问权限
 */
function checkAccess(postPath, userLevel = 'public') {
  const content = fs.readFileSync(postPath, 'utf8');
  const parsed = matter(content);
  const accessLevel = parsed.data.access_level || 'public';
  
  const levelIndex = ACCESS_LEVELS.indexOf(accessLevel);
  const userIndex = ACCESS_LEVELS.indexOf(userLevel);
  
  return userIndex >= levelIndex;
}

/**
 * 生成书籍章节列表
 */
function generateBookChapters() {
  const posts = getAllPosts();
  const bookChapters = [];
  
  for (const postPath of posts) {
    const content = fs.readFileSync(postPath, 'utf8');
    const parsed = matter(content);
    
    if (parsed.data.book_chapter) {
      bookChapters.push({
        title: parsed.data.title,
        path: postPath,
        date: parsed.data.date,
        category: parsed.data.categories || 'uncategorized'
      });
    }
  }
  
  // 按日期排序
  bookChapters.sort((a, b) => new Date(b.date) - new Date(a.date));
  
  return bookChapters;
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
博客访问控制工具

用法:
  node control-access.js [options]

选项:
  --help, -h                    显示帮助信息
  --update-access <level>       更新文章访问级别
  --check-access <user-level>   检查用户访问权限
  --generate-book               生成书籍章节列表
  --list-posts                  列出所有文章及访问级别
  --pattern <pattern>          指定文章路径模式

示例:
  node control-access.js --update-access premium --pattern "2026/*"
  node control-access.js --check-access registered --pattern "some-post.md"
  node control-access.js --generate-book
    `);
    return;
  }
  
  if (args.includes('--generate-book')) {
    const chapters = generateBookChapters();
    console.log('书籍章节列表:');
    console.log(JSON.stringify(chapters, null, 2));
    
    // 保存到文件
    fs.writeFileSync('./book-chapters.json', JSON.stringify(chapters, null, 2));
    console.log('书籍章节列表已保存到 book-chapters.json');
  }
  
  if (args.includes('--list-posts')) {
    const posts = getAllPosts();
    console.log('所有文章及访问级别:');
    
    for (const postPath of posts) {
      const content = fs.readFileSync(postPath, 'utf8');
      const parsed = matter(content);
      
      console.log(`${postPath}: ${parsed.data.access_level || 'public'} (published: ${parsed.data.published || true})`);
    }
  }
  
  if (args.includes('--update-access')) {
    const levelIndex = args.indexOf('--update-access');
    const accessLevel = args[levelIndex + 1];
    
    if (!ACCESS_LEVELS.includes(accessLevel)) {
      console.error(`无效的访问级别: ${accessLevel}`);
      console.error(`有效级别: ${ACCESS_LEVELS.join(', ')}`);
      return;
    }
    
    const patternIndex = args.indexOf('--pattern');
    let pattern = '*';
    if (patternIndex !== -1) {
      pattern = args[patternIndex + 1];
    }
    
    const posts = getAllPosts();
    for (const postPath of posts) {
      if (pattern === '*' || postPath.includes(pattern)) {
        updatePostAccess(postPath, { access_level: accessLevel });
      }
    }
  }
}

// 如果此文件被直接运行，则执行主函数
if (require.main === module) {
  main();
}

module.exports = {
  getAllPosts,
  updatePostAccess,
  checkAccess,
  generateBookChapters,
  ACCESS_LEVELS,
  DEFAULT_ACCESS
};