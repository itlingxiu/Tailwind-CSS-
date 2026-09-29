<script setup lang="ts">
import { partners } from '~/data/site'

const loop = computed(() => [...partners, ...partners])
</script>

<template>
  <section class="border-t border-gray-200 py-20 dark:border-white/10">
    <div class="mx-auto max-w-[90rem] px-4 sm:px-6 lg:px-8">
      <p class="text-sm font-semibold tracking-[0.2em] text-gray-500">赞助</p>
      <div class="mt-4 flex flex-col justify-between gap-6 md:flex-row md:items-end">
        <div>
          <p class="font-mono text-xs text-gray-400">text-4xl tracking-tight</p>
          <h2 class="mt-2 text-4xl font-medium tracking-tight text-gray-950 sm:text-5xl dark:text-white">由优秀的伙伴支持。</h2>
          <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
            Tailwind 能由全职设计和工程团队持续维护，离不开合作伙伴与赞助者。下面列出的是公开赞助名单中的一部分。
          </p>
        </div>
        <NuxtLink to="/partners" class="inline-flex cursor-pointer items-center justify-center rounded-full border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-950 transition-colors duration-200 hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:border-white/15 dark:text-white dark:hover:bg-white/10">
          成为赞助者
        </NuxtLink>
      </div>
    </div>
    <div class="marquee mt-12 overflow-hidden">
      <div class="marquee-track flex w-max gap-3 px-4">
        <a
          v-for="(item, index) in loop"
          :key="`${item.name}-${index}`"
          :href="item.url"
          target="_blank"
          rel="noreferrer"
          class="inline-flex h-16 min-w-40 cursor-pointer items-center justify-center rounded-2xl border border-gray-200 bg-white px-6 text-sm font-semibold tracking-tight text-gray-800 transition-colors duration-200 hover:border-sky-300 hover:text-sky-700 dark:border-white/10 dark:bg-white/5 dark:text-gray-100 dark:hover:border-sky-400/40 dark:hover:text-sky-300"
        >
          {{ item.name }}
        </a>
      </div>
    </div>
  </section>
</template>
