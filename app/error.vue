<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps<{ error: NuxtError }>()

function goHome() {
  clearError({ redirect: '/' })
}
</script>

<template>
  <div class="grid min-h-screen place-items-center bg-white px-4 dark:bg-gray-950">
    <div class="max-w-md text-center">
      <p class="font-mono text-sm text-sky-600">{{ error.statusCode || 500 }}</p>
      <h1 class="mt-3 text-3xl font-semibold text-gray-950 dark:text-white">页面没有找到</h1>
      <p class="mt-3 text-sm leading-6 text-gray-600 dark:text-gray-300">{{ error.statusMessage || '这个地址不在中文站里。' }}</p>
      <button type="button" class="mt-6 cursor-pointer rounded-full bg-gray-950 px-4 py-2 text-sm font-semibold text-white dark:bg-white dark:text-gray-950" @click="goHome">回到首页</button>
    </div>
  </div>
</template>
