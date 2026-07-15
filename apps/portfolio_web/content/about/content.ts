import type { I18n } from '@/i18n'

type AboutContent = {
  hero: {
    title: string
    description: string
  }
  projects: {
    title: string
    items: {
      cvBase: string
      questionForge: string
      decisionEngine: string
    }
  }
  featuredProjects: {
    title: string
    items: {
      cvBase: { title: string; description: string }
      questionForge: { title: string; description: string }
      decisionEngine: { title: string; description: string }
    }
    viewCv: string
  }
  contact: {
    title: string
    description: string
    button: string
  }
}

export const aboutContent: Record<I18n, AboutContent> = {
  en: {
    hero: {
      title: 'Applied AI Engineer.  Builder.  Snowboarder.',
      description:
        'I spent 10 years designing workflow systems as a Product Manager. Today I build AI systems that turn knowledge into decisions, decisions into actions, and feedback into continuous learning.',
    },
    projects: {
      title: 'Projects',
      items: {
        cvBase: 'CV Base',
        questionForge: 'Question Forge',
        decisionEngine: 'Decision Engine',
      },
    },
    featuredProjects: {
      title: 'Featured Projects',
      items: {
        cvBase: {
          title: 'CV Base',
          description:
            'A compiler-driven portfolio built from structured narratives.',
        },
        questionForge: {
          title: 'Question Forge',
          description:
            'Convert educational documents into structured Question Objects.',
        },
        decisionEngine: {
          title: 'Decision Engine',
          description: 'Policy-driven AI reasoning with transparent decisions.',
        },
      },
      viewCv: 'View CV',
    },
    contact: {
      title: 'Let’s Talk',
      description: "Interested in working together? Let's Talk",
      button: 'Connect on WeChat',
    },
  },

  zh: {
    hero: {
      title: 'AI 应用工程师, 产品构建者, 滑雪爱好者。',
      description:
        '过去十年，专注于产品与工作流系统设计。如今，我构建 AI 系统，将知识转化为决策，将决策转化为行动，并通过反馈持续学习和演进。',
    },
    projects: {
      title: '项目',
      items: {
        cvBase: 'CV Base',
        questionForge: 'Question Forge',
        decisionEngine: 'Decision Engine',
      },
    },
    featuredProjects: {
      title: '精选项目',
      items: {
        cvBase: {
          title: 'CV Base',
          description: '基于结构化叙事构建的编译器驱动型作品集。',
        },
        questionForge: {
          title: 'Question Forge',
          description: '将教育文档转化为结构化的问题对象。',
        },
        decisionEngine: {
          title: 'Decision Engine',
          description: '通过政策驱动的 AI 推理，生成透明的决策。',
        },
      },
      viewCv: '查看简历',
    },
    contact: {
      title: '聊聊吧',
      description: '感兴趣一起共事吗？聊聊吧',
      button: '微信联系',
    },
  },
}
