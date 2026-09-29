<script setup lang="ts">
import { blogPosts } from '~/data/site'

const route = useRoute()
const post = computed(() => blogPosts.find((item) => item.slug === route.params.slug))

if (!post.value) {
  throw createError({ statusCode: 404, statusMessage: '没有这篇文章' })
}

useSeoMeta({
  title: () => post.value ? `${post.value.title} · Tailwind CSS 博客` : '博客',
  description: () => post.value?.description,
})
</script>

<template>
  <article v-if="post" class="mx-auto max-w-3xl px-4 py-16 sm:px-6">
    <NuxtLink to="/blog" class="cursor-pointer text-sm font-medium text-sky-600 dark:text-sky-400">返回博客</NuxtLink>
    <p class="mt-6 text-sm text-gray-500">{{ post.date }} · {{ post.author }} · {{ post.minutes }} 分钟</p>
    <h1 class="mt-3 text-4xl font-semibold tracking-tight text-balance text-gray-950 dark:text-white">{{ post.title }}</h1>
    <p class="mt-4 text-lg leading-8 text-gray-600 dark:text-gray-300">{{ post.description }}</p>
    <div class="mt-8 space-y-5 text-base leading-8 text-gray-700 dark:text-gray-200">
      <p v-for="(paragraph, index) in post.body" :key="index">{{ paragraph }}</p>
    </div>
  </article>
</template>
