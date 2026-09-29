<script setup lang="ts">
import docs from '~/data/docs.json'
import { blogPosts } from '~/data/site'

const open = useSearchOpen()
const query = ref('')
const active = ref(0)
const input = ref<HTMLInputElement | null>(null)

const entries = computed(() => {
  const docsEntries = docs.groups.flatMap((group) =>
    group.items.map((item) => ({
      title: item.title,
      href: `/docs/${item.slug}`,
      kind: group.title,
      text: docs.pages[item.slug as keyof typeof docs.pages]?.summary ?? '',
    })),
  )
  const posts = blogPosts.map((post) => ({
    title: post.title,
    href: `/blog/${post.slug}`,
    kind: '博客',
    text: post.description,
  }))
  return [...docsEntries, ...posts]
})

const results = computed(() => {
  const q = query.value.trim().toLowerCase()
  const list = q
    ? entries.value.filter((item) => `${item.title} ${item.text} ${item.kind}`.toLowerCase().includes(q))
    : entries.value.slice(0, 8)
  return list.slice(0, 12)
})

watch(open, async (value) => {
  if (!value) return
  query.value = ''
  active.value = 0
  await nextTick()
  input.value?.focus()
})

watch(results, () => {
  active.value = 0
})

function close() {
  open.value = false
}

function go(index = active.value) {
  const item = results.value[index]
  if (!item) return
  close()
  navigateTo(item.href)
}

function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape') close()
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    active.value = Math.min(active.value + 1, results.value.length - 1)
  }
  if (event.key === 'ArrowUp') {
    event.preventDefault()
    active.value = Math.max(active.value - 1, 0)
  }
  if (event.key === 'Enter') {
    event.preventDefault()
    go()
  }
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-50 flex items-start justify-center px-4 pt-[12vh]" @keydown="onKey">
      <button type="button" class="absolute inset-0 cursor-pointer bg-gray-950/60" aria-label="关闭搜索" @click="close" />
      <div class="relative w-full max-w-xl overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-2xl dark:border-white/10 dark:bg-gray-900" role="dialog" aria-modal="true" aria-label="搜索文档">
        <div class="flex items-center gap-3 border-b border-gray-200 px-4 dark:border-white/10">
          <svg viewBox="0 0 20 20" class="size-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.25" /><path d="M12.5 12.5 17 17" stroke-linecap="round" /></svg>
          <input
            ref="input"
            v-model="query"
            type="search"
            placeholder="搜索文档、类名或文章"
            class="h-12 w-full bg-transparent text-sm text-gray-950 outline-none placeholder:text-gray-400 dark:text-white"
            aria-label="搜索"
          />
        </div>
        <ul class="max-h-80 overflow-auto p-2" role="listbox">
          <li v-if="results.length === 0" class="px-3 py-8 text-center text-sm text-gray-500">没有匹配结果</li>
          <li v-for="(item, index) in results" :key="item.href">
            <button
              type="button"
              class="flex w-full cursor-pointer flex-col rounded-lg px-3 py-2 text-left transition-colors duration-200 focus-visible:outline-2 focus-visible:outline-sky-500"
              :class="index === active ? 'bg-sky-50 dark:bg-white/10' : 'hover:bg-gray-50 dark:hover:bg-white/5'"
              role="option"
              :aria-selected="index === active"
              @mouseenter="active = index"
              @click="go(index)"
            >
              <span class="text-sm font-medium text-gray-950 dark:text-white">{{ item.title }}</span>
              <span class="text-xs text-gray-500">{{ item.kind }}</span>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </Teleport>
</template>
