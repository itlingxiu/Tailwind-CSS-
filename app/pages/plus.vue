<script setup lang="ts">
import { plusModules } from '~/data/site'

const faqs = [
  { q: 'Plus 是什么？', a: 'Tailwind Plus 是 Tailwind Labs 的付费产品，包含网站模板、可复制的界面组件，以及面向 React 的 Catalyst。外观仍然由实用类决定。' },
  { q: '本站能购买吗？', a: '不能。这里只介绍产品构成。价格、许可证和更新以 Tailwind Labs 官方页面为准。' },
  { q: '和开源框架是什么关系？', a: 'Tailwind CSS 框架本身是开源的。Plus 是可选的界面素材，不是使用框架的前提。' },
]

useSeoMeta({
  title: 'Tailwind Plus',
  description: '网站模板、界面组件和 Catalyst 的中文介绍。购买与许可以官方页面为准。',
})
</script>

<template>
  <div>
    <section class="mx-auto max-w-6xl px-4 py-16 sm:px-6">
      <p class="text-sm font-semibold text-sky-600 dark:text-sky-400">Tailwind Plus</p>
      <h1 class="mt-3 max-w-3xl text-4xl font-medium tracking-tight text-gray-950 sm:text-5xl dark:text-white">少写样板，把时间留在产品上。</h1>
      <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
        模板、组件和 Catalyst 都用实用类写成。你拿到的是可以继续改的标记，而不是一份编译后的样式表。
      </p>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="https://tailwindcss.com/plus" target="_blank" rel="noreferrer" class="inline-flex cursor-pointer rounded-full bg-gray-950 px-4 py-2 text-sm font-semibold text-white dark:bg-white dark:text-gray-950">查看官方 Plus</a>
        <NuxtLink to="/docs/installation" class="inline-flex cursor-pointer rounded-full border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-950 dark:border-white/15 dark:text-white">先安装开源框架</NuxtLink>
      </div>
      <div class="mt-12 grid gap-4 lg:grid-cols-3">
        <article v-for="item in plusModules" :key="item.name" class="rounded-2xl border border-gray-200 p-6 dark:border-white/10">
          <h2 class="text-xl font-semibold text-gray-950 dark:text-white">{{ item.name }}</h2>
          <p class="mt-2 text-sm leading-6 text-gray-600 dark:text-gray-300">{{ item.summary }}</p>
          <ul class="mt-4 space-y-2">
            <li v-for="point in item.points" :key="point" class="flex gap-2 text-sm text-gray-700 dark:text-gray-200">
              <svg viewBox="0 0 20 20" class="mt-0.5 size-4 shrink-0 text-sky-500" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 10.5 8 14l8-8" stroke-linecap="round" stroke-linejoin="round" /></svg>
              {{ point }}
            </li>
          </ul>
        </article>
      </div>
    </section>
    <section class="border-t border-gray-200 dark:border-white/10">
      <div class="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <h2 class="text-2xl font-semibold text-gray-950 dark:text-white">常见问题</h2>
        <div class="mt-6 divide-y divide-gray-200 dark:divide-white/10">
          <details v-for="item in faqs" :key="item.q" class="group py-4">
            <summary class="cursor-pointer list-none font-medium text-gray-950 dark:text-white">{{ item.q }}</summary>
            <p class="mt-2 text-sm leading-6 text-gray-600 dark:text-gray-300">{{ item.a }}</p>
          </details>
        </div>
      </div>
    </section>
  </div>
</template>
