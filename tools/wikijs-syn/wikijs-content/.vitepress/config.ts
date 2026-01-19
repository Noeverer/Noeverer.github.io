import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Ante's Wiki",
  description: '个人知识库文档',
  lang: 'zh-CN',

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '编程', link: '/programming/' },
      { text: '学习', link: '/study/' },
      { text: '生活', link: '/life/' },
      {
        text: 'GitHub',
        items: [
          {
            text: 'Wiki.js 内容仓库',
            link: 'https://github.com/Noeverer/wikijs-content'
          },
          {
            text: 'Noeverer.github.io',
            link: 'https://github.com/Noeverer/Noeverer.github.io'
          }
        ]
      }
    ],

    sidebar: {
      '/programming/': [
        {
          text: '编程',
          items: [
            { text: 'Python', link: '/programming/python.md' },
            { text: 'Docker', link: '/programming/docker.md' },
            { text: 'LeetCode', link: '/programming/leetcode.md' }
          ]
        }
      ],
      '/study/': [
        {
          text: '学习',
          items: [
            { text: '学习笔记', link: '/study/notes.md' },
            { text: '思维导图', link: '/study/mindmap.md' }
          ]
        }
      ],
      '/life/': [
        {
          text: '生活',
          items: [
            { text: '感悟', link: '/life/reflections.md' }
          ]
        }
      ]
    },

    search: {
      provider: 'local'
    },

    footer: {
      message: '基于 Wiki.js 和 VitePress 构建',
      copyright: 'Copyright © 2026 Ante Liu'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Noeverer' }
    ]
  }
})
