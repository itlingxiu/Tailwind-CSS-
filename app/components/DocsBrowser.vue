<script setup lang="ts">
import docs from '~/data/docs.json'

type Row = { class: string; css: string; note: string }
type Section = {
  type: 'p' | 'h2' | 'h3' | 'tip' | 'code' | 'table'
  text?: string
  lang?: string
  code?: string
  headers?: string[]
  rows?: Row[]
}

interface DocPage {
  slug: string
  title: string
  summary: string
  group: string
  demo: string
  preview: string
  sections: Section[]
}

const route = useRoute()
const openSearch = useSearchOpen()
const mobileNav = ref(false)
const pages = docs.pages as unknown as Record<string, DocPage>

const slug = computed(() => {
  const value = route.params.slug
  if (!value) return ''
  return Array.isArray(value) ? value.join('/') : String(value)
})

const page = computed(() => pages[slug.value] ?? null)
const flat = computed(() => docs.groups.flatMap((group) => group.items.map((item) => ({ ...item, group: group.title }))))
const index = computed(() => flat.value.findIndex((item) => item.slug === slug.value))
const previous = computed(() => (index.value > 0 ? flat.value[index.value - 1] : null))
const next = computed(() => (index.value >= 0 && index.value < flat.value.length - 1 ? flat.value[index.value + 1] : null))

const officialPangram = '敏捷的棕色狐狸跳过了那只懒狗。'

const previewSamples: Record<string, string> = {
  installation: '在模板里写上类名，构建时会生成对应的静态 CSS。',
  'installation/using-vite': '你好，世界！',
  'installation/using-postcss': '已有 PostCSS 流水线时，装上插件即可。',
  'installation/tailwind-cli': '没有前端框架时，用命令行编译 CSS。',
  'installation/framework-guides': '主流框架都可以在几分钟内接上。',
  'installation/play-cdn': '浏览器里的 Tailwind',
  'editor-setup': '用编辑器插件补全类名、预览颜色，并整理类名顺序。',
  compatibility: '了解浏览器支持情况，以及与其他工具一起使用时的兼容性。',
  'upgrade-guide': '把 Tailwind CSS 项目从 v3 升级到 v4。',
  'styling-with-utility-classes': '保存更改',
  'hover-focus-and-other-states': '悬停或聚焦时再变色',
  theme: '颜色、字体和断点都写在 CSS 主题里。',
  'adding-custom-styles': '实用类不够用时，再补一层自定义 CSS。',
  'detecting-classes-in-source-files': '类名必须完整写在源码里，扫描器才能找到。',
  'functions-and-directives': '用指令和函数扩展主题与样式。',
  preflight: '预检会抹平各浏览器不一致的默认样式。',
  columns: '这段文字会分成多列排布，阅读方式更接近报刊。',
  'break-after': '分页或分列时，避免在这个元素后面断开。',
  'break-before': '分页或分列时，避免在这个元素前面断开。',
  'box-decoration-break': '换行之后，每一段都保留自己的背景和内边距。',
  'line-clamp': '这是一段较长的说明。超出指定行数后，多余文字会被截断，并在末尾显示省略号。',
  'text-overflow': '这是一段会被截断的说明，超出容器宽度后以省略号结尾。',
  'text-wrap': '把标题写成两行，让每一行的宽度更加均衡。',
  'white-space': '这段文字保持在同一行里',
  content: '下一项',
  'background-clip': '渐变只出现在文字上',
  'text-shadow': '带阴影的文字',
  'accent-color': '表单控件的强调色',
  appearance: '去掉浏览器自带的控件外观',
  'caret-color': '输入时光标使用主题色',
  cursor: '指针悬停时显示手型',
  'field-sizing': '输入框宽度跟着内容走',
  resize: '可以沿垂直方向拖拽调整大小',
  'user-select': '点击即可选中整段文字',
}

const previewSample = computed(() => {
  const current = page.value
  if (!current || current.preview !== 'text') return ''
  return previewSamples[current.slug] || (current.group === '排版' ? officialPangram : '')
})

