export interface BlogPost {
  slug: string
  title: string
  description: string
  date: string
  author: string
  minutes: number
  tag: string
  body: string[]
}

export interface ShowcaseItem {
  name: string
  url: string
  host: string
  category: string
  blurb: string
  from: string
  to: string
}

export interface Partner {
  name: string
  url: string
  tier: '旗舰' | '赞助' | '社区'
  blurb: string
}

export const blogPosts: BlogPost[] = [
  {
    slug: 'v4-3-what-to-use',
    title: 'v4.3 里值得马上用上的变化',
    description: '从更细的阴影刻度到容器查询变体，这一版继续把现代 CSS 收进类名。',
    date: '2026-03-18',
    author: '文档组',
    minutes: 6,
    tag: '发布',
    body: [
      'Tailwind CSS v4 把引擎换成了一次性编译的扫描器，v4.3 则是在这套基础上补齐日常会碰到的 CSS 能力。你不需要记住新的配置文件格式，多数变化都是多了几个可以直接写在标记里的类。',
      '阴影和圆角的刻度更细了。卡片不再只有“有阴影”和“没阴影”两档，输入框、菜单和弹层可以各自使用不同重量。升级后如果某个阴影看起来变轻了，先核对是不是默认刻度变了，而不是构建坏了。',
      '容器查询变体让组件按父级宽度换布局，而不是按浏览器宽度。侧栏里的卡片和主栏里的同一张卡片可以呈现不同列数，这比再堆一层页面级断点更符合组件的复用方式。',
      '颜色继续使用更鲜艳的广色域表达。在支持的屏幕上，500 档会比旧调色板更干净；在普通屏幕上，浏览器会回落到它能显示的范围，你不用写两套颜色。',
      '建议的落地顺序是：先跑升级工具，再看阴影、描边和 ring 宽度这三处默认值，最后把主题从 JavaScript 迁到 @theme。迁完之后，新类名就可以按文档直接用。',
    ],
  },
  {
    slug: 'theme-in-css',
    title: '把主题从配置文件搬进 CSS',
    description: '字族、颜色和断点现在是 CSS 变量。改主题不必再维护一份 JavaScript。',
    date: '2026-01-09',
    author: '文档组',
    minutes: 7,
    tag: '主题',
    body: [
      'v3 的主题住在 tailwind.config.js 里。v4 把它搬进了 CSS 的 @theme。这样做的直接好处是：设计变量和最终样式在同一层，浏览器开发工具里也能看到它们。',
      '命名空间决定会生成什么类。--color-mint-500 同时给出背景、文字和边框类；--font-sans 改变 font-sans；--breakpoint-3xl 则新增一个 3xl: 前缀。行高可以跟在字号后面写成 --text-tiny--line-height。',
      '覆盖默认值时，重写同名变量即可。想删掉一个用不到的刻度，把变量设为 initial。不需要再在配置里写一大段 extend。',
      '颜色建议写成 oklch。它把明度、彩度和色相拆开，调一档更深的颜色时，你改的是明度而不是一串互相牵连的 RGB。广色域屏幕会用到额外的鲜艳度，旧屏幕则自动限制在可显示范围内。',
      '团队协作时，把 @theme 放在入口 CSS 的顶部，设计稿里的色板和代码里的变量就能一一对应。组件里继续只写类名，不要在样式表里再发明一套颜色。',
    ],
  },
  {
    slug: 'dark-mode-contrast',
    title: '深色模式不要只是把颜色反转',
    description: '一套能读的深色界面，靠的是成对的颜色、看得见的边框和保留的焦点环。',
    date: '2025-11-02',
    author: '文档组',
    minutes: 5,
    tag: '界面',
    body: [
      '给每个颜色类加一个 dark: 前缀只是开始。如果浅色正文是 gray-900，深色里把它改成 gray-500，对比度往往不够。正文至少保持在 gray-300 附近，次要说明不要低于 gray-400。',
      '边框在浅色里用 gray-200 很清楚，原样搬到近黑背景上就会消失。深色分隔用 white/10 或 white/15。卡片不要用过低的白色透明度，否则文字会和背后的图案混在一起。',
      '焦点环在两种主题里都要看得见。不要在深色里把 outline 设成和背景接近的颜色。键盘用户不看悬停，只看焦点。',
      '手动切换和系统偏好可以并存。本站用类策略：html 上有 dark 时启用深色变体，选择记在 localStorage，刷新前用一段很小的脚本避免闪烁。',
      '图片和图标也要检查。细线图标如果写死了深色描边，在深色背景上会丢。用 currentColor，让图标跟随文字。',
    ],
  },
  {
    slug: 'container-queries',
    title: '容器查询让组件自己决定布局',
    description: '同一个卡片放进窄侧栏和宽主栏时，应跟着容器走，而不是跟着窗口走。',
    date: '2025-09-16',
    author: '文档组',
    minutes: 6,
    tag: '布局',
    body: [
      '视口断点适合页面骨架：导航何时横过来、主栏何时出现。组件内部的列数如果也绑在 sm:、md: 上，就会在侧栏里被错误地拉成两列。',
      '给父元素加上 @container，子元素就能使用 @sm: 和 @md:。这些前缀比较的是容器宽度。容器变窄时，图片可以回到正方形；容器变宽时，再换成 3/2。',
      '这和实用类的组合方式是一样的：先写最小宽度下的类，再用容器变体覆盖。不要在组件里探测 window.innerWidth。',
      '容器需要一个明确的宽度来源。弹性子项记得加上 min-w-0，否则内容的最小宽度会把容器撑开，查询永远不会触发。',
      '页面级断点和容器查询可以一起用。页面决定“有没有侧栏”，组件决定“我在当前这格里怎么排”。两层职责分开之后，同一套卡片才能放进不同模板。',
    ],
  },
  {
    slug: 'utility-maintenance',
    title: '类名变多，并不等于无法维护',
    description: '重复的标记应该收成组件，而不是收成一层新的 CSS 类名。',
    date: '2025-07-21',
    author: '文档组',
    minutes: 5,
    tag: '实践',
    body: [
      '第一次看到一长串类名时，很容易认为这是在把 CSS 写进 HTML。真正会腐烂的是另一件事：一个只在单页使用的语义类，散落在几千行样式表里，谁也不敢删。',
      '实用类把样式留在使用它的模板旁边。要改这张卡片，就改这张卡片。构建会丢掉没人引用的规则，所以你不会为了“以后可能用到”保留一大包 CSS。',
      '当同一串类在三个地方出现，把它收成一个 Vue 组件，而不是一个 .card 规则。组件有属性、插槽和类型，CSS 类只有选择器。复用的是结构，不是一串碰巧相同的声明。',
      '@apply 适合你无法控制标记的场合，例如第三方库要求你提供一个类。在自己的组件里，把类写在模板上更直接，悬停和断点也不会被藏进另一份文件。',
      '约束来自刻度。间距用 4 的倍数，颜色用调色板，圆角用现成的档。页面看起来统一，是因为可选项本来就不多，而不是因为多写了一份设计规范 PDF。',
    ],
  },
  {
    slug: 'small-css',
    title: '生产环境为什么往往不到 10kB',
    description: '扫描器只把源码里出现过的类写进样式表，其余的刻度不会跟去线上。',
    date: '2025-05-08',
    author: '文档组',
    minutes: 4,
    tag: '构建',
    body: [
      '开发时你感觉整个框架都在，是因为本地服务会按文件变化增量生成。生产构建只保留扫描到的类。一个只用了弹性布局、间距、几档灰和一种强调色的页面，产物可以很小。',
      '这也是动态拼接类名会失效的原因。扫描器不执行脚本，bg-${color}-500 在源码里并不是一个真实类名。把可选值写成完整字符串的映射，既保证生成，也让代码审查看得懂。',
      '任意值类会原样进入产物。top-[117px] 用一次就多一条规则。重复出现的数字应升进 @theme，变成可复用的刻度。',
      '浏览器构建和 CDN 适合演练场，不适合生产。它们要在用户的机器上做编译，也无法像静态文件那样长期缓存。上线前改回 Vite 插件或 CLI。',
      '如果你的 CSS 突然变大，先搜一遍是否把整个图标库的类名拼进了源码，或者是否用 @source 扫进了不该扫的目录。生成列表是闭合的，体积异常一定能在源码里找到原因。',
    ],
  },
]

