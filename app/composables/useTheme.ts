export type ThemeChoice = 'system' | 'light' | 'dark'

export function useTheme() {
  const theme = useState<ThemeChoice>('tw-theme', () => 'system')

  onMounted(() => {
    const saved = localStorage.getItem('tw-theme')
    if (saved === 'light' || saved === 'dark' || saved === 'system') {
      theme.value = saved
    }
  })

  watch(theme, (value) => {
    localStorage.setItem('tw-theme', value)
  })

  return theme
}
