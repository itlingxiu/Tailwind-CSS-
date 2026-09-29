<script setup lang="ts">
const theme = useTheme()
const prefersDark = ref(false)

onMounted(() => {
  const media = window.matchMedia('(prefers-color-scheme: dark)')
  prefersDark.value = media.matches
  const onChange = (event: MediaQueryListEvent) => {
    prefersDark.value = event.matches
  }
  media.addEventListener('change', onChange)
  onUnmounted(() => media.removeEventListener('change', onChange))
})

const isDark = computed(() => theme.value === 'dark' || (theme.value === 'system' && prefersDark.value))

useHead({
  htmlAttrs: {
    class: computed(() => (isDark.value ? 'dark' : '')),
  },
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