const showPreview = computed(() => {
  const current = page.value
  if (!current?.preview) return false
  if (current.preview === 'text') return Boolean(previewSample.value)
  return true
})

const headings = computed(() =>
  (page.value?.sections ?? [])
    .filter((section) => section.type === 'h2' && section.text)
    .map((section) => ({ id: anchor(section.text || ''), text: section.text || '' })),
)

function anchor(text: string) {
  return text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\u4e00-\u9fff-]/g, '')
}

watch(() => route.fullPath, () => {
  mobileNav.value = false
})

useSeoMeta({
  title: () => page.value ? `${page.value.title} · Tailwind CSS 中文文档` : '文档 · Tailwind CSS',
  description: () => page.value?.summary || 'Tailwind CSS 中文文档，涵盖安装、核心概念和全部实用类。',
})
</script>

<template>
  <div class="mx-auto flex max-w-[90rem] items-start">
    <aside class="sticky top-16 hidden h-[calc(100vh-4rem)] w-72 shrink-0 overflow-y-auto px-4 py-8 lg:block">
      <DocsSidebar />
    </aside>

    <div v-if="mobileNav" class="fixed inset-0 z-30 lg:hidden">
      <button type="button" class="absolute inset-0 cursor-pointer bg-gray-950/50" aria-label="关闭目录" @click="mobileNav = false" />
      <div class="absolute inset-y-0 left-0 w-80 overflow-y-auto bg-white p-4 pt-20 dark:bg-gray-950">
        <DocsSidebar v-model="mobileNav" />
      </div>
    </div>

    <article class="min-w-0 flex-1 px-4 py-8 sm:px-8 lg:px-10">
      <button type="button" class="mb-6 cursor-pointer rounded-full border border-gray-200 px-3 py-1.5 text-sm font-medium text-gray-700 lg:hidden dark:border-white/10 dark:text-gray-200" @click="mobileNav = true">
        打开目录
      </button>

      <template v-if="!slug">
        <p class="text-sm font-semibold tracking-[0.18em] text-gray-500">文档</p>
        <h1 class="mt-3 text-4xl font-medium tracking-tight text-gray-950 sm:text-5xl dark:text-white">用中文查阅 Tailwind CSS。</h1>
        <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
          从安装到每一个实用类。搜索可以按类名、属性或中文说明查找，侧栏与官网文档的信息架构一致。
        </p>
        <button type="button" class="mt-6 inline-flex cursor-pointer items-center gap-2 rounded-full border border-gray-200 px-4 py-2 text-sm text-gray-600 transition-colors duration-200 hover:bg-gray-50 dark:border-white/10 dark:text-gray-300 dark:hover:bg-white/5" @click="openSearch = true">
          搜索 {{ flat.length }} 篇文档
        </button>
        <div class="mt-10 grid gap-4 sm:grid-cols-2">
          <NuxtLink
            v-for="group in docs.groups"
            :key="group.title"
            :to="`/docs/${group.items[0].slug}`"
            class="cursor-pointer rounded-2xl border border-gray-200 p-5 transition-colors duration-200 hover:border-sky-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:border-white/10 dark:hover:border-sky-400/40"
          >
            <h2 class="text-lg font-semibold text-gray-950 dark:text-white">{{ group.title }}</h2>
            <p class="mt-2 text-sm text-gray-500">{{ group.items.length }} 篇 · 从「{{ group.items[0].title }}」开始</p>
          </NuxtLink>
        </div>
      </template>

      <template v-else-if="page">
        <p class="text-sm font-medium text-sky-600 dark:text-sky-400">{{ page.group }}</p>
        <h1 class="mt-2 text-4xl font-semibold tracking-tight text-gray-950 dark:text-white">{{ page.title }}</h1>
        <p class="mt-4 text-lg leading-8 text-gray-600 dark:text-gray-300">{{ page.summary }}</p>
        <DocsPreview v-if="showPreview" :preview="page.preview" :demo="page.demo" :sample="previewSample" />
        <div class="docs-prose">
          <template v-for="(section, sectionIndex) in page.sections" :key="sectionIndex">
            <h2 v-if="section.type === 'h2'" :id="anchor(section.text || '')">{{ section.text }}</h2>
            <h3 v-else-if="section.type === 'h3'" :id="anchor(section.text || '')">{{ section.text }}</h3>
            <p v-else-if="section.type === 'p' && section.text !== page.summary">{{ section.text }}</p>
            <div v-else-if="section.type === 'tip'" class="docs-tip">{{ section.text }}</div>
            <div v-else-if="section.type === 'code'" class="my-6">
              <CodeBlock :code="section.code || ''" :lang="section.lang" />
            </div>
            <div v-else-if="section.type === 'table'" class="my-6 overflow-x-auto rounded-xl border border-gray-200 dark:border-white/10">
              <table class="w-full min-w-[36rem] text-left text-sm">
                <thead class="bg-gray-50 text-gray-500 dark:bg-white/5">
                  <tr>
                    <th class="px-4 py-2 font-medium">{{ section.headers?.[0] || '类' }}</th>
                    <th class="px-4 py-2 font-medium">{{ section.headers?.[1] || 'CSS' }}</th>
                    <th class="px-4 py-2 font-medium">{{ section.headers?.[2] || '说明' }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in section.rows" :key="row.class" class="border-t border-gray-200 dark:border-white/10">
                    <td class="px-4 py-2 font-mono text-xs text-sky-700 dark:text-sky-300">{{ row.class }}</td>
                    <td class="px-4 py-2 font-mono text-xs text-gray-600 dark:text-gray-300">{{ row.css }}</td>
                    <td class="px-4 py-2 text-gray-700 dark:text-gray-200">{{ row.note }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </div>
        <div class="mt-16 grid gap-3 border-t border-gray-200 pt-6 sm:grid-cols-2 dark:border-white/10">
          <NuxtLink v-if="previous" :to="`/docs/${previous.slug}`" class="cursor-pointer rounded-xl border border-gray-200 px-4 py-3 transition-colors duration-200 hover:border-sky-300 dark:border-white/10 dark:hover:border-sky-400/40">
            <span class="text-xs text-gray-500">上一篇</span>
            <span class="mt-1 block font-medium text-gray-950 dark:text-white">{{ previous.title }}</span>
          </NuxtLink>
          <NuxtLink v-if="next" :to="`/docs/${next.slug}`" class="cursor-pointer rounded-xl border border-gray-200 px-4 py-3 text-right transition-colors duration-200 hover:border-sky-300 sm:col-start-2 dark:border-white/10 dark:hover:border-sky-400/40">
            <span class="text-xs text-gray-500">下一篇</span>
            <span class="mt-1 block font-medium text-gray-950 dark:text-white">{{ next.title }}</span>
          </NuxtLink>
        </div>
      </template>

      <template v-else>
        <h1 class="text-3xl font-semibold text-gray-950 dark:text-white">没有这篇文档</h1>
        <p class="mt-3 text-gray-600 dark:text-gray-300">链接可能已变更。回到目录，或直接搜索类名。</p>
        <NuxtLink to="/docs" class="mt-6 inline-flex cursor-pointer text-sm font-semibold text-sky-600">返回文档首页</NuxtLink>
      </template>
    </article>

    <aside v-if="page && headings.length" class="sticky top-16 hidden h-[calc(100vh-4rem)] w-56 shrink-0 overflow-y-auto py-10 pr-6 xl:block">
      <p class="text-xs font-semibold text-gray-500">本页目录</p>
      <ul class="mt-3 space-y-2">
        <li v-for="item in headings" :key="item.id">
          <a :href="`#${item.id}`" class="cursor-pointer text-sm text-gray-600 transition-colors duration-200 hover:text-gray-950 dark:text-gray-400 dark:hover:text-white">{{ item.text }}</a>
        </li>
      </ul>
    </aside>
  </div>
</template>