export const showcase: ShowcaseItem[] = [
  { name: 'OpenAI', host: 'openai.com', url: 'https://openai.com', category: '产品', blurb: '产品站与文档并用实用类搭出大量独立区块。', from: '#10a37f', to: '#0b3d32' },
  { name: 'Opal', host: 'opalcamera.com', url: 'https://opalcamera.com', category: '产品', blurb: '硬件品牌页用大字号、留白和细边框讲产品。', from: '#111827', to: '#4b5563' },
  { name: 'Feastables', host: 'feastables.com', url: 'https://feastables.com', category: '电商', blurb: '食品电商把强烈的色块直接写进组件。', from: '#f59e0b', to: '#b45309' },
  { name: 'Gumroad', host: 'gumroad.com', url: 'https://gumroad.com', category: '产品', blurb: '创作者商店用卡片和清晰的价格排版完成购买路径。', from: '#ff90e8', to: '#7c3aed' },
  { name: 'Skims', host: 'skims.com', url: 'https://skims.com', category: '电商', blurb: '服饰站依赖图片比例、网格和极简文字。', from: '#e5e7eb', to: '#111827' },
  { name: 'Reddit', host: 'reddit.com', url: 'https://reddit.com', category: '社区', blurb: '高密度信息列表靠间距刻度和字号层次撑住可读性。', from: '#ff4500', to: '#7c2d12' },
  { name: 'Rivian', host: 'rivian.com', url: 'https://rivian.com', category: '产品', blurb: '汽车品牌用全屏分节和大幅图片网格。', from: '#14532d', to: '#052e16' },
  { name: 'Shopify', host: 'shopify.com', url: 'https://shopify.com', category: '产品', blurb: '营销页把功能演示做成可交互的区块。', from: '#96bf48', to: '#14532d' },
  { name: 'Clerk', host: 'clerk.com', url: 'https://clerk.com', category: '开发', blurb: '开发者产品用代码窗和浅色卡片解释身份验证。', from: '#6c47ff', to: '#312e81' },
  { name: 'The Verge', host: 'theverge.com', url: 'https://theverge.com', category: '媒体', blurb: '新闻首页用网格而不是一长条文章流。', from: '#5200ff', to: '#1e1b4b' },
  { name: 'Google I/O', host: 'io.google', url: 'https://io.google', category: '活动', blurb: '大会站点用鲜艳渐变和响应式日程表。', from: '#4285f4', to: '#ea4335' },
  { name: 'TED', host: 'ted.com', url: 'https://ted.com', category: '媒体', blurb: '演讲档案用统一卡片承载完全不同的题目。', from: '#e62b1e', to: '#7f1d1d' },
  { name: 'Poolside', host: 'poolside.ai', url: 'https://poolside.ai', category: 'AI', blurb: '深色产品页用细线和单一强调色。', from: '#22d3ee', to: '#0f172a' },
  { name: 'Midjourney', host: 'midjourney.com', url: 'https://midjourney.com', category: 'AI', blurb: '画廊式首页几乎全靠比例和网格。', from: '#111827', to: '#6366f1' },
  { name: 'NASA JPL', host: 'jpl.nasa.gov', url: 'https://www.jpl.nasa.gov', category: '机构', blurb: '任务专题页把复杂信息和大图放进同一套版式。', from: '#1d4ed8', to: '#0f172a' },
]

