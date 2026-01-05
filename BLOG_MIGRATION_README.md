# 博客迁移与分支管理项目

## 项目概述

本项目实现了将HTML格式的博客文章转换为Markdown格式，并根据内容类型分发到不同分支进行管理的功能。

## 功能说明

### 1. HTML到Markdown转换
- 使用BeautifulSoup解析HTML文件
- 提取文章标题、内容、日期、标签等信息
- 生成包含Front Matter的Markdown文件
- 保留原始内容的结构和格式

### 2. 分支管理
- **personal分支**：个人生活感悟类文章（chocolate, life, love等分类）
- **tech分支**：技术文章（leetcode, code, python, mindmap等分类）
- **work分支**：工作相关记录（work, problem等分类）

### 3. 选择性发布
- 支持排除特定模式的文件（如简历等）
- 每个分支可配置不同的主题
- 支持灵活的分类和标签匹配规则

## 目录结构

```
/workspace/
├── source/_posts/                 # 原始转换后的所有Markdown文件
├── distributed/                   # 分发后的分支目录
│   ├── personal/                  # 个人生活分支
│   │   ├── _config.yml           # 个人分支配置（使用landscape主题）
│   │   ├── package.json          # 依赖配置
│   │   └── source/_posts/        # 个人文章
│   ├── tech/                      # 技术博客分支
│   │   ├── _config.yml           # 技术分支配置（使用next主题）
│   │   ├── package.json          # 依赖配置
│   │   └── source/_posts/        # 技术文章
│   └── work/                      # 工作记录分支
│       ├── _config.yml           # 工作分支配置（使用yilia主题）
│       ├── package.json          # 依赖配置
│       └── source/_posts/        # 工作相关文章
├── publish_config.json           # 分支配置文件
├── convert_html_to_md.py         # HTML到Markdown转换脚本
├── convert_html_to_md_enhanced.py # 增强版转换脚本
└── distribute_posts.py           # 文章分发脚本
```

## 配置说明

### publish_config.json
```json
{
  "branches": {
    "personal": {
      "name": "个人生活",
      "description": "个人生活感悟和思考",
      "categories": ["chocolate", "life", "love"],
      "tags": ["life", "感悟", "chocolate"]
    },
    "tech": {
      "name": "技术博客",
      "description": "技术文章和代码相关",
      "categories": ["leetcode", "code", "python", "mindmap"],
      "tags": ["tech", "code", "algorithm"]
    },
    "work": {
      "name": "工作记录",
      "description": "工作相关记录和总结",
      "categories": ["work", "problem"],
      "tags": ["work", "problem"]
    }
  },
  "exclude_patterns": [
    "jia*",           // 排除包含"jia"的文件（如简历）
    "*简历*",
    "*resume*",
    "*cover*"
  ],
  "theme": {
    "default": "next",
    "branches": {
      "personal": "landscape",
      "tech": "next",
      "work": "yilia"
    }
  }
}
```

## 使用方法

### 1. 添加新文章
将新的HTML文件放入相应目录，然后运行：
```bash
python convert_html_to_md_enhanced.py
python distribute_posts.py
```

### 2. 部署到GitHub Pages
每个分支都有独立的Hexo配置，可独立部署：

```bash
# 进入对应分支目录
cd distributed/personal
npm install
hexo generate
hexo deploy

# 或者对tech分支
cd ../tech
npm install
hexo generate
hexo deploy
```

### 3. 自定义配置
修改`publish_config.json`文件来调整：
- 分类规则
- 排除模式
- 主题设置
- 分支名称和描述

## 主题选择建议

- **NexT**: 功能丰富，适合技术博客
- **Landscape**: 简洁经典，适合个人生活类
- **Yilia**: 简约现代，适合工作记录类

## 维护说明

1. 所有原始HTML文件已转换为Markdown格式
2. 文章已按类型分发到对应分支
3. 每个分支都有独立的Hexo环境配置
4. 可以根据需要调整分类规则和主题配置