<script setup lang="ts">
const tab = ref<'html' | 'css' | 'pkg'>('html')
const picked = ref(['rounded-full', 'bg-sky-500', 'px-4', 'py-2', 'font-semibold', 'text-white'])
const options = ['rounded-full', 'bg-sky-500', 'px-4', 'py-2', 'font-semibold', 'text-white', 'shadow-lg', 'hover:bg-sky-400']

const cssMap: Record<string, string> = {
  'rounded-full': 'border-radius: 9999px;',
  'bg-sky-500': 'background-color: var(--color-sky-500);',
  'px-4': 'padding-inline: 1rem;',
  'py-2': 'padding-block: 0.5rem;',
  'font-semibold': 'font-weight: 600;',
  'text-white': 'color: #fff;',
  'shadow-lg': 'box-shadow: var(--shadow-lg);',
  'hover:bg-sky-400': 'background-color: var(--color-sky-400);',
}

function toggle(name: string) {
  picked.value = picked.value.includes(name) ? picked.value.filter((item) => item !== name) : [...picked.value, name]
}

const generated = computed(() => {
  const lines = picked.value.map((name) => `  ${cssMap[name]}`)
  return `@layer utilities {\n${lines.join('\n')}\n}`
})

const files = computed(() => ({
  html: `<button class="${picked.value.join(' ')}">\n  发布\n</button>`,
  css: '@import "tailwindcss";',
  pkg: '{\n  "dependencies": {\n    "tailwindcss": "^4.1.0",\n    "@tailwindcss/vite": "^4.1.0"\n  }\n}',
}))
</script>

<template>
  <section class="border-t border-gray-200 py-20 dark:border-white/10">
    <div class="mx-auto max-w-[90rem] px-4 sm:px-6 lg:px-8">
      <p class="text-sm font-semibold tracking-[0.2em] text-gray-500">它如何工作</p>
      <h2 class="mt-3 text-4xl font-medium tracking-tight text-gray-950 sm:text-5xl dark:text-white">发得更快，也更小。</h2>
      <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
        生产构建会去掉所有没用到的 CSS。多数项目发到浏览器的样式不足 10kB。勾选类名，看右侧只留下对应规则。
      </p>
      <div class="mt-10 grid gap-6 lg:grid-cols-2">
        <div>
          <div class="flex gap-2">
            <button v-for="item in (['html', 'css', 'pkg'] as const)" :key="item" type="button" class="cursor-pointer rounded-full px-3 py-1 text-xs font-semibold transition-colors duration-200" :class="tab === item ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'bg-gray-100 text-gray-700 dark:bg-white/10 dark:text-gray-200'" @click="tab = item">
              {{ item === 'html' ? 'index.html' : item === 'css' ? 'app.css' : 'package.json' }}
            </button>
          </div>
          <div class="mt-4">
            <CodeBlock :code="files[tab]" :lang="tab === 'html' ? 'html' : tab === 'css' ? 'css' : 'json'" />
          </div>
          <div class="mt-4 flex flex-wrap gap-2">
            <button v-for="name in options" :key="name" type="button" class="cursor-pointer rounded-full border px-3 py-1 font-mono text-xs transition-colors duration-200" :class="picked.includes(name) ? 'border-sky-500 bg-sky-50 text-sky-800 dark:bg-sky-400/10 dark:text-sky-200' : 'border-gray-200 text-gray-600 dark:border-white/10 dark:text-gray-300'" @click="toggle(name)">
              {{ name }}
            </button>
          </div>
        </div>
        <div>
          <p class="text-xs font-semibold text-gray-500">build.css</p>
          <div class="mt-4">
            <CodeBlock :code="generated" lang="css" filename="build.css" />
          </div>
          <button type="button" class="mt-6 cursor-pointer transition-colors duration-200" :class="picked">发布</button>
        </div>
      </div>
    </div>
  </section>
</template>
