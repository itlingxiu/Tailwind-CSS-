# -*- coding: utf-8 -*-
"""Generate Chinese Tailwind CSS documentation data."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "data" / "docs.json"
SAFELIST = ROOT / "app" / "data" / "safelist.html"

pages = {}
groups = []
classes = set()


def add_group(title, items):
    groups.append({"title": title, "items": items})


def page(slug, title, summary, group, sections, demo="", preview="text"):
    pages[slug] = {
        "slug": slug,
        "title": title,
        "summary": summary,
        "group": group,
        "demo": demo,
        "preview": preview,
        "sections": sections,
    }
    for section in sections:
        for row in section.get("rows") or []:
            for token in str(row.get("class", "")).split():
                if token and not token.startswith("("):
                    classes.add(token)
    if demo:
        for token in demo.split():
            classes.add(token)


def p(text):
    return {"type": "p", "text": text}


def h2(text):
    return {"type": "h2", "text": text}


def h3(text):
    return {"type": "h3", "text": text}


def code(lang, body):
    return {"type": "code", "lang": lang, "code": body.strip("\n")}


def table(rows, headers=None):
    data = {"type": "table", "rows": [{"class": a, "css": b, "note": c} for a, b, c in rows]}
    if headers:
        data["headers"] = list(headers)
    return data


def tip(text):
    return {"type": "tip", "text": text}


def util(slug, title, summary, group, prop, rows, extra=None, preview="box", demo=""):
    sections = [
        p(summary),
        h2("常用类"),
        p(f"这些类直接对应 CSS 属性 {prop}。把类写在元素上即可，构建时只会生成你用到的规则。"),
        table(rows),
    ]
    if extra:
        sections.extend(extra)
    sections.append(tip("类名必须完整出现在源码里。不要用字符串拼接动态拼出类名，否则扫描器找不到它们。"))
    page(slug, title, summary, group, sections, demo or (rows[1][0] if len(rows) > 1 else rows[0][0]), preview)


# ---------- 开始使用 ----------
G = "开始使用"
add_group(G, [
    {"title": "安装", "slug": "installation"},
    {"title": "使用 Vite", "slug": "installation/using-vite"},
    {"title": "使用 PostCSS", "slug": "installation/using-postcss"},
    {"title": "Tailwind CLI", "slug": "installation/tailwind-cli"},
    {"title": "框架指南", "slug": "installation/framework-guides"},
    {"title": "Play CDN", "slug": "installation/play-cdn"},
    {"title": "编辑器配置", "slug": "editor-setup"},
    {"title": "兼容性", "slug": "compatibility"},
    {"title": "升级指南", "slug": "upgrade-guide"},
])

page("installation", "安装 Tailwind CSS", "Tailwind 会扫描模板里的类名，生成对应样式，并写成一份静态 CSS。它很快、很灵活，而且没有运行时。", G, [
    p("推荐优先使用 Vite 插件。Nuxt、Laravel、SvelteKit、React Router 和 SolidStart 都可以走这条路径。如果你的工具链基于 PostCSS，也可以使用 PostCSS 插件；没有构建工具时，再用 CLI 或浏览器 CDN。"),
    h2("选择一种方式"),
    table([
        ("Vite 插件", "@tailwindcss/vite", "和 Nuxt、Vite 项目最省事"),
        ("PostCSS 插件", "@tailwindcss/postcss", "适合已有 PostCSS 流水线"),
        ("Tailwind CLI", "@tailwindcss/cli", "不依赖前端框架"),
        ("浏览器 CDN", "@tailwindcss/browser", "只适合原型，不要用于生产"),
    ], ("方式", "包名", "说明")),
    tip("生产环境请使用构建工具。CDN 会在浏览器里编译，体积和缓存都不如静态 CSS。"),
])

page("installation/using-vite", "使用 Vite 安装", "把 Tailwind 作为 Vite 插件接入，是目前最顺畅的安装方式。", G, [
    h2("创建项目"),
    p("如果还没有项目，可以用 Create Vite 新建一个。已有 Nuxt 项目则跳过这一步。"),
    code("bash", "npm create vite@latest my-app\ncd my-app\nnpm install"),
    h2("安装依赖"),
    code("bash", "npm install tailwindcss @tailwindcss/vite"),
    h2("配置 Vite 插件"),
    code("ts", """import { defineConfig } from "vite"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  plugins: [tailwindcss()],
})"""),
    h2("引入样式"),
    p("在入口 CSS 里导入 Tailwind。不需要再写三条 @tailwind 指令。"),
    code("css", '@import "tailwindcss";'),
    h2("在 HTML 里使用"),
    code("html", """<h1 class="text-3xl font-bold tracking-tight text-gray-950">
  你好，Tailwind
</h1>"""),
    tip("Nuxt 项目把 CSS 放到 nuxt.config 的 css 数组，并把插件加进 vite.plugins。本站就是这样接上的。"),
], demo="text-3xl font-bold tracking-tight text-sky-600", preview="text")

page("installation/using-postcss", "使用 PostCSS 安装", "已有 PostCSS 流水线时，安装 PostCSS 插件即可。", G, [
    h2("安装"),
    code("bash", "npm install tailwindcss @tailwindcss/postcss postcss"),
    h2("配置 PostCSS"),
    code("js", """export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
}"""),
    h2("引入样式"),
    code("css", '@import "tailwindcss";'),
    p("然后照常启动你的开发服务器。保存模板文件时，只有用到的类会被写进产物。"),
])

page("installation/tailwind-cli", "使用 Tailwind CLI", "没有 Vite 或 PostCSS 时，可以用独立命令行编译 CSS。", G, [
    h2("安装"),
    code("bash", "npm install tailwindcss @tailwindcss/cli"),
    h2("编译"),
    code("bash", 'npx @tailwindcss/cli -i ./src/input.css -o ./dist/output.css --watch'),
    p("input.css 里只需要一行 @import \"tailwindcss\";。把生成的 output.css 链接到 HTML 即可。"),
    code("html", '<link rel="stylesheet" href="/dist/output.css" />'),
])

page("installation/framework-guides", "框架指南", "主流框架都可以在几分钟内接上 Tailwind CSS v4。", G, [
    h2("Nuxt"),
    p("安装 tailwindcss 和 @tailwindcss/vite，在 nuxt.config.ts 里注册 Vite 插件，再把入口 CSS 加进 css 选项。"),
    code("ts", """import tailwindcss from "@tailwindcss/vite"

export default defineNuxtConfig({
  css: ["~/assets/css/main.css"],
  vite: { plugins: [tailwindcss()] },
})"""),
    code("css", '@import "tailwindcss";'),
    h2("Next.js"),
    p("Next.js 使用 PostCSS。安装 tailwindcss 与 @tailwindcss/postcss，并在 postcss.config.mjs 中启用插件。"),
    h2("Laravel"),
    p("Laravel 自带 Vite。安装 Vite 插件后，在 resources/css/app.css 导入 Tailwind，并在 vite.config 里注册插件。"),
    h2("SvelteKit / React Router / SolidStart"),
    p("这些框架都基于 Vite，步骤与 Vite 安装一致：安装插件、注册插件、导入 CSS。"),
    tip("不要同时安装 v3 的 tailwind.config.js 自动补全和 v4 插件，除非你正在按升级指南迁移。"),
])

page("installation/play-cdn", "Play CDN", "浏览器里直接编译 Tailwind，适合试想法，不适合上线。", G, [
    p("在页面里引入浏览器构建，然后照常写类名。脚本会在运行时扫描 DOM。"),
    code("html", """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  </head>
  <body>
    <h1 class="text-3xl font-semibold">浏览器里的 Tailwind</h1>
  </body>
</html>"""),
    tip("本站的演练场页面使用的就是这套浏览器构建，方便你立刻看到类名效果。"),
], demo="text-3xl font-semibold", preview="text")

page("editor-setup", "编辑器配置", "装上智能提示之后，类名、变体和主题变量都可以自动补全。", G, [
    h2("Visual Studio Code"),
    p("安装官方扩展 Tailwind CSS IntelliSense。它能补全类名、预览颜色，并在悬停时显示生成的 CSS。"),
    h2("Prettier"),
    p("安装 prettier-plugin-tailwindcss，保存时会按推荐顺序整理类名，团队协作时 diff 会干净很多。"),
    h2("其他编辑器"),
    p("JetBrains IDE 可通过 Tailwind CSS 插件获得类似补全。Neovim 可以接入 Tailwind CSS 语言服务器。"),
    tip("v4 的主题写在 CSS 的 @theme 里。把语言服务指向包含 @import \"tailwindcss\" 的入口文件，补全才完整。"),
])

page("compatibility", "兼容性", "Tailwind CSS v4 面向现代浏览器，并使用多层 CSS 特性。", G, [
    p("v4 默认使用原生级联层、注册自定义属性、oklch 颜色和现代选择器。Safari、Chrome、Firefox 和 Edge 的当前版本都支持。"),
    h2("需要旧浏览器时"),
    p("如果必须兼容较老的浏览器，可以额外安装兼容包，并在入口 CSS 里导入它。这会增加一些产物体积。"),
    code("bash", "npm install @tailwindcss/compat"),
    h2("和 CSS 预处理器"),
    p("不建议再套一层 Sass 或 Less 来处理 Tailwind 入口文件。主题、嵌套和函数已经由 Tailwind 自己处理。普通 CSS 模块可以继续用。"),
    tip("容器查询、:has()、色域相关颜色都依赖较新的浏览器。演示页里的效果在旧浏览器上会降级。"),
])

page("upgrade-guide", "从 v3 升级到 v4", "v4 把配置从 JavaScript 移到了 CSS，安装方式和部分默认值也有变化。", G, [
    p("可以先用官方升级工具扫一遍项目，再手动核对下面这些行为差异。"),
    code("bash", "npx @tailwindcss/upgrade"),
    h2("入口文件"),
    p("删掉 @tailwind base、@tailwind components 和 @tailwind utilities，改成一行导入。"),
    code("css", '@import "tailwindcss";'),
    h2("主题配置"),
    p("tailwind.config.js 里的 theme.extend 迁到 @theme。颜色、字体、字号和断点都变成 CSS 变量。"),
    code("css", """@import "tailwindcss";

@theme {
  --font-sans: "Inter", sans-serif;
  --color-brand: oklch(0.65 0.15 230);
  --breakpoint-3xl: 120rem;
}"""),
    h2("默认值变化"),
    table([
        ("ring", "宽度默认变为 1px", "原来的粗描边请改用 ring-3"),
        ("shadow-sm", "阴影更轻", "需要旧效果时用更大的阴影档"),
        ("outline-none", "不再等价于清除轮廓", "旧写法改为 outline-hidden"),
        ("rounded-sm", "圆角刻度调整", "更小的一档是 rounded-xs"),
    ]),
    h2("内容检测"),
    p("content 数组不再是主要配置方式。v4 会自动扫描项目文件。忽略目录或额外源文件时，使用 @source。"),
    tip("动态拼接的类名在 v3 和 v4 都不会被检测到。请写完整类名，或把可选类名列成静态映射。"),
])

# ---------- 核心概念 ----------
G = "核心概念"
add_group(G, [
    {"title": "用实用类写样式", "slug": "styling-with-utility-classes"},
    {"title": "悬停、焦点和其他状态", "slug": "hover-focus-and-other-states"},
    {"title": "响应式设计", "slug": "responsive-design"},
    {"title": "深色模式", "slug": "dark-mode"},
    {"title": "主题变量", "slug": "theme"},
    {"title": "颜色", "slug": "colors"},
    {"title": "添加自定义样式", "slug": "adding-custom-styles"},
    {"title": "在源文件中检测类名", "slug": "detecting-classes-in-source-files"},
    {"title": "函数与指令", "slug": "functions-and-directives"},
])

page("styling-with-utility-classes", "用实用类写样式", "实用类是单一用途的小类。把它们组合在元素上，就能描述完整的设计，而不必先发明一套组件类名。", G, [
    p("传统写法是给元素起一个语义类，再去 CSS 文件里写规则。实用类把这个过程倒过来：样式就在标记旁边，改一处就能看到结果。"),
    h2("一个按钮"),
    code("html", """<button class="rounded-full bg-sky-500 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-400">
  开始使用
</button>"""),
    p("每个类只做一件事：圆角、背景、内边距、字号、字重、文字颜色和悬停背景。读标记就能读懂设计。"),
    h2("为什么这样更快"),
    table([
        ("不用起名", "不必为每个区块想类名", "减少设计系统之外的一次性命名"),
        ("不用切换文件", "HTML 和样式在一起", "改完即可在浏览器里核对"),
        ("约束即设计", "间距、颜色来自刻度", "页面不容易出现随意的像素值"),
        ("产物很小", "未使用的类不会输出", "多数项目的 CSS 小于 10kB"),
    ]),
    tip("重复出现的类组合可以抽成 Vue 组件，而不是过早抽成 CSS 组件类。标记复用通常比 @apply 更清晰。"),
], demo="rounded-full bg-sky-500 px-4 py-2 text-sm font-semibold text-white", preview="text")

page("hover-focus-and-other-states", "悬停、焦点和其他状态", "把状态写成前缀，挂到任意实用类前面。", G, [
    p("变体位于类名左侧，用冒号分隔。hover: 表示悬停，focus: 表示聚焦，disabled: 表示禁用。它们可以和响应式、深色模式叠在一起。"),
    h2("常见状态"),
    table([
        ("hover:bg-sky-400", ":hover", "指针悬停"),
        ("focus:outline-none", ":focus", "元素获得焦点"),
        ("focus-visible:outline-2", ":focus-visible", "键盘焦点，推荐用于可见焦点环"),
        ("active:scale-95", ":active", "按下瞬间"),
        ("disabled:opacity-50", ":disabled", "禁用"),
        ("aria-expanded:rotate-180", "[aria-expanded=true]", "按 ARIA 状态"),
        ("data-open:block", "[data-open]", "按 data 属性"),
    ]),
    code("html", """<button class="rounded-lg bg-gray-900 px-3 py-2 text-white transition hover:bg-gray-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 disabled:cursor-not-allowed disabled:opacity-50">
  保存
