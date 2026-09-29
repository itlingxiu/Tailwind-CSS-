<script setup lang="ts">
const open = useSearchOpen()
const sample = `<div class="flex flex-col items-center gap-6 rounded-2xl p-7 md:flex-row">
  <div>
    <img class="size-48 rounded-md shadow-xl" alt="" />
  </div>
  <div class="flex flex-col items-center md:items-start">
    <span class="text-2xl font-medium">类名战争</span>
    <span class="font-medium text-sky-500">反模式</span>
    <span class="flex gap-2 font-medium text-gray-600">
      <span>第 4 期</span>
      <span>·</span>
      <span>2025</span>
    </span>
  </div>
</div>`
</script>

<template>
  <section class="relative overflow-hidden">
    <div class="mx-auto max-w-[90rem] px-4 pb-20 pt-16 sm:px-6 sm:pt-24 lg:px-8 lg:pt-28">
      <p class="font-mono text-xs text-gray-400">text-4xl sm:text-5xl lg:text-6xl xl:text-8xl tracking-tight text-balance</p>
      <h1 class="mt-3 max-w-5xl text-4xl font-medium tracking-tight text-balance text-gray-950 sm:text-5xl lg:text-6xl xl:text-7xl dark:text-white">
        不用离开 HTML，也能快速构建现代网站。
      </h1>
      <p class="mt-6 max-w-3xl text-lg font-medium leading-8 text-gray-600 dark:text-gray-300">
        一套实用类优先的 CSS 框架。像
        <code class="font-mono text-sky-600 dark:text-sky-400">flex</code>、
        <code class="font-mono text-sky-600 dark:text-sky-400">pt-4</code>、
        <code class="font-mono text-sky-600 dark:text-sky-400">text-center</code>
        和
        <code class="font-mono text-sky-600 dark:text-sky-400">rotate-90</code>
        这样的类，可以直接组合在标记里，搭出任何界面。
      </p>
      <div class="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
        <NuxtLink to="/docs/installation" class="inline-flex cursor-pointer items-center justify-center rounded-full bg-gray-950 px-5 py-2.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:bg-white dark:text-gray-950 dark:hover:bg-gray-200">
          开始使用
        </NuxtLink>
        <button type="button" class="inline-flex cursor-pointer items-center justify-between gap-6 rounded-full border border-gray-200 px-4 py-2.5 text-sm text-gray-500 transition-colors duration-200 hover:bg-gray-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:border-white/10 dark:text-gray-400 dark:hover:bg-white/5" @click="open = true">
          <span class="inline-flex items-center gap-2">
            <svg viewBox="0 0 20 20" class="size-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.25" /><path d="M12.5 12.5 17 17" stroke-linecap="round" /></svg>
            快速搜索
          </span>
          <kbd class="rounded-full border border-gray-200 px-2 text-xs dark:border-white/10">Ctrl K</kbd>
        </button>
      </div>

      <div class="mt-16 grid items-center gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <CodeBlock :code="sample" lang="html" filename="index.html" />
        <div class="flex flex-col items-center gap-6 rounded-2xl border border-gray-200 bg-white p-7 shadow-sm md:flex-row dark:border-white/10 dark:bg-gray-900">
          <div class="grid size-40 shrink-0 place-items-center rounded-md bg-gradient-to-br from-sky-400 via-indigo-500 to-fuchsia-500 shadow-xl sm:size-48" role="img" aria-label="封面示意">
            <span class="font-mono text-xs font-medium tracking-widest text-white/90">COVER</span>
          </div>
          <div class="flex flex-col items-center text-center md:items-start md:text-left">
            <span class="text-2xl font-medium text-gray-950 dark:text-white">类名战争</span>
            <span class="font-medium text-sky-500">反模式</span>
            <span class="mt-2 flex gap-2 text-sm font-medium text-gray-600 dark:text-gray-400">
              <span>第 4 期</span>
              <span>·</span>
              <span>2025</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