export const partners: Partner[] = [
  { name: 'Vercel', url: 'https://vercel.com', tier: '旗舰', blurb: '前端部署平台，也是许多 Tailwind 项目的上线方式。' },
  { name: 'Shopify', url: 'https://shopify.com', tier: '旗舰', blurb: '面向商家的商务平台，营销与后台都在使用实用类。' },
  { name: 'Cursor', url: 'https://cursor.com', tier: '旗舰', blurb: '用 AI 编写和修改界面的代码编辑器。' },
  { name: 'Supabase', url: 'https://supabase.com', tier: '赞助', blurb: '开源的 Postgres 后端，常与 Nuxt、Next 一起出现。' },
  { name: 'Clerk', url: 'https://clerk.com', tier: '赞助', blurb: '面向现代应用的用户身份与组织管理。' },
  { name: 'Resend', url: 'https://resend.com', tier: '赞助', blurb: '给开发者用的事务邮件接口。' },
  { name: 'Railway', url: 'https://railway.com', tier: '赞助', blurb: '用来部署数据库和应用的基础设施。' },
  { name: 'Mux', url: 'https://mux.com', tier: '赞助', blurb: '视频上传、转码与播放。' },
  { name: 'Sanity', url: 'https://sanity.io', tier: '社区', blurb: '结构化内容平台。' },
  { name: 'Mintlify', url: 'https://mintlify.com', tier: '社区', blurb: '用来发布产品文档的站点工具。' },
  { name: 'CodeRabbit', url: 'https://coderabbit.ai', tier: '社区', blurb: '拉取请求里的自动代码审查。' },
  { name: 'ImageKit', url: 'https://imagekit.io', tier: '社区', blurb: '图片与视频的优化分发。' },
]

export const plusModules = [
  {
    name: '网站模板',
    summary: '一整页就能跑起来的营销站、文档站和应用壳。',
    points: ['响应式页面骨架', '深色与浅色都已排好', '用实用类写成，方便继续改'],
  },
  {
    name: '界面组件',
    summary: '表单、导航、卡片和营销区块，复制进项目即可调整。',
    points: ['按场景分类', '不绑定运行时框架', '类名可以直接改'],
  },
  {
    name: 'Catalyst',
    summary: '面向 React 的无头风格组件套件，处理焦点、弹层和表单状态。',
    points: ['键盘与焦点行为已处理好', '外观仍由类名决定', '适合产品后台'],
  },
]

export const nav = [
  { label: '文档', to: '/docs' },
  { label: '演练场', to: '/play' },
  { label: '博客', to: '/blog' },
  { label: '案例', to: '/showcase' },
  { label: '合作伙伴', to: '/partners' },
]
