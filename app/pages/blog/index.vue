<script setup lang="ts">
import { blogPosts } from '~/data/site'

useSeoMeta({
  title: '博客 · Tailwind CSS',
  description: '关于 Tailwind CSS v4、主题变量、深色模式和构建体积的中文说明。',
})
</script>

<template>
  <div class="mx-auto max-w-5xl px-4 py-16 sm:px-6">
    <p class="text-sm font-semibold tracking-[0.18em] text-gray-500">博客</p>
    <h1 class="mt-3 text-4xl font-medium tracking-tight text-gray-950 sm:text-5xl dark:text-white">写给正在用实用类的人。</h1>
    <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">这些文章用中文解释 v4 的工作方式。它们是学习笔记，不是 Tailwind Labs 官方博客的译文。</p>
    <div class="mt-10 divide-y divide-gray-200 border-y border-gray-200 dark:divide-white/10 dark:border-white/10">
      <NuxtLink v-for="post in blogPosts" :key="post.slug" :to="`/blog/${post.slug}`" class="grid cursor-pointer gap-2 py-6 transition-colors duration-200 hover:bg-gray-50 sm:grid-cols-[8rem_1fr] sm:gap-6 dark:hover:bg-white/5">
        <time class="text-sm text-gray-500" :datetime="post.date">{{ post.date }}</time>
        <div>
          <p class="text-xs font-semibold text-sky-600 dark:text-sky-400">{{ post.tag }}</p>
          <h2 class="mt-1 text-xl font-semibold text-gray-950 dark:text-white">{{ post.title }}</h2>
          <p class="mt-2 text-sm leading-6 text-gray-600 dark:text-gray-300">{{ post.description }}</p>
        </div>
      </NuxtLink>
    </div>
  </div>
</template>
