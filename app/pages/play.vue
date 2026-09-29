<script setup lang="ts">
const html = ref(`<div class="mx-auto max-w-sm rounded-2xl bg-white p-6 shadow-xl">
  <p class="text-sm font-medium text-sky-600">演练场</p>
  <h1 class="mt-2 text-2xl font-semibold text-gray-950">改类名，立刻看结果。</h1>
  <p class="mt-3 text-sm leading-6 text-gray-600">这是浏览器里的 Tailwind，适合试布局，不适合作为生产构建。</p>
  <button class="mt-4 rounded-full bg-sky-500 px-4 py-2 text-sm font-semibold text-white">开始</button>
</div>`)

const srcdoc = computed(() => `<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"><\/script>
</head>
<body class="min-h-screen bg-gray-100 p-6">
${html.value.replace(/<script/gi, '')}
</body>
</html>`)

useSeoMeta({
  title: '演练场 · Tailwind CSS',
  description: '在浏览器里修改 HTML 类名，并立刻预览 Tailwind CSS 的效果。',
})
</script>

<template>
  <div class="mx-auto grid min-h-[calc(100vh-8rem)] max-w-[90rem] gap-4 px-4 py-6 lg:grid-cols-2 lg:px-6">
    <section class="flex min-h-96 flex-col">
      <div class="mb-3 flex items-center justify-between">
        <h1 class="text-lg font-semibold text-gray-950 dark:text-white">标记</h1>
        <p class="text-xs text-gray-500">预览使用浏览器构建</p>
      </div>
      <label class="sr-only" for="playground">HTML</label>
      <textarea id="playground" v-model="html" spellcheck="false" class="min-h-[32rem] flex-1 resize-y rounded-2xl border border-gray-800 bg-gray-950 p-4 font-mono text-sm leading-6 text-gray-100 outline-none focus-visible:outline-2 focus-visible:outline-sky-500" />
    </section>
    <section class="overflow-hidden rounded-2xl border border-gray-200 bg-gray-100 dark:border-white/10">
      <div class="flex items-center gap-2 border-b border-gray-200 bg-white px-4 py-2 dark:border-white/10 dark:bg-gray-900">
        <span class="size-2.5 rounded-full bg-gray-300" />
        <span class="size-2.5 rounded-full bg-gray-300" />
        <span class="size-2.5 rounded-full bg-gray-300" />
        <span class="ml-2 text-xs text-gray-500">预览</span>
      </div>
      <iframe class="h-[36rem] w-full bg-gray-100" sandbox="allow-scripts" :srcdoc="srcdoc" title="Tailwind 预览" />
    </section>
  </div>
</template>
