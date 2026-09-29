<script setup lang="ts">
const props = defineProps<{
  code: string
  lang?: string
  filename?: string
}>()

const copied = ref(false)

async function copy() {
  await navigator.clipboard.writeText(props.code)
  copied.value = true
  window.setTimeout(() => {
    copied.value = false
  }, 1600)
}

const html = computed(() => highlightCode(props.code, props.lang || 'html'))
</script>

<template>
  <div class="min-w-0 overflow-hidden rounded-2xl border border-gray-800 bg-gray-950 shadow-xl">
    <div class="flex items-center justify-between border-b border-white/10 px-4 py-2">
      <div class="flex items-center gap-2">
        <span class="size-2.5 rounded-full bg-white/15" />
        <span class="size-2.5 rounded-full bg-white/15" />
        <span class="size-2.5 rounded-full bg-white/15" />
        <span v-if="filename" class="ml-2 font-mono text-xs text-gray-400">{{ filename }}</span>
      </div>
      <button type="button" class="cursor-pointer rounded-md px-2 py-1 text-xs text-gray-300 transition-colors duration-200 hover:bg-white/10 hover:text-white focus-visible:outline-2 focus-visible:outline-sky-400" @click="copy">
        {{ copied ? '已复制' : '复制' }}
      </button>
    </div>
    <pre class="overflow-x-auto p-4 font-mono text-[13px] leading-6 text-gray-100"><code v-html="html" /></pre>
  </div>
</template>
