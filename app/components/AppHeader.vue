<script setup lang="ts">
import docs from '~/data/docs.json'
import { blogPosts, nav } from '~/data/site'

const route = useRoute()
const open = useSearchOpen()
const menuOpen = ref(false)
const versionOpen = ref(false)

const flatDocs = computed(() =>
  docs.groups.flatMap((group) => group.items.map((item) => ({ ...item, group: group.title }))),
)

watch(() => route.fullPath, () => {
  menuOpen.value = false
  versionOpen.value = false
})

function onKey(event: KeyboardEvent) {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    open.value = true
  }
}

onMounted(() => window.addEventListener('keydown', onKey))
onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-gray-200/80 bg-white/80 backdrop-blur-md dark:border-white/10 dark:bg-gray-950/80">
    <div class="mx-auto flex h-16 max-w-[90rem] items-center gap-3 px-4 sm:px-6 lg:px-8">
      <NuxtLink to="/" class="flex shrink-0 items-center gap-2 rounded-md text-gray-950 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-sky-500 dark:text-white" aria-label="首页">
        <LogoMark />
        <span class="text-lg font-semibold tracking-tight">tailwindcss</span>
      </NuxtLink>

      <div class="relative">
        <button
          type="button"
          class="inline-flex cursor-pointer items-center gap-1 rounded-full border border-gray-200 px-2 py-1 text-xs font-semibold text-gray-700 transition-colors duration-200 hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:border-white/10 dark:text-gray-200 dark:hover:bg-white/10"
          aria-haspopup="listbox"
          :aria-expanded="versionOpen"
          @click="versionOpen = !versionOpen"
        >
          v4.3
          <svg viewBox="0 0 20 20" class="size-3.5" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.17l3.71-3.94a.75.75 0 1 1 1.08 1.04l-4.25 4.5a.75.75 0 0 1-1.08 0l-4.25-4.5a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" /></svg>
        </button>
        <div v-if="versionOpen" class="absolute left-0 top-9 z-50 w-52 rounded-xl border border-gray-200 bg-white p-1 shadow-lg dark:border-white/10 dark:bg-gray-900">
          <p class="px-3 py-2 text-sm font-medium text-gray-950 dark:text-white">v4.3 当前文档</p>
          <NuxtLink to="/docs/upgrade-guide" class="block cursor-pointer rounded-lg px-3 py-2 text-sm text-gray-600 transition-colors duration-200 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-white/10">从 v3 升级</NuxtLink>
        </div>
      </div>

      <div class="flex-1" />

      <button
        type="button"
        class="hidden cursor-pointer items-center gap-3 rounded-full border border-gray-200 bg-gray-50 px-3 py-1.5 text-sm text-gray-500 transition-colors duration-200 hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 sm:inline-flex dark:border-white/10 dark:bg-white/5 dark:text-gray-400 dark:hover:bg-white/10"
        @click="open = true"
      >
        <svg viewBox="0 0 20 20" class="size-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.25" /><path d="M12.5 12.5 17 17" stroke-linecap="round" /></svg>
        <span>搜索</span>
        <kbd class="rounded border border-gray-200 bg-white px-1.5 text-[11px] font-medium text-gray-500 dark:border-white/10 dark:bg-gray-800 dark:text-gray-300">Ctrl K</kbd>
      </button>

      <nav class="hidden items-center gap-1 lg:flex" aria-label="主导航">
        <NuxtLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="cursor-pointer rounded-md px-2.5 py-1.5 text-sm font-medium text-gray-700 transition-colors duration-200 hover:text-gray-950 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:text-gray-300 dark:hover:text-white"
          :class="route.path.startsWith(item.to) ? 'text-gray-950 dark:text-white' : ''"
        >
          {{ item.label }}
        </NuxtLink>
      </nav>

      <NuxtLink
        to="/plus"
        class="hidden cursor-pointer rounded-full border border-sky-300 px-3 py-1 text-sm font-semibold text-sky-600 transition-colors duration-200 hover:bg-sky-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 sm:inline-flex dark:border-sky-400/40 dark:text-sky-300 dark:hover:bg-sky-400/10"
      >
        Plus
      </NuxtLink>

      <a
        href="https://github.com/tailwindlabs/tailwindcss"
        target="_blank"
        rel="noreferrer"
        class="hidden cursor-pointer rounded-full p-2 text-gray-700 transition-colors duration-200 hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 sm:inline-flex dark:text-gray-200 dark:hover:bg-white/10"
        aria-label="GitHub 仓库"
      >
        <svg viewBox="0 0 24 24" class="size-5" fill="currentColor" aria-hidden="true"><path d="M12 .5A11.5 11.5 0 0 0 .5 12.3c0 5.22 3.38 9.64 8.07 11.2.59.11.8-.26.8-.57v-2.2c-3.28.73-3.97-1.42-3.97-1.42-.53-1.38-1.3-1.75-1.3-1.75-1.06-.75.08-.73.08-.73 1.18.08 1.8 1.24 1.8 1.24 1.04 1.83 2.73 1.3 3.4.99.1-.78.4-1.3.74-1.6-2.62-.3-5.37-1.34-5.37-5.97 0-1.32.46-2.4 1.22-3.24-.12-.31-.53-1.56.12-3.25 0 0 1-.33 3.3 1.25a11.2 11.2 0 0 1 6 0c2.3-1.58 3.3-1.25 3.3-1.25.65 1.69.24 2.94.12 3.25.76.84 1.22 1.92 1.22 3.24 0 4.64-2.76 5.66-5.39 5.96.42.37.8 1.1.8 2.22v3.29c0 .31.21.69.81.57A11.51 11.51 0 0 0 23.5 12.3 11.5 11.5 0 0 0 12 .5Z" /></svg>
      </a>

      <button
        type="button"
        class="inline-flex cursor-pointer items-center justify-center rounded-md p-2 text-gray-700 transition-colors duration-200 hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 lg:hidden dark:text-gray-200 dark:hover:bg-white/10"
        :aria-expanded="menuOpen"
        aria-label="打开导航菜单"
        @click="menuOpen = !menuOpen"
      >
        <svg v-if="!menuOpen" viewBox="0 0 24 24" class="size-5" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round" /></svg>
        <svg v-else viewBox="0 0 24 24" class="size-5" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 6l12 12M18 6 6 18" stroke-linecap="round" /></svg>
      </button>
    </div>

    <div v-if="menuOpen" class="border-t border-gray-200 bg-white px-4 py-3 lg:hidden dark:border-white/10 dark:bg-gray-950">
      <button type="button" class="mb-3 flex w-full cursor-pointer items-center gap-2 rounded-lg border border-gray-200 px-3 py-2 text-sm text-gray-600 dark:border-white/10 dark:text-gray-300" @click="open = true; menuOpen = false">
        搜索文档
      </button>
      <NuxtLink v-for="item in nav" :key="item.to" :to="item.to" class="block cursor-pointer rounded-lg px-3 py-2 text-sm font-medium text-gray-800 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-white/10">{{ item.label }}</NuxtLink>
      <NuxtLink to="/plus" class="mt-1 block cursor-pointer rounded-lg px-3 py-2 text-sm font-semibold text-sky-600 dark:text-sky-300">Plus</NuxtLink>
      <p class="mt-3 px-3 text-xs text-gray-500">文档 {{ flatDocs.length }} 篇 · 博客 {{ blogPosts.length }} 篇</p>
    </div>
  </header>
</template>
