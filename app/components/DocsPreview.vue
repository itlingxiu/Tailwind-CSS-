<script setup lang="ts">
defineProps<{
  preview: string
  demo: string
}>()
</script>

<template>
  <div class="not-prose my-6 overflow-hidden rounded-2xl border border-gray-200 bg-gray-50 p-4 dark:border-white/10 dark:bg-white/5">
    <div v-if="preview === 'text'" class="rounded-xl bg-white p-6 dark:bg-gray-950">
      <p class="text-gray-950 dark:text-white" :class="demo">敏捷的棕色狐狸跳过懒狗。The quick brown fox jumps.</p>
    </div>
    <div v-else-if="preview === 'flex'" class="flex gap-2 rounded-xl bg-white p-4 dark:bg-gray-950" :class="demo">
      <div class="rounded-lg bg-sky-500 px-3 py-6 text-xs text-white">一</div>
      <div class="rounded-lg bg-indigo-500 px-3 py-6 text-xs text-white">二</div>
      <div class="rounded-lg bg-fuchsia-500 px-3 py-6 text-xs text-white">三</div>
    </div>
    <div v-else-if="preview === 'grid'" class="grid grid-cols-3 gap-2 rounded-xl bg-white p-4 dark:bg-gray-950">
      <div class="rounded-lg bg-sky-500 py-6 text-center text-xs text-white" :class="demo">一</div>
      <div class="rounded-lg bg-indigo-500 py-6 text-center text-xs text-white">二</div>
      <div class="rounded-lg bg-fuchsia-500 py-6 text-center text-xs text-white">三</div>
    </div>
    <div v-else-if="preview === 'color'" class="h-28 rounded-xl" :class="demo" />
    <div v-else-if="preview === 'spacing'" class="rounded-xl bg-sky-100 dark:bg-sky-400/20">
      <div class="bg-sky-500 text-center text-sm text-white" :class="demo">内容</div>
    </div>
    <div v-else-if="preview === 'rounded' || preview === 'shadow' || preview === 'box' || preview === 'border'" class="grid place-items-center rounded-xl bg-[linear-gradient(135deg,#e0f2fe,#fae8ff)] py-8 dark:bg-gray-950">
      <div class="grid size-28 place-items-center bg-white text-xs font-medium text-gray-700 dark:bg-gray-900 dark:text-gray-200" :class="demo">示例</div>
    </div>
    <div v-else-if="preview === 'filter'" class="grid place-items-center rounded-xl bg-[radial-gradient(circle_at_30%_30%,#38bdf8,#4f46e5_45%,#111827)] py-8">
      <div class="size-24 rounded-2xl bg-gradient-to-br from-amber-300 to-rose-500" :class="demo" />
    </div>
    <div v-else-if="preview === 'backdrop'" class="relative h-36 overflow-hidden rounded-xl bg-[radial-gradient(circle_at_20%_20%,#38bdf8,transparent_40%),radial-gradient(circle_at_80%_30%,#e879f9,transparent_40%),linear-gradient(#111827,#312e81)]">
      <div class="absolute inset-x-6 bottom-6 rounded-xl px-4 py-3 text-sm font-medium text-gray-950" :class="demo">背后的颜色被处理过</div>
    </div>
    <div v-else-if="preview === 'position'" class="relative h-36 rounded-xl bg-white dark:bg-gray-950">
      <div class="absolute size-16 rounded-lg bg-sky-500" :class="demo" />
    </div>
    <div v-else-if="preview === 'transform' || preview === 'transition'" class="grid place-items-center py-6">
      <div class="rounded-xl bg-sky-500 px-4 py-6 text-sm font-semibold text-white" :class="demo">变换</div>
    </div>
    <div v-else-if="preview === 'table'" class="overflow-x-auto rounded-xl bg-white dark:bg-gray-950">
      <table class="w-full text-left text-sm" :class="demo">
        <caption class="caption-top p-2 text-gray-500">周末班次</caption>
        <thead>
          <tr class="border-b border-gray-200 dark:border-white/10">
            <th class="p-2">线路</th>
            <th class="p-2">班次</th>
          </tr>
        </thead>
        <tbody>
          <tr class="border border-gray-200 dark:border-white/10"><td class="p-2">湖滨</td><td class="p-2">08:30</td></tr>
          <tr class="border border-gray-200 dark:border-white/10"><td class="p-2">山脊</td><td class="p-2">11:00</td></tr>
        </tbody>
      </table>
    </div>
    <div v-else class="rounded-xl bg-white p-6 text-sm text-gray-700 dark:bg-gray-950 dark:text-gray-200" :class="demo">
      示例
    </div>
    <p v-if="demo" class="mt-3 font-mono text-xs text-gray-500">{{ demo }}</p>
  </div>
</template>