</button>"""),
    h2("分组与同伴"),
    p("父元素加上 group，子元素就能用 group-hover: 响应父级悬停。相邻元素可以用 peer 和 peer-focus:。"),
    tip("所有可点击元素都应该有悬停反馈和可见的键盘焦点。颜色变化用 150 到 300 毫秒的过渡就够了。"),
], demo="rounded-lg bg-gray-900 px-3 py-2 text-sm font-medium text-white", preview="text")

page("responsive-design", "响应式设计", "在任意实用类前加上断点前缀，就能只在该宽度及以上生效。", G, [
    p("Tailwind 是移动优先的。不带前缀的类在所有宽度生效，sm: 从 40rem 起生效，更大的断点会覆盖它。"),
    h2("默认断点"),
    table([
        ("（无前缀）", "0px", "默认，先写手机样式"),
        ("sm:", "40rem", "小屏平板"),
        ("md:", "48rem", "平板"),
        ("lg:", "64rem", "笔记本"),
        ("xl:", "80rem", "桌面"),
        ("2xl:", "96rem", "大桌面"),
    ]),
    code("html", """<img class="aspect-square w-full object-cover sm:aspect-video lg:aspect-3/2" alt="湖边小屋" />
<div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
  <!-- 卡片 -->
</div>"""),
    h2("自定义断点"),
    code("css", """@theme {
  --breakpoint-3xl: 120rem;
}"""),
    p("之后就可以使用 3xl:flex 这样的类。容器查询则使用 @sm: 这一类前缀，依据的是父容器而不是视口。"),
    tip("先在窄屏上排好内容，再逐级增强。不要用 max-sm: 把桌面样式硬压回手机，除非确有必要。"),
], demo="grid grid-cols-2 gap-3", preview="grid")

page("dark-mode", "深色模式", "在颜色类前加上 dark:，即可为深色主题准备另一套颜色。", G, [
    p("v4 默认跟随 CSS 的 prefers-color-scheme。如果要做手动切换，把深色变体改成类选择器，并在 html 上切换 dark 类。本站使用的就是这种方式。"),
    h2("类策略"),
    code("css", '@custom-variant dark (&:where(.dark, .dark *));'),
    code("html", """<div class="bg-white text-gray-950 dark:bg-gray-950 dark:text-white">
  <p class="text-gray-600 dark:text-gray-300">正文需要足够对比度。</p>
</div>"""),
    h2("对比度"),
    p("浅色正文不要低于 slate-600，深色正文不要用过暗的灰色贴在近黑背景上。边框在浅色用 gray-200，在深色用 white/10，两侧都要看得见。"),
    tip("系统、浅色、深色三种选择应被记住。页脚的主题开关会把选择写入 localStorage。"),
], demo="rounded-xl bg-white px-4 py-3 text-gray-950 shadow-sm dark:bg-gray-900 dark:text-white", preview="box")

page("theme", "主题变量", "定制主题就是声明几条 CSS 变量。命名空间决定它会生成哪些实用类。", G, [
    p("在 @theme 里新增变量后，Tailwind 会生成对应的类和底层自定义属性。例如 --color-mint-500 会带来 bg-mint-500、text-mint-500 和 border-mint-500。"),
    code("css", """@import "tailwindcss";

@theme {
  --font-sans: "Inter", sans-serif;
  --font-mono: "IBM Plex Mono", monospace;
  --text-tiny: 0.625rem;
  --text-tiny--line-height: 1rem;
  --color-mint-500: oklch(0.7 0.18 145);
  --color-mint-700: oklch(0.5 0.14 145);
}"""),
    h2("常用命名空间"),
    table([
        ("--color-*", "bg / text / border", "颜色"),
        ("--font-*", "font-*", "字族"),
        ("--text-*", "text-*", "字号"),
        ("--breakpoint-*", "sm: / md:", "断点"),
        ("--spacing", "p-* / m-* / w-*", "间距基数"),
        ("--radius-*", "rounded-*", "圆角"),
        ("--shadow-*", "shadow-*", "阴影"),
    ]),
    p("覆盖默认值时直接重写同名变量。移除某个默认刻度可以把变量设为 initial。"),
    tip("颜色推荐使用 oklch，这样在广色域屏幕上更鲜艳，在普通屏幕上也能正常回落。"),
])

page("colors", "颜色", "默认调色板覆盖常用色相，每一档从 50 到 950，并用更鲜艳的广色域颜色。", G, [
    p("实用类把颜色分成背景、文字、边框、轮廓、阴影和装饰线。同一档颜色可以复用在这些属性上。"),
    h2("用法"),
    table([
        ("bg-sky-500", "background-color", "填充"),
        ("text-sky-700", "color", "文字"),
        ("border-sky-200", "border-color", "边框"),
        ("ring-sky-500", "--tw-ring-color", "焦点环"),
        ("from-sky-400", "渐变色标", "配合 bg-gradient-to-r"),
        ("bg-black/50", "带透明度", "斜线后跟透明度"),
    ]),
    h2("默认色相"),
    p("调色板包含 red、orange、amber、yellow、lime、green、emerald、teal、cyan、sky、blue、indigo、violet、purple、fuchsia、pink、rose，以及 slate、gray、zinc、neutral、stone。每一组都有 50、100、200、300、400、500、600、700、800、900、950。"),
    code("html", '<p class="text-sky-600 dark:text-sky-400">链接与强调色</p>'),
    tip("不要只靠颜色传达状态。成功、警告和错误还应配上文字或图标。"),
], demo="bg-sky-500 text-white", preview="color")

page("adding-custom-styles", "添加自定义样式", "当实用类不够用时，可以加主题变量、自定义实用类，或在组件层写少量 CSS。", G, [
    h2("自定义实用类"),
    code("css", """@utility content-auto {
  content-visibility: auto;
}"""),
    p("定义之后就可以像内置类一样使用 content-auto，也可以加 hover: 和 md: 前缀。"),
    h2("任意值"),
    p("偶尔出现的一次性数值可以用方括号，例如 top-[117px] 或 grid-cols-[1fr_2fr]。如果同一个值出现多次，应提升为主题变量。"),
    h2("少用 @apply"),
    code("css", """.btn {
  @apply rounded-full bg-gray-950 px-4 py-2 text-sm font-semibold text-white;
}"""),
    p("@apply 适合把类收进必须由第三方选择器控制的地方。在 Vue 组件里，直接把类写在模板上通常更易读。"),
    tip("级联层的顺序是 theme、base、components、utilities。实用类层赢过组件层，因此你很少需要和优先级搏斗。"),
])

page("detecting-classes-in-source-files", "在源文件中检测类名", "Tailwind 只生成它在源码里真正看到的类。", G, [
    p("扫描器会读取项目文件，提取完整的类名标记。它不执行 JavaScript，所以运行时拼出来的字符串不会生效。"),
    h2("这样写"),
    code("html", """<div :class="isOn ? 'bg-sky-500' : 'bg-gray-200'"></div>"""),
    h2("不要这样写"),
    code("html", """<div :class="`bg-${color}-500`"></div>"""),
    p("如果颜色来自数据，把可选类名做成对象映射，让每个完整类名都出现在源文件中。"),
    h2("额外源文件"),
    code("css", """@source "../node_modules/@acme/ui";
