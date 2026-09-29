<script setup lang="ts">
import { partners } from '~/data/site'

const tiers = ['旗舰', '赞助', '社区'] as const

useSeoMeta({
  title: '合作伙伴 · Tailwind CSS',
  description: '支持 Tailwind CSS 持续维护的公开赞助与合作伙伴。',
})
</script>

<template>
  <div class="mx-auto max-w-6xl px-4 py-16 sm:px-6">
    <p class="text-sm font-semibold tracking-[0.18em] text-gray-500">合作伙伴</p>
    <h1 class="mt-3 text-4xl font-medium tracking-tight text-gray-950 sm:text-5xl dark:text-white">让全职维护成为可能。</h1>
    <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
      名单来自官网公开赞助信息，按层级分组，方便浏览。成为赞助者请前往 Tailwind Labs 的官方渠道，本站不处理付款。
    </p>
    <div class="mt-8">
      <a href="https://tailwindcss.com/partners" target="_blank" rel="noreferrer" class="inline-flex cursor-pointer rounded-full bg-gray-950 px-4 py-2 text-sm font-semibold text-white dark:bg-white dark:text-gray-950">查看官网合作伙伴</a>
    </div>
    <div v-for="tier in tiers" :key="tier" class="mt-12">
      <h2 class="text-lg font-semibold text-gray-950 dark:text-white">{{ tier }}</h2>
      <div class="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <a v-for="item in partners.filter((partner) => partner.tier === tier)" :key="item.name" :href="item.url" target="_blank" rel="noreferrer" class="cursor-pointer rounded-2xl border border-gray-200 p-5 transition-colors duration-200 hover:border-sky-300 dark:border-white/10 dark:hover:border-sky-400/40">
          <p class="text-lg font-semibold text-gray-950 dark:text-white">{{ item.name }}</p>
          <p class="mt-2 text-sm leading-6 text-gray-600 dark:text-gray-300">{{ item.blurb }}</p>
        </a>
      </div>
    </div>
  </div>
</template>
