function escapeHtml(value: string) {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

export function highlightCode(code: string, lang = 'html') {
  if (lang === 'html' || lang === 'vue') {
    return code.replace(/<!--[\s\S]*?-->|<\/?[\w:-]+|[\w:-]+="[^"]*"|[^<]+/g, (token) => {
      if (token.startsWith('<!--')) return `<span class="text-gray-500">${escapeHtml(token)}</span>`
      if (token.startsWith('<')) {
        const matched = token.match(/^(<\/?)([\w:-]+)/)
        if (!matched) return escapeHtml(token)
        return `${escapeHtml(matched[1])}<span class="text-pink-400">${escapeHtml(matched[2])}</span>`
      }
      const attribute = token.match(/^([\w:-]+)(=")([^"]*)(")$/)
      if (attribute) {
        return `<span class="text-sky-300">${escapeHtml(attribute[1])}</span>=<span class="text-emerald-300">"${escapeHtml(attribute[3])}"</span>`
      }
      return escapeHtml(token)
    })
  }

  if (lang === 'css') {
    return code.replace(/\/\*[\s\S]*?\*\/|@[a-zA-Z-]+|[.#]?[a-zA-Z_-][\w-]*(?=\s*\{)|[\w-]+(?=\s*:)|[^{}\n]+/g, (token) => {
      if (token.startsWith('/*')) return `<span class="text-gray-500">${escapeHtml(token)}</span>`
      if (token.startsWith('@')) return `<span class="text-pink-400">${escapeHtml(token)}</span>`
      if (token.includes('{') || token.startsWith('.') || token.startsWith('#')) {
        return `<span class="text-sky-300">${escapeHtml(token)}</span>`
      }
      if (/^[\w-]+$/.test(token)) return `<span class="text-violet-300">${escapeHtml(token)}</span>`
      return escapeHtml(token)
    })
  }

  return escapeHtml(code).replace(/\b(import|export|from|const|return|function|default)\b/g, '<span class="text-pink-400">$1</span>')
}
