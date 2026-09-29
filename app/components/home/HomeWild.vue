<script setup lang="ts">
import { showcase } from '~/data/site'
</script>

<template>
  <section class="border-t border-gray-200 py-20 dark:border-white/10">
    <div class="mx-auto max-w-[90rem] px-4 sm:px-6 lg:px-8">
      <p class="text-sm font-semibold tracking-[0.2em] text-gray-500">真实项目</p>
      <h2 class="mt-3 max-w-3xl text-4xl font-medium tracking-tight text-balance text-gray-950 sm:text-5xl dark:text-white">想做什么就做什么，不必先去改 CSS 文件。</h2>
      <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
        类名足够底层，所以不会把每个网站做成同一个样子。下面这些公开站点都用 Tailwind 搭建，版式却各不相同。
      </p>
      <div class="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <a
          v-for="item in showcase.slice(0, 9)"
          :key="item.host"
          :href="item.url"
          target="_blank"
          rel="noreferrer"
          class="group cursor-pointer overflow-hidden rounded-2xl border border-gray-200 bg-white transition-colors duration-200 hover:border-sky-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:border-white/10 dark:bg-gray-900 dark:hover:border-sky-400/40"
        >
          <div class="h-36" :style="{ backgroundImage: `linear-gradient(135deg, ${item.from}, ${item.to})` }" />
          <div class="flex items-center justify-between px-4 py-3">
            <div>
              <p class="font-semibold text-gray-950 dark:text-white">{{ item.name }}</p>
              <p class="text-sm text-gray-500">{{ item.host }}</p>
            </div>
            <svg viewBox="0 0 20 20" class="size-4 text-gray-400 transition-transform duration-200 group-hover:translate-x-0.5" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </div>
        </a>
      </div>
      <NuxtLink to="/showcase" class="mt-8 inline-flex cursor-pointer text-sm font-semibold text-sky-600 hover:text-sky-500 dark:text-sky-400">查看全部案例</NuxtLink>
    </div>
  </section>
</template>
