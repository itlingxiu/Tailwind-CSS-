<script setup lang="ts">
const theme = useTheme()
const options = [
  { id: 'system', label: '系统' },
  { id: 'light', label: '浅色' },
  { id: 'dark', label: '深色' },
] as const

const columns = [
  {
    title: 'Tailwind CSS',
    links: [
      { label: '文档', to: '/docs' },
      { label: '演练场', to: '/play' },
      { label: '博客', to: '/blog' },
      { label: '案例', to: '/showcase' },
    ],
  },
  {
    title: '资源',
    links: [
      { label: 'Refactoring UI', href: 'https://www.refactoringui.com' },
      { label: 'Headless UI', href: 'https://headlessui.com' },
      { label: 'Heroicons', href: 'https://heroicons.com' },
      { label: 'Hero Patterns', href: 'https://heropatterns.com' },
    ],
  },
  {
    title: '社区',
    links: [
      { label: 'GitHub', href: 'https://github.com/tailwindlabs/tailwindcss' },
      { label: 'X', href: 'https://x.com/tailwindcss' },
    ],
  },
]
</script>

<template>
  <footer class="border-t border-gray-200 bg-white dark:border-white/10 dark:bg-gray-950">
    <div class="mx-auto grid max-w-[90rem] gap-10 px-4 py-16 sm:px-6 md:grid-cols-4 lg:px-8">
      <div>
        <NuxtLink to="/" class="inline-flex items-center gap-2 font-semibold text-gray-950 dark:text-white" aria-label="首页">
          <LogoMark />
          tailwindcss
        </NuxtLink>
        <p class="mt-4 max-w-xs text-sm leading-6 text-gray-600 dark:text-gray-400">
          本站是学习用途的中文界面复刻，与 Tailwind Labs 没有隶属关系。Tailwind CSS 及其标识归 Tailwind Labs 所有。
        </p>
        <fieldset class="mt-6">
          <legend class="text-xs font-semibold tracking-wide text-gray-500">主题</legend>
          <div class="mt-2 inline-flex rounded-full border border-gray-200 p-1 dark:border-white/10" role="radiogroup" aria-label="主题">
            <label
              v-for="option in options"
              :key="option.id"
              class="cursor-pointer rounded-full px-3 py-1 text-xs font-medium transition-colors duration-200"
              :class="theme === option.id ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'text-gray-600 hover:text-gray-950 dark:text-gray-300'"
            >
              <input v-model="theme" class="sr-only" type="radio" name="theme" :value="option.id" />
              {{ option.label }}
            </label>
          </div>
        </fieldset>
      </div>
      <div v-for="column in columns" :key="column.title">
        <h2 class="text-sm font-semibold text-gray-950 dark:text-white">{{ column.title }}</h2>
        <ul class="mt-4 space-y-3">
          <li v-for="link in column.links" :key="link.label">
            <NuxtLink v-if="'to' in link" :to="link.to" class="cursor-pointer text-sm text-gray-600 transition-colors duration-200 hover:text-gray-950 dark:text-gray-400 dark:hover:text-white">{{ link.label }}</NuxtLink>
            <a v-else :href="link.href" target="_blank" rel="noreferrer" class="cursor-pointer text-sm text-gray-600 transition-colors duration-200 hover:text-gray-950 dark:text-gray-400 dark:hover:text-white">{{ link.label }}</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-200 dark:border-white/10">
      <div class="mx-auto flex max-w-[90rem] flex-col gap-2 px-4 py-6 text-xs text-gray-500 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <p>界面内容为中文学习复刻 · Copyright © 2026 Tailwind Labs Inc.</p>
        <NuxtLink to="/trademark" class="cursor-pointer underline-offset-2 hover:underline">商标说明</NuxtLink>
      </div>
    </div>
  </footer>
</template>
