<script setup lang="ts">
import { showcase } from '~/data/site'

const category = ref('全部')
const categories = ['全部', ...new Set(showcase.map((item) => item.category))]
const visible = computed(() => category.value === '全部' ? showcase : showcase.filter((item) => item.category === category.value))

useSeoMeta({
  title: '案例 · Tailwind CSS',
  description: '使用 Tailwind CSS 构建的公开网站。每个站点的版式都不一样。',
})
</script>

<template>
  <div class="mx-auto max-w-[90rem] px-4 py-16 sm:px-6 lg:px-8">
    <p class="text-sm font-semibold tracking-[0.18em] text-gray-500">案例</p>
    <h1 class="mt-3 max-w-3xl text-4xl font-medium tracking-tight text-gray-950 sm:text-5xl dark:text-white">同一套类名，完全不同的网站。</h1>
    <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
      这些是公开可访问的站点。卡片是版式示意，不是对方页面的截图。点击会前往原站。
    </p>
    <div class="mt-8 flex flex-wrap gap-2">
      <button v-for="item in categories" :key="item" type="button" class="cursor-pointer rounded-full px-3 py-1 text-sm font-medium transition-colors duration-200" :class="category === item ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'bg-gray-100 text-gray-700 dark:bg-white/10 dark:text-gray-200'" @click="category = item">
        {{ item }}
      </button>
    </div>
    <div class="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <a v-for="item in visible" :key="item.host" :href="item.url" target="_blank" rel="noreferrer" class="cursor-pointer overflow-hidden rounded-2xl border border-gray-200 bg-white transition-colors duration-200 hover:border-sky-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:border-white/10 dark:bg-gray-900 dark:hover:border-sky-400/40">
        <div class="flex h-40 flex-col justify-between p-4 text-white" :style="{ backgroundImage: `linear-gradient(145deg, ${item.from}, ${item.to})` }">
          <span class="text-xs font-medium text-white/80">{{ item.category }}</span>
          <span class="text-2xl font-semibold tracking-tight">{{ item.name }}</span>
        </div>
        <div class="p-4">
          <p class="text-sm text-gray-500">{{ item.host }}</p>
          <p class="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-200">{{ item.blurb }}</p>
        </div>
      </a>
    </div>
  </div>
</template>
