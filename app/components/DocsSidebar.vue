<script setup lang="ts">
import docs from '~/data/docs.json'

const route = useRoute()
const open = defineModel<boolean>({ default: false })

const current = computed(() => {
  const slug = route.params.slug
  return Array.isArray(slug) ? slug.join('/') : (slug ? String(slug) : '')
})
</script>

<template>
  <nav aria-label="文档目录">
    <div class="space-y-8">
      <div v-for="group in docs.groups" :key="group.title">
        <h2 class="px-3 text-sm font-semibold text-gray-950 dark:text-white">{{ group.title }}</h2>
        <ul class="mt-2 space-y-0.5">
          <li v-for="item in group.items" :key="item.slug">
            <NuxtLink
              :to="`/docs/${item.slug}`"
              class="block cursor-pointer rounded-lg px-3 py-1.5 text-sm transition-colors duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500"
              :class="current === item.slug ? 'bg-gray-100 font-medium text-gray-950 dark:bg-white/10 dark:text-white' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-950 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-white'"
              @click="open = false"
            >
              {{ item.title }}
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