@source not "../legacy";"""),
    tip("本站把文档数据放在 app/data 下，类名以完整字符串写在 JSON 和 Vue 模板里，因此预览能正确生成。"),
])

page("functions-and-directives", "函数与指令", "入口 CSS 里的少量指令负责导入、主题、分层和自定义实用类。", G, [
    h2("指令"),
    table([
        ("@import \"tailwindcss\"", "入口", "载入主题、预检和实用类"),
        ("@theme", "主题", "声明设计变量"),
        ("@utility", "实用类", "新增可加变体的类"),
        ("@layer", "分层", "把自定义 CSS 放进指定层"),
        ("@source", "扫描", "增加或排除源文件"),
        ("@custom-variant", "变体", "例如深色模式类策略"),
        ("@apply", "内联", "在 CSS 里引用实用类"),
    ]),
    h2("theme()"),
    p("在仍需要读取主题值的自定义 CSS 里，可以用 theme(--color-sky-500) 拿到变量。更常见的做法是直接使用生成好的 CSS 变量，例如 var(--color-sky-500)。"),
    code("css", """@layer components {
  .card {
    background: var(--color-white);
    border-radius: var(--radius-xl);
  }
}"""),
])

# ---------- 基础样式 ----------
G = "基础样式"
add_group(G, [{"title": "Preflight", "slug": "preflight"}])
page("preflight", "Preflight", "Preflight 是一套温和的基础样式，用来抹平浏览器默认差异。", G, [
    p("它会去掉 body 的默认外边距，统一标题字号继承，让图片变成块级且最大宽度为 100%，并为按钮和表单设置更可预测的字体。"),
    h2("它会做什么"),
    table([
        ("margin: 0", "body、标题、列表", "间距改由实用类控制"),
        ("box-sizing: border-box", "所有元素", "宽高包含边框和内边距"),
        ("img { max-width: 100% }", "图片与视频", "避免撑破布局"),
        ("button 字体继承", "表单控件", "不再突然变成系统字体"),
    ]),
    p("如果不想使用 Preflight，可以只导入主题和实用类。多数项目保留它更省心。"),
    tip("列表项目符号默认被去掉。需要符号时加上 list-disc 和 pl-5。"),
], demo="list-disc pl-5", preview="text")

# ---------- utilities ----------

def rows_box(pairs):
    return pairs

LAYOUT = "布局"
add_group(LAYOUT, [
    {"title": "aspect-ratio", "slug": "aspect-ratio"},
    {"title": "columns", "slug": "columns"},
    {"title": "break-after", "slug": "break-after"},
    {"title": "break-before", "slug": "break-before"},
    {"title": "break-inside", "slug": "break-inside"},
    {"title": "box-decoration-break", "slug": "box-decoration-break"},
    {"title": "box-sizing", "slug": "box-sizing"},
    {"title": "display", "slug": "display"},
    {"title": "float", "slug": "float"},
    {"title": "clear", "slug": "clear"},
    {"title": "isolation", "slug": "isolation"},
    {"title": "object-fit", "slug": "object-fit"},
    {"title": "object-position", "slug": "object-position"},
    {"title": "overflow", "slug": "overflow"},
    {"title": "overscroll-behavior", "slug": "overscroll-behavior"},
    {"title": "position", "slug": "position"},
    {"title": "top / right / bottom / left", "slug": "top-right-bottom-left"},
    {"title": "visibility", "slug": "visibility"},
    {"title": "z-index", "slug": "z-index"},
])

util("aspect-ratio", "aspect-ratio", "控制元素的宽高比，常用于图片、视频和卡片封面。", LAYOUT, "aspect-ratio", [
    ("aspect-auto", "aspect-ratio: auto", "由内容决定"),
    ("aspect-square", "aspect-ratio: 1 / 1", "正方形"),
    ("aspect-video", "aspect-ratio: 16 / 9", "视频"),
    ("aspect-3/2", "aspect-ratio: 3 / 2", "照片"),
], preview="box", demo="aspect-video w-full bg-sky-500")

util("columns", "columns", "把内容排成报纸式的多栏。", LAYOUT, "columns", [
    ("columns-1", "columns: 1", "单栏"),
    ("columns-2", "columns: 2", "两栏"),
    ("columns-3", "columns: 3", "三栏"),
    ("columns-auto", "columns: auto", "自动"),
], preview="text", demo="columns-2 gap-8")

util("break-after", "break-after", "控制元素之后是否强制分页、分栏或换区域。", LAYOUT, "break-after", [
    ("break-after-auto", "break-after: auto", "自动"),
    ("break-after-avoid", "break-after: avoid", "尽量不断开"),
    ("break-after-page", "break-after: page", "之后分页"),
    ("break-after-column", "break-after: column", "之后分栏"),
], preview="text")

util("break-before", "break-before", "控制元素之前是否强制分页或分栏。", LAYOUT, "break-before", [
    ("break-before-auto", "break-before: auto", "自动"),
    ("break-before-avoid", "break-before: avoid", "尽量不断开"),
    ("break-before-page", "break-before: page", "之前分页"),
    ("break-before-column", "break-before: column", "之前分栏"),
], preview="text")

util("break-inside", "break-inside", "避免卡片或图片在分栏、分页时被从中间切开。", LAYOUT, "break-inside", [
    ("break-inside-auto", "break-inside: auto", "允许断开"),
    ("break-inside-avoid", "break-inside: avoid", "保持完整"),
], preview="box", demo="break-inside-avoid")

util("box-decoration-break", "box-decoration-break", "决定背景和边框在换行时是连成一块，还是每行独立。", LAYOUT, "box-decoration-break", [
    ("box-decoration-slice", "box-decoration-break: slice", "整段共享装饰"),
    ("box-decoration-clone", "box-decoration-break: clone", "每一行克隆装饰"),
], preview="text", demo="box-decoration-clone bg-sky-200 px-2")

util("box-sizing", "box-sizing", "决定宽高是否包含内边距和边框。Preflight 已把全局设为 border-box。", LAYOUT, "box-sizing", [
    ("box-border", "box-sizing: border-box", "推荐，尺寸更好预测"),
    ("box-content", "box-sizing: content-box", "恢复传统内容盒"),
], preview="box", demo="box-border w-40 border-4 p-4")

util("display", "display", "设置元素的盒子类型，是布局的起点。", LAYOUT, "display", [
    ("block", "display: block", "块级"),
    ("inline", "display: inline", "行内"),
    ("inline-block", "display: inline-block", "行内块"),
    ("flex", "display: flex", "弹性布局"),
    ("inline-flex", "display: inline-flex", "行内弹性"),
    ("grid", "display: grid", "网格"),
    ("hidden", "display: none", "不显示，也不占位"),
], preview="flex", demo="flex gap-3")

util("float", "float", "让元素向左或向右浮动，文字绕排。现代布局更常用 flex 和 grid。", LAYOUT, "float", [
    ("float-start", "float: inline-start", "书写方向的起始侧"),
    ("float-end", "float: inline-end", "书写方向的结束侧"),
    ("float-none", "float: none", "不浮动"),
], preview="box", demo="float-end")

util("clear", "clear", "指定元素哪一侧不允许再紧挨浮动元素。", LAYOUT, "clear", [
    ("clear-start", "clear: inline-start", "清除起始侧"),
    ("clear-end", "clear: inline-end", "清除结束侧"),
    ("clear-both", "clear: both", "两侧都清除"),
    ("clear-none", "clear: none", "不清除"),
], preview="box")

util("isolation", "isolation", "建立新的层叠上下文，避免 z-index 和混合模式互相干扰。", LAYOUT, "isolation", [
    ("isolate", "isolation: isolate", "新建层叠上下文"),
    ("isolation-auto", "isolation: auto", "默认"),
], preview="box", demo="isolate")

util("object-fit", "object-fit", "控制被替换元素（图片、视频）如何填满容器。", LAYOUT, "object-fit", [
    ("object-contain", "object-fit: contain", "完整显示，可能留白"),
    ("object-cover", "object-fit: cover", "铺满并裁切"),
    ("object-fill", "object-fit: fill", "拉伸铺满"),
    ("object-none", "object-fit: none", "保持原始尺寸"),
    ("object-scale-down", "object-fit: scale-down", "取 none 与 contain 中更小者"),
], preview="box", demo="object-cover")

util("object-position", "object-position", "在 object-cover 裁切时，决定保留图片的哪一部分。", LAYOUT, "object-position", [
    ("object-bottom", "object-position: bottom", "靠下"),
    ("object-center", "object-position: center", "居中"),
    ("object-top", "object-position: top", "靠上"),
    ("object-left", "object-position: left", "靠左"),
    ("object-right", "object-position: right", "靠右"),
], preview="box", demo="object-cover object-top")

util("overflow", "overflow", "控制内容超出内边距盒时是否裁切或滚动。", LAYOUT, "overflow", [
    ("overflow-auto", "overflow: auto", "需要时出现滚动条"),
    ("overflow-hidden", "overflow: hidden", "直接裁切"),
    ("overflow-scroll", "overflow: scroll", "始终保留滚动条"),
    ("overflow-visible", "overflow: visible", "允许溢出"),
    ("overflow-x-auto", "overflow-x: auto", "只处理横向"),
    ("overflow-y-auto", "overflow-y: auto", "只处理纵向"),
], preview="box", demo="h-16 overflow-hidden")

util("overscroll-behavior", "overscroll-behavior", "控制滚动到边缘时是否把滚动链式传递给父级，常用于弹层。", LAYOUT, "overscroll-behavior", [
    ("overscroll-auto", "overscroll-behavior: auto", "允许链式滚动"),
    ("overscroll-contain", "overscroll-behavior: contain", "滚到头就停住"),
    ("overscroll-none", "overscroll-behavior: none", "同时抑制回弹"),
], preview="box", demo="overscroll-contain")

util("position", "position", "设置定位方式。配合 top、right、bottom、left 或 inset 使用。", LAYOUT, "position", [
    ("static", "position: static", "正常流"),
    ("relative", "position: relative", "相对自身偏移，作为绝对子元素的参照"),
    ("absolute", "position: absolute", "相对最近的定位祖先"),
    ("fixed", "position: fixed", "相对视口"),
    ("sticky", "position: sticky", "滚动到阈值后粘住"),
], preview="position", demo="relative")

util("top-right-bottom-left", "top / right / bottom / left", "为已定位元素设置偏移。也提供逻辑属性 inset-x、inset-y 和 inset。", LAYOUT, "inset / top / right / bottom / left", [
    ("inset-0", "inset: 0", "铺满定位祖先"),
    ("inset-x-0", "left/right: 0", "水平拉满"),
    ("top-4", "top: 1rem", "距顶 1rem"),
    ("right-0", "right: 0", "贴右"),
    ("bottom-0", "bottom: 0", "贴底"),
    ("left-1/2", "left: 50%", "水平中线，常配 -translate-x-1/2"),
], preview="position", demo="top-4")

util("visibility", "visibility", "隐藏元素但继续占位。与 hidden（display: none）不同。", LAYOUT, "visibility", [
    ("visible", "visibility: visible", "可见"),
    ("invisible", "visibility: hidden", "不可见但仍占空间"),
    ("collapse", "visibility: collapse", "表格行或列可折叠"),
], preview="box", demo="invisible")

util("z-index", "z-index", "控制层叠顺序。只对定位元素或创建了层叠上下文的元素有意义。", LAYOUT, "z-index", [
    ("z-0", "z-index: 0", "基线"),
    ("z-10", "z-index: 10", "略高"),
    ("z-20", "z-index: 20", "下拉"),
    ("z-40", "z-index: 40", "粘性顶栏"),
    ("z-50", "z-index: 50", "弹层"),
    ("-z-10", "z-index: -10", "放到后面"),
], preview="position", demo="z-10")

FLEX = "弹性盒与网格"
add_group(FLEX, [
    {"title": "flex-basis", "slug": "flex-basis"},
    {"title": "flex-direction", "slug": "flex-direction"},
    {"title": "flex-wrap", "slug": "flex-wrap"},
    {"title": "flex", "slug": "flex"},
    {"title": "flex-grow", "slug": "flex-grow"},
    {"title": "flex-shrink", "slug": "flex-shrink"},
    {"title": "order", "slug": "order"},
    {"title": "grid-template-columns", "slug": "grid-template-columns"},
    {"title": "grid-column", "slug": "grid-column"},
    {"title": "grid-template-rows", "slug": "grid-template-rows"},
    {"title": "grid-row", "slug": "grid-row"},
    {"title": "grid-auto-flow", "slug": "grid-auto-flow"},
    {"title": "grid-auto-columns", "slug": "grid-auto-columns"},
    {"title": "grid-auto-rows", "slug": "grid-auto-rows"},
    {"title": "gap", "slug": "gap"},
    {"title": "justify-content", "slug": "justify-content"},
    {"title": "justify-items", "slug": "justify-items"},
    {"title": "justify-self", "slug": "justify-self"},
    {"title": "align-content", "slug": "align-content"},
    {"title": "align-items", "slug": "align-items"},
    {"title": "align-self", "slug": "align-self"},
    {"title": "place-content", "slug": "place-content"},
    {"title": "place-items", "slug": "place-items"},
    {"title": "place-self", "slug": "place-self"},
])

util("flex-basis", "flex-basis", "设置弹性项目在分配剩余空间之前的初始主尺寸。", FLEX, "flex-basis", [
    ("basis-0", "flex-basis: 0", "从 0 开始分配"),
    ("basis-auto", "flex-basis: auto", "按内容"),
    ("basis-full", "flex-basis: 100%", "占满一行"),
    ("basis-1/2", "flex-basis: 50%", "一半"),
    ("basis-64", "flex-basis: 16rem", "固定起始宽度"),
], preview="flex", demo="basis-1/2")

util("flex-direction", "flex-direction", "决定主轴方向。", FLEX, "flex-direction", [
    ("flex-row", "flex-direction: row", "横向，默认"),
    ("flex-row-reverse", "flex-direction: row-reverse", "横向反向"),
    ("flex-col", "flex-direction: column", "纵向"),
    ("flex-col-reverse", "flex-direction: column-reverse", "纵向反向"),
], preview="flex", demo="flex flex-col gap-2")

util("flex-wrap", "flex-wrap", "空间不够时是否换行。", FLEX, "flex-wrap", [
    ("flex-nowrap", "flex-wrap: nowrap", "不换行"),
    ("flex-wrap", "flex-wrap: wrap", "换行"),
    ("flex-wrap-reverse", "flex-wrap: wrap-reverse", "反向换行"),
], preview="flex", demo="flex flex-wrap gap-2")

util("flex", "flex", "同时设置伸缩、收缩和基准，是 flex-grow / shrink / basis 的简写。", FLEX, "flex", [
    ("flex-1", "flex: 1 1 0%", "平均占满剩余空间"),
    ("flex-auto", "flex: 1 1 auto", "按内容起步再伸缩"),
    ("flex-initial", "flex: 0 1 auto", "默认可收缩"),
    ("flex-none", "flex: none", "不伸缩"),
], preview="flex", demo="flex flex-1")

util("flex-grow", "flex-grow", "允许项目占据剩余空间。", FLEX, "flex-grow", [
    ("grow", "flex-grow: 1", "增长"),
    ("grow-0", "flex-grow: 0", "不增长"),
], preview="flex", demo="grow")

util("flex-shrink", "flex-shrink", "空间不足时是否允许项目变小。", FLEX, "flex-shrink", [
    ("shrink", "flex-shrink: 1", "允许收缩"),
    ("shrink-0", "flex-shrink: 0", "保持尺寸，适合图标"),
], preview="flex", demo="shrink-0")

util("order", "order", "改变弹性或网格项目的视觉顺序，而不改 DOM 顺序。", FLEX, "order", [
    ("order-1", "order: 1", "靠后"),
    ("order-2", "order: 2", "更后"),
    ("order-first", "order: -9999", "移到最前"),
    ("order-last", "order: 9999", "移到最后"),
    ("order-none", "order: 0", "默认"),
], preview="flex", demo="order-first")

util("grid-template-columns", "grid-template-columns", "定义网格列。这是用类名表达复杂布局的核心。", FLEX, "grid-template-columns", [
    ("grid-cols-1", "grid-template-columns: repeat(1, minmax(0, 1fr))", "一列"),
    ("grid-cols-2", "两列等分", "卡片列表"),
    ("grid-cols-3", "三列等分", "图库"),
    ("grid-cols-4", "四列等分", "桌面密集列表"),
    ("grid-cols-12", "十二列", "经典栅格"),
    ("grid-cols-none", "grid-template-columns: none", "不显式分列"),
], preview="grid", demo="grid grid-cols-3 gap-3")

util("grid-column", "grid-column", "让项目横跨多列。", FLEX, "grid-column", [
    ("col-auto", "grid-column: auto", "自动"),
    ("col-span-2", "grid-column: span 2", "跨两列"),
    ("col-span-full", "grid-column: 1 / -1", "占满整行"),
    ("col-start-2", "grid-column-start: 2", "从第 2 列开始"),
], preview="grid", demo="col-span-2")

util("grid-template-rows", "grid-template-rows", "定义网格行的高度轨道。", FLEX, "grid-template-rows", [
    ("grid-rows-1", "一行", "单行"),
    ("grid-rows-2", "两行等分", "等高行"),
    ("grid-rows-3", "三行等分", "等高行"),
    ("grid-rows-none", "grid-template-rows: none", "由内容决定"),
], preview="grid", demo="grid grid-rows-2")

util("grid-row", "grid-row", "让项目纵跨多行。", FLEX, "grid-row", [
    ("row-auto", "grid-row: auto", "自动"),
    ("row-span-2", "grid-row: span 2", "跨两行"),
    ("row-span-full", "占满所有行", "侧栏常用"),
    ("row-start-2", "grid-row-start: 2", "从第 2 行开始"),
], preview="grid", demo="row-span-2")

util("grid-auto-flow", "grid-auto-flow", "决定自动放置算法先走列还是先行，以及是否尽量填满空洞。", FLEX, "grid-auto-flow", [
    ("grid-flow-row", "grid-auto-flow: row", "先行后列"),
    ("grid-flow-col", "grid-auto-flow: column", "先列后行"),
    ("grid-flow-dense", "grid-auto-flow: dense", "尽量填坑"),
    ("grid-flow-row-dense", "row dense", "按行并填坑"),
], preview="grid", demo="grid-flow-col")

util("grid-auto-columns", "grid-auto-columns", "设置隐式创建的列宽。", FLEX, "grid-auto-columns", [
    ("auto-cols-auto", "grid-auto-columns: auto", "按内容"),
    ("auto-cols-min", "grid-auto-columns: min-content", "最小内容"),
    ("auto-cols-max", "grid-auto-columns: max-content", "最大内容"),
    ("auto-cols-fr", "grid-auto-columns: minmax(0, 1fr)", "等分"),
], preview="grid", demo="auto-cols-fr")

util("grid-auto-rows", "grid-auto-rows", "设置隐式创建的行高。", FLEX, "grid-auto-rows", [
    ("auto-rows-auto", "grid-auto-rows: auto", "按内容"),
    ("auto-rows-min", "min-content", "最小内容"),
    ("auto-rows-max", "max-content", "最大内容"),
    ("auto-rows-fr", "minmax(0, 1fr)", "等分"),
], preview="grid", demo="auto-rows-fr")

util("gap", "gap", "设置弹性盒或网格项目之间的缝隙。1 单位等于 0.25rem。", FLEX, "gap", [
    ("gap-0", "gap: 0", "无缝"),
    ("gap-2", "gap: 0.5rem", "紧凑"),
    ("gap-4", "gap: 1rem", "常规"),
    ("gap-8", "gap: 2rem", "宽松"),
    ("gap-x-6", "column-gap: 1.5rem", "只设列距"),
    ("gap-y-3", "row-gap: 0.75rem", "只设行距"),
], preview="grid", demo="flex gap-4")

util("justify-content", "justify-content", "沿主轴分配项目之间的空间。", FLEX, "justify-content", [
    ("justify-start", "justify-content: flex-start", "靠起始边"),
    ("justify-center", "justify-content: center", "居中"),
    ("justify-end", "justify-content: flex-end", "靠结束边"),
    ("justify-between", "justify-content: space-between", "两端对齐"),
    ("justify-around", "justify-content: space-around", "环绕间距"),
    ("justify-evenly", "justify-content: space-evenly", "完全均分"),
], preview="flex", demo="flex justify-between")

util("justify-items", "justify-items", "在网格中，沿行方向对齐每个单元格里的项目。", FLEX, "justify-items", [
    ("justify-items-start", "justify-items: start", "靠起始边"),
    ("justify-items-center", "justify-items: center", "居中"),
    ("justify-items-end", "justify-items: end", "靠结束边"),
    ("justify-items-stretch", "justify-items: stretch", "拉伸"),
], preview="grid", demo="justify-items-center")

util("justify-self", "justify-self", "只调整某一个网格项目在单元格内的行向对齐。", FLEX, "justify-self", [
    ("justify-self-auto", "justify-self: auto", "继承"),
    ("justify-self-start", "justify-self: start", "靠起始边"),
    ("justify-self-center", "justify-self: center", "居中"),
    ("justify-self-end", "justify-self: end", "靠结束边"),
], preview="grid", demo="justify-self-end")

util("align-content", "align-content", "多行内容沿交叉轴分配额外空间。", FLEX, "align-content", [
    ("content-start", "align-content: flex-start", "靠起始边"),
    ("content-center", "align-content: center", "居中"),
    ("content-between", "align-content: space-between", "两端对齐"),
    ("content-evenly", "align-content: space-evenly", "均分"),
], preview="flex", demo="content-center")

util("align-items", "align-items", "沿交叉轴对齐项目。横向 flex 里就是垂直对齐。", FLEX, "align-items", [
    ("items-start", "align-items: flex-start", "顶部"),
    ("items-center", "align-items: center", "居中"),
    ("items-end", "align-items: flex-end", "底部"),
    ("items-stretch", "align-items: stretch", "拉伸"),
    ("items-baseline", "align-items: baseline", "基线对齐"),
], preview="flex", demo="flex items-center")

util("align-self", "align-self", "覆盖单个项目的交叉轴对齐。", FLEX, "align-self", [
    ("self-auto", "align-self: auto", "继承"),
    ("self-start", "align-self: flex-start", "靠起始边"),
    ("self-center", "align-self: center", "居中"),
    ("self-end", "align-self: flex-end", "靠结束边"),
    ("self-stretch", "align-self: stretch", "拉伸"),
], preview="flex", demo="self-center")

util("place-content", "place-content", "同时设置 align-content 和 justify-content。", FLEX, "place-content", [
    ("place-content-center", "place-content: center", "两个方向居中"),
    ("place-content-start", "place-content: start", "靠起始角"),
    ("place-content-end", "place-content: end", "靠结束角"),
    ("place-content-between", "place-content: space-between", "两端"),
], preview="grid", demo="place-content-center")

util("place-items", "place-items", "同时设置 align-items 和 justify-items。", FLEX, "place-items", [
    ("place-items-center", "place-items: center", "单元格内居中"),
    ("place-items-start", "place-items: start", "靠起始角"),
    ("place-items-end", "place-items: end", "靠结束角"),
    ("place-items-stretch", "place-items: stretch", "拉伸"),
], preview="grid", demo="grid place-items-center")

util("place-self", "place-self", "同时设置单个项目的 align-self 和 justify-self。", FLEX, "place-self", [
    ("place-self-auto", "place-self: auto", "继承"),
    ("place-self-start", "place-self: start", "靠起始角"),
    ("place-self-center", "place-self: center", "居中"),
    ("place-self-end", "place-self: end", "靠结束角"),
], preview="grid", demo="place-self-center")

SP = "间距"
add_group(SP, [
    {"title": "padding", "slug": "padding"},
    {"title": "margin", "slug": "margin"},
])

scale = [
    ("0", "0", "0"),
    ("px", "1px", "1 像素"),
    ("0.5", "0.125rem", "2px"),
    ("1", "0.25rem", "4px"),
    ("2", "0.5rem", "8px"),
    ("4", "1rem", "16px"),
    ("6", "1.5rem", "24px"),
    ("8", "2rem", "32px"),
]
util("padding", "padding", "内边距使用 p、px、py、pt、pr、pb、pl、ps、pe。数字刻度的 1 等于 0.25rem。", SP, "padding", [
    (f"p-{k}", f"padding: {v}", note) for k, v, note in scale
] + [
    ("px-4", "padding-left/right: 1rem", "水平"),
    ("py-2", "padding-top/bottom: 0.5rem", "垂直"),
    ("ps-4", "padding-inline-start: 1rem", "逻辑起始边，适合多语言"),
], preview="spacing", demo="p-6")

util("margin", "margin", "外边距使用 m、mx、my、mt、mr、mb、ml、ms、me，并支持负值。", SP, "margin", [
    (f"m-{k}", f"margin: {v}", note) for k, v, note in scale
] + [
    ("mx-auto", "margin-left/right: auto", "水平居中定宽块"),
    ("-mt-4", "margin-top: -1rem", "负外边距"),
    ("ms-auto", "margin-inline-start: auto", "把项目推到行尾"),
], preview="spacing", demo="mx-auto mt-4")

SZ = "尺寸"
add_group(SZ, [
    {"title": "width", "slug": "width"},
    {"title": "min-width", "slug": "min-width"},
    {"title": "max-width", "slug": "max-width"},
    {"title": "height", "slug": "height"},
    {"title": "min-height", "slug": "min-height"},
    {"title": "max-height", "slug": "max-height"},
    {"title": "inline-size", "slug": "inline-size"},
    {"title": "min-inline-size", "slug": "min-inline-size"},
    {"title": "max-inline-size", "slug": "max-inline-size"},
    {"title": "block-size", "slug": "block-size"},
    {"title": "min-block-size", "slug": "min-block-size"},
    {"title": "max-block-size", "slug": "max-block-size"},
])

util("width", "width", "设置宽度。分数、固定刻度、全宽和屏幕宽度都可以。", SZ, "width", [
    ("w-auto", "width: auto", "自动"),
    ("w-full", "width: 100%", "撑满父级"),
    ("w-screen", "width: 100vw", "视口宽度"),
    ("w-1/2", "width: 50%", "一半"),
    ("w-64", "width: 16rem", "16rem"),
    ("w-fit", "width: fit-content", "包住内容"),
], preview="box", demo="w-1/2 bg-sky-500")

util("min-width", "min-width", "设置最小宽度，防止弹性项目被压得太窄。", SZ, "min-width", [
    ("min-w-0", "min-width: 0", "允许收缩到 0，避免溢出"),
    ("min-w-full", "min-width: 100%", "至少和父级一样宽"),
    ("min-w-64", "min-width: 16rem", "侧栏常用"),
    ("min-w-fit", "min-width: fit-content", "不窄于内容"),
], preview="box", demo="min-w-64")

util("max-width", "max-width", "限制最大宽度。阅读文本通常限制在 max-w-prose 或 max-w-3xl。", SZ, "max-width", [
    ("max-w-none", "max-width: none", "不限制"),
    ("max-w-sm", "max-width: 24rem", "小卡片"),
    ("max-w-3xl", "max-width: 48rem", "文档正文"),
    ("max-w-7xl", "max-width: 80rem", "页面容器"),
    ("max-w-prose", "65ch", "适合长文"),
    ("max-w-full", "max-width: 100%", "不超过父级"),
], preview="box", demo="max-w-sm")

util("height", "height", "设置高度。", SZ, "height", [
    ("h-auto", "height: auto", "自动"),
    ("h-full", "height: 100%", "撑满父级"),
    ("h-screen", "height: 100vh", "视口高度"),
    ("h-64", "height: 16rem", "固定高度"),
    ("h-fit", "height: fit-content", "包住内容"),
], preview="box", demo="h-16 bg-sky-500")

util("min-height", "min-height", "设置最小高度，让区块即使内容很少也保持存在感。", SZ, "min-height", [
    ("min-h-0", "min-height: 0", "允许收缩"),
    ("min-h-full", "min-height: 100%", "至少和父级一样高"),
    ("min-h-screen", "min-height: 100vh", "至少一屏"),
    ("min-h-64", "min-height: 16rem", "固定下限"),
], preview="box", demo="min-h-24")

util("max-height", "max-height", "限制最大高度，常配合 overflow-auto 做滚动区域。", SZ, "max-height", [
    ("max-h-none", "max-height: none", "不限制"),
    ("max-h-64", "max-height: 16rem", "卡片内滚动"),
    ("max-h-screen", "max-height: 100vh", "不超过一屏"),
    ("max-h-full", "max-height: 100%", "不超过父级"),
], preview="box", demo="max-h-16 overflow-auto")

util("inline-size", "inline-size", "逻辑宽度，随书写方向变化。横向文字里相当于 width。", SZ, "inline-size", [
    ("inline-auto", "inline-size: auto", "自动"),
    ("w-inline 等价写法用 inline-size 任意值", "inline-size", "v4 提供 size 相关逻辑类"),
    ("size-16", "width/height: 4rem", "同时设置宽高时更常用 size"),
], extra=[
    p("需要同时设定宽高时，用 size-16、size-full。只控制行内尺寸时使用逻辑属性，方便同一套布局服务从左到右和从右到左的语言。"),
], preview="box", demo="size-16 bg-sky-500")

util("min-inline-size", "min-inline-size", "逻辑方向上的最小尺寸。", SZ, "min-inline-size", [
    ("min-w-0", "在横向文字中接近 min-inline-size: 0", "允许网格子项收缩"),
    ("min-w-full", "min-inline-size: 100%", "下限为父级"),
], preview="box", demo="min-w-full")

util("max-inline-size", "max-inline-size", "逻辑方向上的最大尺寸。", SZ, "max-inline-size", [
    ("max-w-prose", "约 65ch", "阅读宽度"),
    ("max-w-full", "100%", "不超过容器"),
], preview="box", demo="max-w-prose")

util("block-size", "block-size", "逻辑高度。横向文字里相当于 height。", SZ, "block-size", [
    ("h-full", "block-size: 100%", "撑满"),
    ("h-screen", "100vh", "一屏"),
    ("h-svh", "100svh", "小视口高度，移动端地址栏变化时更稳"),
], preview="box", demo="h-16")

util("min-block-size", "min-block-size", "逻辑方向上的最小块尺寸。", SZ, "min-block-size", [
    ("min-h-screen", "100vh", "整页至少一屏"),
    ("min-h-full", "100%", "填满父级"),
], preview="box", demo="min-h-16")

util("max-block-size", "max-block-size", "逻辑方向上的最大块尺寸。", SZ, "max-block-size", [
    ("max-h-screen", "100vh", "不超过视口"),
    ("max-h-full", "100%", "不超过父级"),
], preview="box", demo="max-h-16")

TY = "排版"
add_group(TY, [
    {"title": "font-family", "slug": "font-family"},
    {"title": "font-size", "slug": "font-size"},
    {"title": "font-smoothing", "slug": "font-smoothing"},
    {"title": "font-style", "slug": "font-style"},
    {"title": "font-weight", "slug": "font-weight"},
    {"title": "font-stretch", "slug": "font-stretch"},
    {"title": "font-variant-numeric", "slug": "font-variant-numeric"},
    {"title": "font-feature-settings", "slug": "font-feature-settings"},
    {"title": "letter-spacing", "slug": "letter-spacing"},
    {"title": "line-clamp", "slug": "line-clamp"},
    {"title": "line-height", "slug": "line-height"},
    {"title": "list-style-image", "slug": "list-style-image"},
    {"title": "list-style-position", "slug": "list-style-position"},
    {"title": "list-style-type", "slug": "list-style-type"},
    {"title": "text-align", "slug": "text-align"},
    {"title": "color", "slug": "color"},
    {"title": "text-decoration-line", "slug": "text-decoration-line"},
    {"title": "text-decoration-color", "slug": "text-decoration-color"},
    {"title": "text-decoration-style", "slug": "text-decoration-style"},
    {"title": "text-decoration-thickness", "slug": "text-decoration-thickness"},
    {"title": "text-underline-offset", "slug": "text-underline-offset"},
    {"title": "text-transform", "slug": "text-transform"},
    {"title": "text-overflow", "slug": "text-overflow"},
    {"title": "text-wrap", "slug": "text-wrap"},
    {"title": "text-indent", "slug": "text-indent"},
    {"title": "tab-size", "slug": "tab-size"},
    {"title": "vertical-align", "slug": "vertical-align"},
    {"title": "white-space", "slug": "white-space"},
    {"title": "word-break", "slug": "word-break"},
    {"title": "overflow-wrap", "slug": "overflow-wrap"},
    {"title": "hyphens", "slug": "hyphens"},
    {"title": "content", "slug": "content"},
])

util("font-family", "font-family", "切换字族。本站正文是 Inter 加思源黑体回退，代码是 IBM Plex Mono。", TY, "font-family", [
    ("font-sans", "var(--font-sans)", "界面正文"),
    ("font-serif", "衬线字族", "长文或标题点缀"),
    ("font-mono", "var(--font-mono)", "代码"),
], preview="text", demo="font-mono")

util("font-size", "font-size", "字号类同时带有推荐行高。中文标题不宜再叠过紧的字距。", TY, "font-size", [
    ("text-xs", "0.75rem", "辅助说明"),
    ("text-sm", "0.875rem", "次要文字"),
    ("text-base", "1rem", "正文"),
    ("text-lg", "1.125rem", "导语"),
    ("text-xl", "1.25rem", "小标题"),
    ("text-2xl", "1.5rem", "卡片标题"),
    ("text-4xl", "2.25rem", "章节标题"),
    ("text-6xl", "3.75rem", "主标题"),
], preview="text", demo="text-4xl font-medium tracking-tight")

util("font-smoothing", "font-smoothing", "在 macOS 上调整灰度抗锯齿或子像素渲染。", TY, "-webkit-font-smoothing", [
    ("antialiased", "灰度抗锯齿", "本站默认"),
    ("subpixel-antialiased", "子像素渲染", "浅色小字可能更清晰"),
], preview="text", demo="antialiased")

util("font-style", "font-style", "切换正体与斜体。中文斜体通常不明显，英文强调更适合。", TY, "font-style", [
    ("italic", "font-style: italic", "斜体"),
    ("not-italic", "font-style: normal", "取消斜体"),
], preview="text", demo="italic")

util("font-weight", "font-weight", "字重。中文界面常用 400、500 和 700。", TY, "font-weight", [
    ("font-normal", "400", "正文"),
    ("font-medium", "500", "导航与按钮"),
    ("font-semibold", "600", "小标题"),
    ("font-bold", "700", "强调"),
], preview="text", demo="font-semibold")

util("font-stretch", "font-stretch", "调整可变字体的宽度轴。普通字体可能看不出差别。", TY, "font-stretch", [
    ("font-stretch-normal", "font-stretch: normal", "正常"),
    ("font-stretch-condensed", "font-stretch: condensed", "变窄"),
    ("font-stretch-expanded", "font-stretch: expanded", "变宽"),
], preview="text", demo="font-stretch-condensed")

util("font-variant-numeric", "font-variant-numeric", "控制数字的表格对齐、分数和旧式数字。", TY, "font-variant-numeric", [
    ("tabular-nums", "tabular-nums", "等宽数字，适合价格和计数"),
    ("proportional-nums", "proportional-nums", "比例数字"),
    ("diagonal-fractions", "diagonal-fractions", "斜分数"),
    ("oldstyle-nums", "oldstyle-nums", "旧式数字"),
], preview="text", demo="tabular-nums")

util("font-feature-settings", "font-feature-settings", "打开或关闭 OpenType 特性。", TY, "font-feature-settings", [
    ("normal-nums", "font-variant-numeric: normal", "恢复默认数字"),
    ("lining-nums", "lining-nums", "对齐的现代数字"),
], preview="text", demo="lining-nums")

util("letter-spacing", "letter-spacing", "字距。大标题可以略紧，全大写英文标签可以略松。中文正文保持正常。", TY, "letter-spacing", [
    ("tracking-tighter", "letter-spacing: -0.05em", "很紧"),
    ("tracking-tight", "letter-spacing: -0.025em", "稍紧"),
    ("tracking-normal", "letter-spacing: 0", "正常"),
    ("tracking-wide", "letter-spacing: 0.025em", "稍松"),
    ("tracking-widest", "letter-spacing: 0.1em", "标签常用"),
], preview="text", demo="tracking-widest")

util("line-clamp", "line-clamp", "把文字限制在固定行数，并在末尾显示省略号。", TY, "-webkit-line-clamp", [
    ("line-clamp-1", "1 行", "标题"),
    ("line-clamp-2", "2 行", "卡片摘要"),
    ("line-clamp-3", "3 行", "列表简介"),
    ("line-clamp-none", "不限制", "展开后"),
], preview="text", demo="line-clamp-2")

util("line-height", "line-height", "行高。也可以写在字号后面，例如 text-base/7。", TY, "line-height", [
    ("leading-none", "line-height: 1", "标题"),
    ("leading-tight", "1.25", "紧凑标题"),
    ("leading-snug", "1.375", "小标题"),
    ("leading-normal", "1.5", "默认"),
    ("leading-relaxed", "1.625", "长文"),
], preview="text", demo="leading-relaxed")

util("list-style-image", "list-style-image", "用图片代替列表符号。多数界面直接用 list-disc 更清晰。", TY, "list-style-image", [
    ("list-image-none", "list-style-image: none", "不使用图片符号"),
], preview="text", demo="list-image-none")

util("list-style-position", "list-style-position", "符号放在内容盒内部还是外部。", TY, "list-style-position", [
    ("list-inside", "list-style-position: inside", "符号在盒内"),
    ("list-outside", "list-style-position: outside", "符号在盒外"),
], preview="text", demo="list-inside list-disc")

util("list-style-type", "list-style-type", "列表符号类型。Preflight 会去掉默认符号，需要时再加回来。", TY, "list-style-type", [
    ("list-none", "list-style-type: none", "无符号"),
    ("list-disc", "disc", "实心圆"),
    ("list-decimal", "decimal", "数字"),
], extra=[code("html", '<ul class="list-disc pl-5"><li>文档</li><li>演练场</li></ul>')],
    preview="text", demo="list-disc pl-5")

util("text-align", "text-align", "文本对齐。逻辑对齐使用 text-start 和 text-end。", TY, "text-align", [
    ("text-left", "text-align: left", "左对齐"),
    ("text-center", "text-align: center", "居中"),
    ("text-right", "text-align: right", "右对齐"),
    ("text-justify", "text-align: justify", "两端对齐"),
    ("text-start", "text-align: start", "跟随书写方向"),
    ("text-end", "text-align: end", "跟随书写方向的末端"),
], preview="text", demo="text-center")

util("color", "color", "文字颜色。深色模式请成对写上 dark: 变体，并保证对比度。", TY, "color", [
    ("text-gray-950", "近黑", "浅色主题主文字"),
    ("text-gray-600", "中灰", "次要文字下限"),
    ("text-white", "白色", "深色背景上的文字"),
    ("text-sky-500", "品牌青", "链接与强调"),
    ("text-transparent", "透明", "配合背景裁切做渐变字"),
], preview="text", demo="text-sky-600 font-semibold")

util("text-decoration-line", "text-decoration-line", "下划线、删除线和上划线。", TY, "text-decoration-line", [
    ("underline", "underline", "下划线"),
    ("overline", "overline", "上划线"),
    ("line-through", "line-through", "删除线"),
    ("no-underline", "none", "去掉装饰线"),
], preview="text", demo="underline")

util("text-decoration-color", "text-decoration-color", "装饰线的颜色，可与文字颜色不同。", TY, "text-decoration-color", [
    ("decoration-sky-500", "sky-500", "品牌色下划线"),
    ("decoration-inherit", "inherit", "跟随文字"),
], preview="text", demo="underline decoration-sky-500")

util("text-decoration-style", "text-decoration-style", "装饰线样式。", TY, "text-decoration-style", [
    ("decoration-solid", "solid", "实线"),
    ("decoration-double", "double", "双线"),
    ("decoration-dotted", "dotted", "点线"),
    ("decoration-dashed", "dashed", "虚线"),
    ("decoration-wavy", "wavy", "波浪线"),
], preview="text", demo="underline decoration-wavy")

util("text-decoration-thickness", "text-decoration-thickness", "装饰线粗细。", TY, "text-decoration-thickness", [
    ("decoration-1", "1px", "细"),
    ("decoration-2", "2px", "常规强调"),
    ("decoration-4", "4px", "很粗"),
    ("decoration-auto", "auto", "浏览器默认"),
], preview="text", demo="underline decoration-2")

util("text-underline-offset", "text-underline-offset", "下划线与文字基线的距离。", TY, "text-underline-offset", [
    ("underline-offset-2", "2px", "略微离开文字"),
    ("underline-offset-4", "4px", "更疏"),
    ("underline-offset-auto", "auto", "自动"),
], preview="text", demo="underline underline-offset-4")

util("text-transform", "text-transform", "大小写转换。对中文没有视觉影响。", TY, "text-transform", [
    ("uppercase", "uppercase", "全大写"),
    ("lowercase", "lowercase", "全小写"),
    ("capitalize", "capitalize", "单词首字母大写"),
    ("normal-case", "none", "保持原样"),
], preview="text", demo="uppercase tracking-wide")

util("text-overflow", "text-overflow", "单行溢出时如何提示被截断。需要同时限制宽度并设置 whitespace 和 overflow。", TY, "text-overflow", [
    ("truncate", "overflow hidden + ellipsis + nowrap", "单行省略"),
    ("text-ellipsis", "text-overflow: ellipsis", "省略号"),
    ("text-clip", "text-overflow: clip", "直接裁切"),
], preview="text", demo="truncate max-w-40")

util("text-wrap", "text-wrap", "控制换行平衡，避免标题最后一行只剩一个词。", TY, "text-wrap", [
    ("text-wrap", "text-wrap: wrap", "正常换行"),
    ("text-nowrap", "text-wrap: nowrap", "不换行"),
    ("text-balance", "text-wrap: balance", "标题行长更均匀"),
    ("text-pretty", "text-wrap: pretty", "减少孤词"),
], preview="text", demo="text-balance")

util("text-indent", "text-indent", "段落首行缩进。中文排版有时会用两个字宽。", TY, "text-indent", [
    ("indent-0", "0", "不缩进"),
    ("indent-4", "1rem", "轻微缩进"),
    ("indent-8", "2rem", "约两个汉字的视觉宽度"),
], preview="text", demo="indent-8")

util("tab-size", "tab-size", "制表符等于多少个空格，影响代码对齐。", TY, "tab-size", [
    ("tab-0", "tab-size: 0? 实际为较小值", "少用"),
    ("tab-2? 请使用任意值", "tab-size", "默认通常是 4 或 8"),
], extra=[p("需要精确控制时写 tab-[2] 或 tab-[4]。代码块更常见的做法是直接把缩进转成空格。")], preview="text", demo="font-mono")

util("vertical-align", "vertical-align", "行内或表格单元格的垂直对齐。", TY, "vertical-align", [
    ("align-baseline", "baseline", "基线"),
    ("align-top", "top", "顶部"),
    ("align-middle", "middle", "中部"),
    ("align-bottom", "bottom", "底部"),
    ("align-text-top", "text-top", "相对文字顶部"),
], preview="text", demo="align-middle")

util("white-space", "white-space", "空白与换行的处理方式。", TY, "white-space", [
    ("whitespace-normal", "normal", "合并空白并换行"),
    ("whitespace-nowrap", "nowrap", "不换行"),
    ("whitespace-pre", "pre", "保留空白，不自动换行"),
    ("whitespace-pre-line", "pre-line", "保留换行，合并空格"),
    ("whitespace-pre-wrap", "pre-wrap", "保留空白且可换行"),
], preview="text", demo="whitespace-nowrap")

util("word-break", "word-break", "长串字符（URL、哈希）如何断开。", TY, "word-break", [
    ("break-normal", "normal", "默认规则"),
    ("break-all", "break-all", "任意字符处可断"),
    ("break-keep", "keep-all", "中日韩文字尽量不拆开"),
], preview="text", demo="break-all")

util("overflow-wrap", "overflow-wrap", "当一个词太长时，允许在单词内部换行以免撑破容器。", TY, "overflow-wrap", [
    ("wrap-break-word", "overflow-wrap: break-word", "必要时断开长词"),
    ("wrap-anywhere", "overflow-wrap: anywhere", "更积极地断开"),
], preview="text", demo="wrap-break-word")

util("hyphens", "hyphens", "是否自动插入连字符。需要 lang 属性，中文通常不必开启。", TY, "hyphens", [
    ("hyphens-none", "hyphens: none", "不连字符"),
    ("hyphens-manual", "hyphens: manual", "只在软连字符处"),
    ("hyphens-auto", "hyphens: auto", "浏览器自动处理"),
], preview="text", demo="hyphens-manual")

util("content", "content", "为 ::before 和 ::after 设置内容。在 Tailwind 里通常写成 before:content-['文本']。", TY, "content", [
    ("content-none", "content: none", "不生成内容"),
    ("before:content-['']", "content: ''", "空内容，用来画装饰"),
], extra=[
    p("伪元素还需要 before: 或 after: 变体，以及绝对定位、块级显示等类，装饰才会出现。"),
    code("html", '<span class="before:mr-1 before:text-sky-500 before:content-[\'→\']">下一步</span>'),
], preview="text", demo="before:content-['→'] before:mr-1")

BG = "背景"
add_group(BG, [
    {"title": "background-attachment", "slug": "background-attachment"},
    {"title": "background-clip", "slug": "background-clip"},
    {"title": "background-color", "slug": "background-color"},
    {"title": "background-image", "slug": "background-image"},
    {"title": "background-origin", "slug": "background-origin"},
    {"title": "background-position", "slug": "background-position"},
    {"title": "background-repeat", "slug": "background-repeat"},
    {"title": "background-size", "slug": "background-size"},
])

util("background-attachment", "background-attachment", "背景随内容滚动，还是相对视口固定。", BG, "background-attachment", [
    ("bg-fixed", "fixed", "相对视口固定"),
    ("bg-local", "local", "随元素内容滚动"),
    ("bg-scroll", "scroll", "随页面滚动"),
], preview="box", demo="bg-fixed")

util("background-clip", "background-clip", "背景绘制到边框盒、内边距盒还是文字形状。", BG, "background-clip", [
    ("bg-clip-border", "border-box", "含边框"),
    ("bg-clip-padding", "padding-box", "不含边框"),
    ("bg-clip-content", "content-box", "只在内容区"),
    ("bg-clip-text", "text", "裁成文字，配合透明文字色做渐变字"),
], preview="text", demo="bg-gradient-to-r from-sky-500 to-indigo-500 bg-clip-text text-transparent font-semibold")

util("background-color", "background-color", "背景色。透明度写在颜色后面，如 bg-black/50。", BG, "background-color", [
    ("bg-white", "白色", "卡片"),
    ("bg-gray-950", "近黑", "深色页面"),
    ("bg-sky-500", "品牌青", "主按钮"),
    ("bg-transparent", "透明", "幽灵按钮"),
    ("bg-black/5", "5% 黑", "浅色悬停底"),
], preview="color", demo="bg-sky-500")

util("background-image", "background-image", "渐变、网格和自定义图片都从这里开始。", BG, "background-image", [
    ("bg-none", "none", "无背景图"),
    ("bg-gradient-to-r", "向右线性渐变", "配合 from / via / to"),
    ("bg-gradient-to-br", "向右下", "封面常用"),
    ("bg-[url(...)]", "任意图片", "一次性图片地址"),
], extra=[code("html", '<div class="h-24 bg-gradient-to-r from-sky-400 to-fuchsia-500"></div>')],
    preview="color", demo="bg-gradient-to-r from-sky-400 to-indigo-500")

util("background-origin", "background-origin", "背景图定位的参考盒。", BG, "background-origin", [
    ("bg-origin-border", "border-box", "从边框外沿算"),
    ("bg-origin-padding", "padding-box", "从内边距外沿算"),
    ("bg-origin-content", "content-box", "从内容区算"),
], preview="box", demo="bg-origin-content")

util("background-position", "background-position", "背景图的位置。", BG, "background-position", [
    ("bg-center", "center", "居中"),
    ("bg-top", "top", "顶部"),
    ("bg-bottom", "bottom", "底部"),
    ("bg-left", "left", "左侧"),
    ("bg-right", "right", "右侧"),
], preview="box", demo="bg-center")

util("background-repeat", "background-repeat", "背景图是否重复。", BG, "background-repeat", [
    ("bg-repeat", "repeat", "双向重复"),
    ("bg-no-repeat", "no-repeat", "不重复"),
    ("bg-repeat-x", "repeat-x", "横向重复"),
    ("bg-repeat-y", "repeat-y", "纵向重复"),
], preview="box", demo="bg-no-repeat")

util("background-size", "background-size", "背景图尺寸。", BG, "background-size", [
    ("bg-auto", "auto", "原始尺寸"),
    ("bg-cover", "cover", "铺满，可能裁切"),
    ("bg-contain", "contain", "完整放入"),
], preview="box", demo="bg-cover")

BD = "边框"
add_group(BD, [
    {"title": "border-radius", "slug": "border-radius"},
    {"title": "border-width", "slug": "border-width"},
    {"title": "border-color", "slug": "border-color"},
    {"title": "border-style", "slug": "border-style"},
    {"title": "outline-width", "slug": "outline-width"},
    {"title": "outline-color", "slug": "outline-color"},
    {"title": "outline-style", "slug": "outline-style"},
    {"title": "outline-offset", "slug": "outline-offset"},
])

util("border-radius", "border-radius", "圆角。v4 里更小的一档是 rounded-xs。", BD, "border-radius", [
    ("rounded-none", "0", "直角"),
    ("rounded-sm", "0.25rem", "小圆角"),
    ("rounded-md", "0.375rem", "输入框"),
    ("rounded-lg", "0.5rem", "卡片内元素"),
    ("rounded-xl", "0.75rem", "卡片"),
    ("rounded-2xl", "1rem", "大卡片"),
    ("rounded-full", "9999px", "胶囊与头像"),
], preview="rounded", demo="rounded-2xl bg-sky-500")

util("border-width", "border-width", "边框宽度。未设置颜色时，Preflight 往往已给出 currentColor 或默认灰。", BD, "border-width", [
    ("border", "1px", "四边"),
    ("border-2", "2px", "更明显"),
    ("border-0", "0", "去掉"),
    ("border-x", "左右", "分隔竖线"),
    ("border-y", "上下", "分隔横线"),
    ("border-t", "上", "顶栏底边常用"),
], preview="border", demo="border border-gray-300")

util("border-color", "border-color", "边框颜色。浅色用 gray-200，深色用 white/10。", BD, "border-color", [
    ("border-gray-200", "浅灰", "浅色主题分隔"),
    ("border-white/10", "10% 白", "深色主题分隔"),
    ("border-sky-400", "品牌青", "强调边"),
    ("border-transparent", "透明", "占位，避免悬停时布局跳动"),
], preview="border", demo="border-2 border-sky-500")

util("border-style", "border-style", "边框线型。", BD, "border-style", [
    ("border-solid", "solid", "实线，默认"),
    ("border-dashed", "dashed", "虚线"),
    ("border-dotted", "dotted", "点线"),
    ("border-double", "double", "双线"),
    ("border-none", "none", "无线型"),
], preview="border", demo="border-2 border-dashed border-gray-400")

util("outline-width", "outline-width", "轮廓不占布局空间，适合焦点环。", BD, "outline-width", [
    ("outline-0", "0", "无轮廓"),
    ("outline-1", "1px", "细环"),
    ("outline-2", "2px", "键盘焦点推荐"),
    ("outline-4", "4px", "很醒目"),
], preview="border", demo="outline-2 outline-sky-500 outline-offset-2")

util("outline-color", "outline-color", "轮廓颜色。", BD, "outline-color", [
    ("outline-sky-500", "品牌青", "焦点"),
    ("outline-black", "黑", "高对比"),
    ("outline-transparent", "透明", "占位"),
], preview="border", demo="outline outline-sky-500")

util("outline-style", "outline-style", "轮廓线型。v4 中若要恢复旧的 outline-none 行为，使用 outline-hidden。", BD, "outline-style", [
    ("outline-solid", "solid", "实线"),
    ("outline-dashed", "dashed", "虚线"),
    ("outline-dotted", "dotted", "点线"),
    ("outline-none", "none", "去掉轮廓样式"),
    ("outline-hidden", "对辅助技术更安全的隐藏", "替代 v3 的 outline-none"),
], preview="border", demo="outline-dashed")

util("outline-offset", "outline-offset", "轮廓与边框之间的空隙。", BD, "outline-offset", [
    ("outline-offset-0", "0", "贴着边框"),
    ("outline-offset-2", "2px", "常用焦点间距"),
    ("outline-offset-4", "4px", "更远"),
], preview="border", demo="outline-2 outline-offset-4 outline-sky-500")

EF = "效果"
add_group(EF, [
    {"title": "box-shadow", "slug": "box-shadow"},
    {"title": "text-shadow", "slug": "text-shadow"},
    {"title": "opacity", "slug": "opacity"},
    {"title": "mix-blend-mode", "slug": "mix-blend-mode"},
    {"title": "background-blend-mode", "slug": "background-blend-mode"},
    {"title": "mask-clip", "slug": "mask-clip"},
    {"title": "mask-composite", "slug": "mask-composite"},
    {"title": "mask-image", "slug": "mask-image"},
    {"title": "mask-mode", "slug": "mask-mode"},
    {"title": "mask-origin", "slug": "mask-origin"},
    {"title": "mask-position", "slug": "mask-position"},
    {"title": "mask-repeat", "slug": "mask-repeat"},
    {"title": "mask-size", "slug": "mask-size"},
    {"title": "mask-type", "slug": "mask-type"},
])

util("box-shadow", "box-shadow", "盒阴影用来抬起卡片。悬停时改变阴影，不要用会挤占布局的缩放。", EF, "box-shadow", [
    ("shadow-xs", "很轻", "输入框"),
    ("shadow-sm", "轻", "按钮"),
    ("shadow-md", "中等", "菜单"),
    ("shadow-lg", "较重", "弹层"),
    ("shadow-xl", "重", "封面"),
    ("shadow-none", "无", "去掉阴影"),
], preview="shadow", demo="shadow-xl rounded-2xl bg-white")

util("text-shadow", "text-shadow", "文字阴影。v4 提供了与盒阴影类似的刻度。", EF, "text-shadow", [
    ("text-shadow-2xs", "极轻", "提高浅色字可读性"),
    ("text-shadow-sm", "轻", "图片上的标题"),
    ("text-shadow-md", "中", "海报标题"),
    ("text-shadow-none", "无", "去掉"),
], preview="text", demo="text-shadow-md text-white")

util("opacity", "opacity", "整个元素及其子元素的不透明度。只想让背景半透明时，用颜色斜线语法。", EF, "opacity", [
    ("opacity-0", "0", "完全透明"),
    ("opacity-50", "0.5", "禁用态"),
    ("opacity-75", "0.75", "次要"),
    ("opacity-100", "1", "不透明"),
], preview="box", demo="opacity-50 bg-sky-500")

util("mix-blend-mode", "mix-blend-mode", "元素与背后内容的混合方式。", EF, "mix-blend-mode", [
    ("mix-blend-normal", "normal", "正常"),
    ("mix-blend-multiply", "multiply", "正片叠底"),
    ("mix-blend-screen", "screen", "滤色"),
    ("mix-blend-overlay", "overlay", "叠加"),
], preview="box", demo="mix-blend-multiply")

util("background-blend-mode", "background-blend-mode", "同一元素上多个背景层如何混合。", EF, "background-blend-mode", [
    ("bg-blend-normal", "normal", "正常"),
    ("bg-blend-multiply", "multiply", "正片叠底"),
    ("bg-blend-overlay", "overlay", "叠加"),
    ("bg-blend-darken", "darken", "变暗"),
], preview="color", demo="bg-blend-multiply")

for slug, title, summary, prop, rows in [
    ("mask-clip", "mask-clip", "蒙版裁切参考的盒子。", "mask-clip", [("mask-clip-border", "border-box", "边框盒"), ("mask-clip-padding", "padding-box", "内边距盒"), ("mask-clip-content", "content-box", "内容盒")]),
    ("mask-composite", "mask-composite", "多个蒙版如何合成。", "mask-composite", [("mask-add", "add", "相加"), ("mask-subtract", "subtract", "相减"), ("mask-intersect", "intersect", "相交"), ("mask-exclude", "exclude", "排除")]),
    ("mask-image", "mask-image", "用渐变或图片作为蒙版。", "mask-image", [("mask-none", "none", "无蒙版"), ("mask-[linear-gradient(...)]", "任意渐变", "做边缘淡出")]),
    ("mask-mode", "mask-mode", "蒙版按亮度还是按透明度计算。", "mask-mode", [("mask-luminance", "luminance", "亮度"), ("mask-alpha", "alpha", "透明度")]),
    ("mask-origin", "mask-origin", "蒙版定位的参考盒。", "mask-origin", [("mask-origin-border", "border-box", "边框"), ("mask-origin-padding", "padding-box", "内边距"), ("mask-origin-content", "content-box", "内容")]),
    ("mask-position", "mask-position", "蒙版位置。", "mask-position", [("mask-top", "top", "顶部"), ("mask-center", "center", "居中"), ("mask-bottom", "bottom", "底部")]),
    ("mask-repeat", "mask-repeat", "蒙版是否重复。", "mask-repeat", [("mask-repeat", "repeat", "重复"), ("mask-no-repeat", "no-repeat", "不重复")]),
    ("mask-size", "mask-size", "蒙版尺寸。", "mask-size", [("mask-cover? 使用任意值", "cover / contain", "与背景尺寸类似"), ("mask-auto 概念", "auto", "原始尺寸")]),
    ("mask-type", "mask-type", "SVG 蒙版类型。", "mask-type", [("mask-type-alpha", "alpha", "透明度"), ("mask-type-luminance", "luminance", "亮度")]),
]:
    util(slug, title, summary, EF, prop, rows, preview="box")

FL = "滤镜"
add_group(FL, [
    {"title": "filter", "slug": "filter"},
    {"title": "blur", "slug": "filter-blur"},
    {"title": "brightness", "slug": "filter-brightness"},
    {"title": "contrast", "slug": "filter-contrast"},
    {"title": "drop-shadow", "slug": "filter-drop-shadow"},
    {"title": "grayscale", "slug": "filter-grayscale"},
    {"title": "hue-rotate", "slug": "filter-hue-rotate"},
    {"title": "invert", "slug": "filter-invert"},
    {"title": "saturate", "slug": "filter-saturate"},
    {"title": "sepia", "slug": "filter-sepia"},
    {"title": "backdrop-filter", "slug": "backdrop-filter"},
    {"title": "backdrop blur", "slug": "backdrop-filter-blur"},
    {"title": "backdrop brightness", "slug": "backdrop-filter-brightness"},
    {"title": "backdrop contrast", "slug": "backdrop-filter-contrast"},
    {"title": "backdrop grayscale", "slug": "backdrop-filter-grayscale"},
    {"title": "backdrop hue-rotate", "slug": "backdrop-filter-hue-rotate"},
    {"title": "backdrop invert", "slug": "backdrop-filter-invert"},
    {"title": "backdrop opacity", "slug": "backdrop-filter-opacity"},
    {"title": "backdrop saturate", "slug": "backdrop-filter-saturate"},
    {"title": "backdrop sepia", "slug": "backdrop-filter-sepia"},
])

util("filter", "filter", "滤镜类可以叠加。none 用来关掉元素自身的滤镜。", FL, "filter", [
    ("filter-none", "filter: none", "清除滤镜"),
    ("blur-sm", "blur(4px)", "可与其他滤镜并存"),
    ("grayscale", "grayscale(100%)", "去色"),
], preview="filter", demo="grayscale")

util("filter-blur", "blur", "高斯模糊。数值越大越糊。", FL, "filter: blur()", [
    ("blur-none", "0", "清晰"),
    ("blur-xs", "4px", "很轻"),
    ("blur-sm", "8px", "轻"),
    ("blur-md", "12px", "中"),
    ("blur-lg", "16px", "强"),
    ("blur-xl", "24px", "很强"),
    ("blur-3xl", "64px", "极强"),
], preview="filter", demo="blur-md")

util("filter-brightness", "brightness", "亮度倍率。100 是原始亮度。", FL, "filter: brightness()", [
    ("brightness-50", "0.5", "变暗"),
    ("brightness-100", "1", "原始"),
    ("brightness-125", "1.25", "略亮"),
    ("brightness-150", "1.5", "很亮"),
], preview="filter", demo="brightness-125")

util("filter-contrast", "contrast", "对比度倍率。", FL, "filter: contrast()", [
    ("contrast-50", "0.5", "发灰"),
    ("contrast-100", "1", "原始"),
    ("contrast-150", "1.5", "更利落"),
], preview="filter", demo="contrast-150")

util("filter-drop-shadow", "drop-shadow", "沿元素不透明轮廓投影，适合图标和透明 PNG。", FL, "filter: drop-shadow()", [
    ("drop-shadow-sm", "轻投影", "小图标"),
    ("drop-shadow-md", "中投影", "浮动图标"),
    ("drop-shadow-xl", "重投影", "强调"),
    ("drop-shadow-none", "无", "去掉"),
], preview="filter", demo="drop-shadow-xl")

util("filter-grayscale", "grayscale", "去色比例。", FL, "filter: grayscale()", [
    ("grayscale-0", "0", "彩色"),
    ("grayscale", "100%", "完全灰"),
], preview="filter", demo="grayscale")

util("filter-hue-rotate", "hue-rotate", "在色相环上旋转颜色。", FL, "filter: hue-rotate()", [
    ("hue-rotate-0", "0deg", "原色"),
    ("hue-rotate-15", "15deg", "略偏"),
    ("hue-rotate-90", "90deg", "明显变色"),
    ("hue-rotate-180", "180deg", "对侧色"),
], preview="filter", demo="hue-rotate-90")

util("filter-invert", "invert", "颜色反相。", FL, "filter: invert()", [
    ("invert-0", "0", "正常"),
    ("invert", "100%", "反相"),
], preview="filter", demo="invert")

util("filter-saturate", "saturate", "饱和度。", FL, "filter: saturate()", [
    ("saturate-0", "0", "灰"),
    ("saturate-100", "1", "原始"),
    ("saturate-150", "1.5", "更艳"),
    ("saturate-200", "2", "很艳"),
], preview="filter", demo="saturate-200")

util("filter-sepia", "sepia", "棕褐色。", FL, "filter: sepia()", [
    ("sepia-0", "0", "无"),
    ("sepia", "100%", "全棕褐"),
], preview="filter", demo="sepia")

util("backdrop-filter", "backdrop-filter", "模糊或染色元素背后的内容。元素自身需要半透明背景才能看见效果。", FL, "backdrop-filter", [
    ("backdrop-filter-none", "none", "关闭"),
    ("backdrop-blur-md", "blur(12px)", "毛玻璃"),
], extra=[p("顶栏就是半透明背景加上 backdrop-blur。请保证背后真的有内容，否则看不出滤镜。")],
    preview="backdrop", demo="backdrop-blur-md bg-white/60")

util("backdrop-filter-blur", "backdrop blur", "只模糊元素背后的像素。", FL, "backdrop-filter: blur()", [
    ("backdrop-blur-none", "0", "不模糊"),
    ("backdrop-blur-sm", "8px", "轻"),
    ("backdrop-blur-md", "12px", "导航常用"),
    ("backdrop-blur-xl", "24px", "强"),
], preview="backdrop", demo="backdrop-blur-md bg-white/50")

util("backdrop-filter-brightness", "backdrop brightness", "调整背后内容的亮度。", FL, "backdrop-filter: brightness()", [
    ("backdrop-brightness-50", "0.5", "压暗背后"),
    ("backdrop-brightness-100", "1", "不变"),
    ("backdrop-brightness-125", "1.25", "提亮背后"),
], preview="backdrop", demo="backdrop-brightness-125 bg-white/40")

util("backdrop-filter-contrast", "backdrop contrast", "调整背后内容的对比度。", FL, "backdrop-filter: contrast()", [
    ("backdrop-contrast-50", "0.5", "降低"),
    ("backdrop-contrast-125", "1.25", "提高"),
], preview="backdrop", demo="backdrop-contrast-125 bg-white/40")

util("backdrop-filter-grayscale", "backdrop grayscale", "让背后内容失去颜色。", FL, "backdrop-filter: grayscale()", [
    ("backdrop-grayscale-0", "0", "保持彩色"),
    ("backdrop-grayscale", "100%", "背后变灰"),
], preview="backdrop", demo="backdrop-grayscale bg-white/40")

util("backdrop-filter-hue-rotate", "backdrop hue-rotate", "旋转背后内容的色相。", FL, "backdrop-filter: hue-rotate()", [
    ("backdrop-hue-rotate-0", "0deg", "不变"),
    ("backdrop-hue-rotate-90", "90deg", "明显偏色"),
], preview="backdrop", demo="backdrop-hue-rotate-90 bg-white/40")

util("backdrop-filter-invert", "backdrop invert", "反相背后的内容。", FL, "backdrop-filter: invert()", [
    ("backdrop-invert-0", "0", "正常"),
    ("backdrop-invert", "100%", "反相"),
], preview="backdrop", demo="backdrop-invert bg-white/30")

util("backdrop-filter-opacity", "backdrop opacity", "降低背后内容的不透明度。", FL, "backdrop-filter: opacity()", [
    ("backdrop-opacity-50", "0.5", "背后变淡"),
    ("backdrop-opacity-100", "1", "不变"),
], preview="backdrop", demo="backdrop-opacity-80 bg-white/40")

util("backdrop-filter-saturate", "backdrop saturate", "调整背后内容的饱和度。毛玻璃上略微提高饱和度会更通透。", FL, "backdrop-filter: saturate()", [
    ("backdrop-saturate-50", "0.5", "变淡"),
    ("backdrop-saturate-150", "1.5", "更鲜"),
], preview="backdrop", demo="backdrop-saturate-150 bg-white/40")

util("backdrop-filter-sepia", "backdrop sepia", "给背后内容加上棕褐色。", FL, "backdrop-filter: sepia()", [
    ("backdrop-sepia-0", "0", "无"),
    ("backdrop-sepia", "100%", "全棕褐"),
], preview="backdrop", demo="backdrop-sepia bg-white/40")

TB = "表格"
add_group(TB, [
    {"title": "border-collapse", "slug": "border-collapse"},
    {"title": "border-spacing", "slug": "border-spacing"},
    {"title": "table-layout", "slug": "table-layout"},
    {"title": "caption-side", "slug": "caption-side"},
])

util("border-collapse", "border-collapse", "相邻单元格边框合并还是分离。", TB, "border-collapse", [
    ("border-collapse", "collapse", "合并成一条线"),
    ("border-separate", "separate", "各自保留边框"),
], preview="table", demo="border-collapse")

util("border-spacing", "border-spacing", "分离边框模式下，单元格之间的距离。", TB, "border-spacing", [
    ("border-spacing-0", "0", "贴紧"),
    ("border-spacing-2", "0.5rem", "略微分开"),
    ("border-spacing-4", "1rem", "明显分开"),
], preview="table", demo="border-separate border-spacing-2")

util("table-layout", "table-layout", "列宽按内容计算，还是按表格宽度平均分配。", TB, "table-layout", [
    ("table-auto", "auto", "按内容"),
    ("table-fixed", "fixed", "按第一行或 col 分配，更稳定"),
], preview="table", demo="table-fixed")

util("caption-side", "caption-side", "表格标题在表上方还是下方。", TB, "caption-side", [
    ("caption-top", "top", "标题在上"),
    ("caption-bottom", "bottom", "标题在下"),
], preview="table", demo="caption-bottom")

AN = "过渡与动画"
add_group(AN, [
    {"title": "transition-property", "slug": "transition-property"},
    {"title": "transition-behavior", "slug": "transition-behavior"},
    {"title": "transition-duration", "slug": "transition-duration"},
    {"title": "transition-timing-function", "slug": "transition-timing-function"},
    {"title": "transition-delay", "slug": "transition-delay"},
    {"title": "animation", "slug": "animation"},
])

util("transition-property", "transition-property", "指定哪些属性参与过渡。颜色过渡是界面里最常用的一种。", AN, "transition-property", [
    ("transition-none", "none", "不过渡"),
    ("transition-all", "all", "所有可过渡属性，慎用"),
    ("transition-colors", "颜色相关", "悬停换色"),
    ("transition-opacity", "opacity", "淡入淡出"),
    ("transition-transform", "transform", "位移旋转"),
    ("transition-shadow", "box-shadow", "抬起卡片"),
], preview="transition", demo="transition-colors")

util("transition-behavior", "transition-behavior", "是否允许离散属性（如 display）参与过渡。", AN, "transition-behavior", [
    ("transition-normal", "normal", "默认"),
    ("transition-discrete", "allow-discrete", "配合 starting 样式做进入动画"),
], preview="transition", demo="transition-discrete")

util("transition-duration", "transition-duration", "过渡时长。界面反馈保持在 150 到 300 毫秒。", AN, "transition-duration", [
    ("duration-75", "75ms", "极快"),
    ("duration-150", "150ms", "按钮"),
    ("duration-200", "200ms", "本站默认交互"),
    ("duration-300", "300ms", "面板"),
    ("duration-700", "700ms", "演示用慢动作"),
    ("duration-1000", "1000ms", "很长，日常界面避免"),
], preview="transition", demo="duration-300")

util("transition-timing-function", "transition-timing-function", "速度曲线。", AN, "transition-timing-function", [
    ("ease-linear", "linear", "匀速"),
    ("ease-in", "ease-in", "慢起步"),
    ("ease-out", "ease-out", "快起步，界面首选"),
    ("ease-in-out", "ease-in-out", "两端慢"),
], preview="transition", demo="ease-out")

util("transition-delay", "transition-delay", "过渡开始前的等待。", AN, "transition-delay", [
    ("delay-0", "0ms", "立即"),
    ("delay-75", "75ms", "很短"),
    ("delay-150", "150ms", "错开列表"),
    ("delay-300", "300ms", "明显等待"),
], preview="transition", demo="delay-150")

util("animation", "animation", "内置关键帧动画。尊重 prefers-reduced-motion，必要时提供关闭动画的状态。", AN, "animation", [
    ("animate-none", "none", "停止"),
    ("animate-spin", "spin 1s linear infinite", "加载指示"),
    ("animate-ping", "ping", "提示点"),
    ("animate-pulse", "pulse", "骨架屏"),
    ("animate-bounce", "bounce", "引导注意，少用"),
], preview="transition", demo="animate-pulse")

TF = "变换"
add_group(TF, [
    {"title": "backface-visibility", "slug": "backface-visibility"},
    {"title": "perspective", "slug": "perspective"},
    {"title": "perspective-origin", "slug": "perspective-origin"},
    {"title": "rotate", "slug": "rotate"},
    {"title": "scale", "slug": "scale"},
    {"title": "skew", "slug": "skew"},
    {"title": "transform", "slug": "transform"},
    {"title": "transform-origin", "slug": "transform-origin"},
    {"title": "transform-style", "slug": "transform-style"},
    {"title": "translate", "slug": "translate"},
    {"title": "zoom", "slug": "zoom"},
])

util("backface-visibility", "backface-visibility", "3D 翻转时，元素背面是否可见。", TF, "backface-visibility", [
    ("backface-visible", "visible", "看得见背面"),
    ("backface-hidden", "hidden", "翻转卡片时隐藏背面"),
], preview="transform", demo="backface-hidden")

util("perspective", "perspective", "父元素的透视距离。数值越小，3D 越夸张。", TF, "perspective", [
    ("perspective-none", "none", "无透视"),
    ("perspective-distant", "1200px", "平缓"),
    ("perspective-normal", "500px", "常规"),
    ("perspective-near", "300px", "强烈"),
], preview="transform", demo="perspective-normal")

util("perspective-origin", "perspective-origin", "透视消失点的位置。", TF, "perspective-origin", [
    ("perspective-origin-center", "center", "中心"),
    ("perspective-origin-top", "top", "上方"),
    ("perspective-origin-bottom", "bottom", "下方"),
], preview="transform", demo="perspective-origin-center")

util("rotate", "rotate", "旋转。3D 使用 rotate-x、rotate-y 和 rotate-z。", TF, "rotate", [
    ("rotate-0", "0deg", "不旋转"),
    ("rotate-45", "45deg", "菱形"),
    ("rotate-90", "90deg", "顺时针 90 度"),
    ("rotate-180", "180deg", "上下颠倒"),
    ("-rotate-6", "-6deg", "轻微倾斜"),
], preview="transform", demo="rotate-6")

util("scale", "scale", "缩放。悬停放大容易引起布局抖动，优先用颜色和阴影反馈。", TF, "scale", [
    ("scale-0", "0", "缩成一点"),
    ("scale-95", "0.95", "按下反馈"),
    ("scale-100", "1", "原始"),
    ("scale-105", "1.05", "轻微放大"),
    ("scale-x-110", "scaleX(1.1)", "只拉宽"),
], preview="transform", demo="scale-110")

util("skew", "skew", "倾斜。适合装饰条，不适合正文。", TF, "skew", [
    ("skew-x-0", "skewX(0)", "不倾斜"),
    ("skew-x-6", "skewX(6deg)", "横向轻斜"),
    ("skew-y-3", "skewY(3deg)", "纵向轻斜"),
    ("-skew-x-12", "skewX(-12deg)", "反向"),
], preview="transform", demo="skew-x-6")

util("transform", "transform", "GPU 友好的变换总开关。单独的 rotate、scale、translate 类已经会启用变换。", TF, "transform", [
    ("transform-none", "none", "清除变换"),
    ("transform-gpu", "translate3d(0,0,0)", "强制独立图层，谨慎使用"),
], preview="transform", demo="transform-none")

util("transform-origin", "transform-origin", "旋转和缩放的原点。", TF, "transform-origin", [
    ("origin-center", "center", "中心"),
    ("origin-top", "top", "上边"),
    ("origin-bottom-left", "bottom left", "左下角"),
    ("origin-top-right", "top right", "右上角"),
], preview="transform", demo="origin-top-left rotate-6")

util("transform-style", "transform-style", "子元素是在 3D 空间里渲染，还是被拍扁到父元素平面。", TF, "transform-style", [
    ("transform-flat", "flat", "拍平"),
    ("transform-3d", "preserve-3d", "保留三维，翻转卡片需要它"),
], preview="transform", demo="transform-3d")

util("translate", "translate", "平移，不改变文档流占位。居中绝对定位元素时很常用。", TF, "translate", [
    ("translate-x-0", "translateX(0)", "不移动"),
    ("translate-x-4", "1rem", "向右"),
    ("-translate-y-1", "-0.25rem", "略微上浮"),
    ("translate-x-1/2", "50%", "自身宽度的一半"),
    ("-translate-x-1/2", "-50%", "配合 left-1/2 水平居中"),
], preview="transform", demo="-translate-y-1")

util("zoom", "zoom", "CSS zoom。它会影响布局，和 transform: scale 不同。", TF, "zoom", [
    ("zoom-100", "1? 使用 zoom-100 表示原始", "原始"),
    ("zoom-110", "1.1", "放大并占更多空间"),
    ("zoom-90", "0.9", "缩小"),
], extra=[p("如果只是视觉放大且不想撑开邻居，用 scale-110。zoom 会改变元素参与布局的尺寸。")], preview="transform", demo="scale-105")

IT = "交互"
add_group(IT, [
    {"title": "accent-color", "slug": "accent-color"},
    {"title": "appearance", "slug": "appearance"},
    {"title": "caret-color", "slug": "caret-color"},
    {"title": "color-scheme", "slug": "color-scheme"},
    {"title": "cursor", "slug": "cursor"},
    {"title": "field-sizing", "slug": "field-sizing"},
    {"title": "pointer-events", "slug": "pointer-events"},
    {"title": "resize", "slug": "resize"},
    {"title": "scroll-behavior", "slug": "scroll-behavior"},
    {"title": "scrollbar-color", "slug": "scrollbar-color"},
    {"title": "scrollbar-width", "slug": "scrollbar-width"},
    {"title": "scrollbar-gutter", "slug": "scrollbar-gutter"},
    {"title": "scroll-margin", "slug": "scroll-margin"},
    {"title": "scroll-padding", "slug": "scroll-padding"},
    {"title": "scroll-snap-align", "slug": "scroll-snap-align"},
    {"title": "scroll-snap-stop", "slug": "scroll-snap-stop"},
    {"title": "scroll-snap-type", "slug": "scroll-snap-type"},
    {"title": "touch-action", "slug": "touch-action"},
    {"title": "user-select", "slug": "user-select"},
    {"title": "will-change", "slug": "will-change"},
])

util("accent-color", "accent-color", "复选框、单选框和范围输入的强调色。", IT, "accent-color", [
    ("accent-auto", "auto", "浏览器默认"),
    ("accent-sky-500", "sky-500", "品牌色控件"),
    ("accent-indigo-600", "indigo-600", "另一种强调"),
], preview="text", demo="accent-sky-500")

util("appearance", "appearance", "是否使用浏览器原生外观。", IT, "appearance", [
    ("appearance-none", "none", "去掉原生样式，便于自定义"),
    ("appearance-auto", "auto", "恢复原生"),
], preview="text", demo="appearance-none")

util("caret-color", "caret-color", "输入框里闪烁光标的颜色。", IT, "caret-color", [
    ("caret-sky-500", "sky-500", "品牌色光标"),
    ("caret-black", "black", "黑色"),
    ("caret-transparent", "transparent", "隐藏光标"),
], preview="text", demo="caret-sky-500")

util("color-scheme", "color-scheme", "告诉浏览器表单控件和滚动条应使用浅色还是深色系统样式。", IT, "color-scheme", [
    ("scheme-light", "light", "浅色控件"),
    ("scheme-dark", "dark", "深色控件"),
    ("scheme-normal", "normal", "跟随页面"),
], preview="box", demo="scheme-dark")

util("cursor", "cursor", "鼠标指针。可点击的按钮、链接和卡片都应使用 pointer。", IT, "cursor", [
    ("cursor-auto", "auto", "自动"),
    ("cursor-pointer", "pointer", "可点击"),
    ("cursor-not-allowed", "not-allowed", "禁用"),
    ("cursor-text", "text", "可选文本"),
    ("cursor-grab", "grab", "可拖拽"),
    ("cursor-wait", "wait", "忙碌"),
], preview="text", demo="cursor-pointer")

util("field-sizing", "field-sizing", "让文本域按内容增高，而不是固定行数。", IT, "field-sizing", [
    ("field-sizing-fixed", "fixed", "固定尺寸"),
    ("field-sizing-content", "content", "随内容增长"),
], preview="text", demo="field-sizing-content")

util("pointer-events", "pointer-events", "元素是否成为指针事件的目标。", IT, "pointer-events", [
    ("pointer-events-none", "none", "点击穿透"),
    ("pointer-events-auto", "auto", "恢复接收"),
], preview="box", demo="pointer-events-none")

util("resize", "resize", "文本域是否允许用户拖拽改变尺寸。", IT, "resize", [
    ("resize-none", "none", "不可调整"),
    ("resize", "both", "双向"),
    ("resize-y", "vertical", "只纵向，文本域常用"),
    ("resize-x", "horizontal", "只横向"),
], preview="text", demo="resize-y")

util("scroll-behavior", "scroll-behavior", "锚点滚动是否平滑。系统要求减少动效时应关闭。", IT, "scroll-behavior", [
    ("scroll-auto", "auto", "瞬间跳转"),
    ("scroll-smooth", "smooth", "平滑滚动"),
], preview="box", demo="scroll-smooth")

util("scrollbar-color", "scrollbar-color", "滚动条滑块和轨道的颜色。", IT, "scrollbar-color", [
    ("scrollbar-auto", "auto? 使用任意值更灵活", "浏览器默认"),
], extra=[p("可以用任意值 scrollbar-[#38bdf8_#e5e7eb] 分别指定滑块和轨道。深色主题里把轨道改成接近背景的颜色。")], preview="box")

util("scrollbar-width", "scrollbar-width", "滚动条粗细。", IT, "scrollbar-width", [
    ("scrollbar-auto", "auto", "默认"),
    ("scrollbar-thin", "thin", "细滚动条"),
    ("scrollbar-none", "none", "隐藏，仍可用滚轮，注意可发现性"),
], preview="box", demo="scrollbar-thin")

util("scrollbar-gutter", "scrollbar-gutter", "是否预留滚动条槽，避免内容在出现滚动条时横向跳动。", IT, "scrollbar-gutter", [
    ("scrollbar-gutter-auto", "auto", "按需"),
    ("scrollbar-gutter-stable", "stable", "始终预留"),
    ("scrollbar-gutter-both", "stable both-edges", "两侧都预留"),
], preview="box", demo="scrollbar-gutter-stable")

util("scroll-margin", "scroll-margin", "锚点滚动后额外留出的外边距，避免标题被粘性顶栏挡住。", IT, "scroll-margin", [
    ("scroll-m-0", "0", "不留"),
    ("scroll-mt-16", "4rem", "避开 64px 顶栏"),
    ("scroll-mt-24", "6rem", "文档标题常用"),
], preview="box", demo="scroll-mt-16")

util("scroll-padding", "scroll-padding", "滚动容器的对齐内边距，影响 scroll-snap 和锚点。", IT, "scroll-padding", [
    ("scroll-p-0", "0", "不留"),
    ("scroll-pt-16", "4rem", "顶部让出顶栏"),
    ("scroll-px-4", "1rem", "左右留白"),
], preview="box", demo="scroll-pt-4")

util("scroll-snap-align", "scroll-snap-align", "子元素停靠到滚动容器的哪个位置。", IT, "scroll-snap-align", [
    ("snap-start", "start", "对齐起始边"),
    ("snap-center", "center", "对齐中心"),
    ("snap-end", "end", "对齐结束边"),
    ("snap-none", "none", "不停靠"),
], preview="box", demo="snap-center")

util("scroll-snap-stop", "scroll-snap-stop", "快速滑动时是否允许跳过中间的停靠点。", IT, "scroll-snap-stop", [
    ("snap-normal", "normal", "可以跳过"),
    ("snap-always", "always", "每项都要停"),
], preview="box", demo="snap-always")

util("scroll-snap-type", "scroll-snap-type", "在滚动容器上开启停靠，并指定轴。", IT, "scroll-snap-type", [
    ("snap-none", "none", "关闭"),
    ("snap-x", "x mandatory", "横向轮播"),
    ("snap-y", "y mandatory", "纵向分页"),
    ("snap-both", "both mandatory", "两轴"),
    ("snap-mandatory", "mandatory", "必须停在点上"),
    ("snap-proximity", "proximity", "接近时才停"),
], preview="box", demo="snap-x snap-mandatory")

util("touch-action", "touch-action", "浏览器如何处理触摸手势，避免和自定义拖拽冲突。", IT, "touch-action", [
    ("touch-auto", "auto", "浏览器处理"),
    ("touch-none", "none", "全部交给脚本"),
    ("touch-pan-x", "pan-x", "只允许横向平移"),
    ("touch-pan-y", "pan-y", "只允许纵向平移"),
    ("touch-manipulation", "manipulation", "去掉双击缩放延迟"),
], preview="box", demo="touch-manipulation")

util("user-select", "user-select", "文字能否被选中。不要为了“好看”禁用正文选择。", IT, "user-select", [
    ("select-none", "none", "不可选，适合拖拽手柄"),
    ("select-text", "text", "可选"),
    ("select-all", "all", "点击即全选"),
    ("select-auto", "auto", "自动"),
], preview="text", demo="select-all")

util("will-change", "will-change", "提示浏览器元素即将变化。只在确实要动画的瞬间使用，不要全局常开。", IT, "will-change", [
    ("will-change-auto", "auto", "不提示"),
    ("will-change-transform", "transform", "即将变换"),
    ("will-change-contents", "contents", "内容将变"),
    ("will-change-scroll", "scroll-position", "即将滚动"),
], preview="box", demo="will-change-transform")

SVG = "SVG"
add_group(SVG, [
    {"title": "fill", "slug": "fill"},
    {"title": "stroke", "slug": "stroke"},
    {"title": "stroke-width", "slug": "stroke-width"},
])

util("fill", "fill", "SVG 形状的填充色。", SVG, "fill", [
    ("fill-none", "none", "不填充"),
    ("fill-current", "currentColor", "跟随文字颜色"),
    ("fill-sky-500", "sky-500", "品牌色"),
    ("fill-transparent", "transparent", "透明"),
], preview="box", demo="fill-sky-500")

util("stroke", "stroke", "SVG 描边颜色。", SVG, "stroke", [
    ("stroke-none", "none", "无描边"),
    ("stroke-current", "currentColor", "跟随文字"),
    ("stroke-gray-950", "近黑", "线图标"),
    ("stroke-sky-500", "品牌青", "强调图标"),
], preview="box", demo="stroke-sky-500")

util("stroke-width", "stroke-width", "SVG 描边粗细。24 视口的图标常用 1.5 或 2。", SVG, "stroke-width", [
    ("stroke-0", "0", "无"),
    ("stroke-1", "1", "细"),
    ("stroke-2", "2", "标准线图标"),
], preview="box", demo="stroke-2")

AC = "无障碍"
add_group(AC, [{"title": "forced-color-adjust", "slug": "forced-color-adjust"}])
util("forced-color-adjust", "forced-color-adjust", "在 Windows 高对比度等强制色彩模式下，是否允许浏览器替换颜色。", AC, "forced-color-adjust", [
    ("forced-color-adjust-auto", "auto", "允许系统调整，默认更安全"),
    ("forced-color-adjust-none", "none", "保留原色，仅用于必须保持品牌色的图形"),
], extra=[
    p("不要用颜色作为唯一的状态提示。图标按钮需要 aria-label。表单控件需要关联的 label。焦点环在两种主题下都要看得见。"),
], preview="box", demo="forced-color-adjust-auto")

# collect classes used inside code samples roughly
for page_data in pages.values():
    for section in page_data["sections"]:
        if section.get("type") == "code":
            for token in section.get("code", "").replace('"', " ").replace("'", " ").replace("<", " ").replace(">", " ").split():
                if any(ch in token for ch in "-:/") or token in {"flex", "grid", "hidden", "italic", "underline", "truncate", "antialiased", "isolate", "grayscale", "invert", "sepia", "blur", "grow", "shrink", "border", "table", "resize", "animate-spin", "animate-ping", "animate-pulse", "animate-bounce"}:
                    if token.startswith(("bg-", "text-", "border", "rounded", "shadow", "p-", "m-", "w-", "h-", "flex", "grid", "dark:", "hover:", "sm:", "md:", "lg:", "font-", "leading-", "tracking-", "aspect-", "object-", "overflow", "items-", "justify-", "gap-", "min-", "max-", "size-", "from-", "to-", "via-", "outline", "ring-", "accent-", "cursor-", "list-", "line-clamp", "transition", "duration-", "ease-", "rotate-", "scale-", "translate", "fill-", "stroke")):
                        classes.add(token.strip(".,;"))

html = "<div class=\"hidden\">\n" + "\n".join(f'<span class="{name}"></span>' for name in sorted(classes)) + "\n</div>\n"
SAFELIST.parent.mkdir(parents=True, exist_ok=True)
SAFELIST.write_text(html, encoding="utf-8")
OUT.write_text(json.dumps({"groups": groups, "pages": pages}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"pages={len(pages)} groups={len(groups)} classes={len(classes)}")
