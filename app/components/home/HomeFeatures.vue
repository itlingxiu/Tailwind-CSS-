<script setup lang="ts">
const breakpoint = ref<'mobile' | 'sm' | 'md' | 'lg' | 'xl'>('md')
const breakpoints = ['mobile', 'sm', 'md', 'lg', 'xl'] as const
const expanded = ref(false)

const layoutClass = computed(() => {
  if (breakpoint.value === 'mobile') return 'grid-cols-1'
  if (breakpoint.value === 'sm') return 'grid-cols-1'
  return 'grid-cols-[180px_1fr]'
})

const filters = reactive({
  'blur-sm': false,
  'brightness-125': false,
  grayscale: false,
  'contrast-125': false,
  'saturate-150': false,
  sepia: false,
})
const filterClass = computed(() => Object.entries(filters).filter(([, on]) => on).map(([name]) => name).join(' '))

const darkCard = ref(true)
const hue = ref('sky')
const hues = ['red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan', 'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose']
const shades = [950, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50]
const hueAngle: Record<string, number> = {
  red: 25, orange: 55, amber: 80, yellow: 100, lime: 125, green: 145, emerald: 165, teal: 185, cyan: 205, sky: 230, blue: 255, indigo: 275, violet: 295, purple: 310, fuchsia: 330, pink: 355, rose: 12,
}
const shadeStop: Record<number, [number, number]> = {
  50: [0.97, 0.02], 100: [0.94, 0.045], 200: [0.9, 0.08], 300: [0.84, 0.11], 400: [0.74, 0.14], 500: [0.64, 0.15], 600: [0.55, 0.13], 700: [0.46, 0.11], 800: [0.39, 0.09], 900: [0.32, 0.07], 950: [0.24, 0.05],
}
function swatch(name: string, shade: number) {
  const [lightness, chroma] = shadeStop[shade]
  return `oklch(${lightness} ${chroma} ${hueAngle[name]})`
}

const category = ref('全部')
const places = [
  { name: '树屋', place: '莫干山', kind: '树屋', tone: 'from-emerald-400 to-lime-600' },
  { name: '湖畔小屋', place: '千岛湖', kind: '湖滨', tone: 'from-sky-400 to-blue-700' },
  { name: '设计师住宅', place: '上海', kind: '设计', tone: 'from-stone-300 to-stone-600' },
  { name: '山间庄园', place: '大理', kind: '庄园', tone: 'from-amber-300 to-orange-600' },
]
const visiblePlaces = computed(() => category.value === '全部' ? places : places.filter((item) => item.kind === category.value))

const easing = ref('ease-out')
const easings = ['linear', 'ease-out', 'ease-in-out', 'ease-in']
const moved = ref(false)

const direction = ref<'ltr' | 'rtl'>('ltr')
const containerWidth = ref(520)
const rotateX = ref(12)
const rotateY = ref(-18)

const themeCode = `@theme {
  --font-sans: "Inter", sans-serif;
  --font-mono: "IBM Plex Mono", monospace;
  --color-mint-500: oklch(0.7 0.18 145);
  --color-mint-700: oklch(0.5 0.14 145);
}`

const layerCode = `@layer theme, base, components, utilities;

@layer theme {
  :root { /* 主题变量 */ }
}
@layer base { /* Preflight */ }
@layer components { /* 你的组件 */ }
@layer utilities { /* 实用类 */ }`
</script>

<template>
  <section class="border-t border-gray-200 py-20 dark:border-white/10">
    <div class="mx-auto max-w-[90rem] px-4 sm:px-6 lg:px-8">
      <p class="text-sm font-semibold tracking-[0.2em] text-gray-500">为什么是 Tailwind CSS</p>
      <h2 class="mt-3 max-w-3xl text-4xl font-medium tracking-tight text-balance text-gray-950 sm:text-5xl dark:text-white">为现代 Web 而做。</h2>
      <p class="mt-4 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">
        Tailwind 直接使用现在的 CSS 能力：断点、深色模式、变量、网格、容器查询、滤镜和三维变换，都变成可以组合的类。
      </p>

      <div class="mt-16 space-y-20">
        <article class="grid items-center gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">响应式设计</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">在任意实用类前面加上屏幕尺寸，它就只在那个断点及以上生效。先写手机，再往上加。</p>
          </div>
          <div class="rounded-2xl border border-gray-200 bg-gray-50 p-4 dark:border-white/10 dark:bg-white/5">
            <div class="flex flex-wrap gap-2" role="tablist" aria-label="断点">
              <button v-for="item in breakpoints" :key="item" type="button" class="cursor-pointer rounded-full px-3 py-1 text-xs font-semibold transition-colors duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500" :class="breakpoint === item ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'bg-white text-gray-600 hover:bg-gray-100 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800'" @click="breakpoint = item">
                {{ item === 'mobile' ? '手机' : item }}
              </button>
            </div>
            <div class="mt-4 grid gap-4 rounded-xl bg-white p-4 dark:bg-gray-950" :class="layoutClass">
              <div class="h-36 rounded-lg bg-gradient-to-br from-sky-300 to-indigo-600" />
              <div>
                <p class="text-xs text-gray-500">整栋小屋</p>
                <h4 class="text-lg font-semibold text-gray-950 dark:text-white">湖畔小屋</h4>
                <p class="mt-1 text-sm text-gray-600 dark:text-gray-300">2.66 · 128 条评价 · 湾田</p>
                <p class="mt-3 text-sm leading-6 text-gray-600 dark:text-gray-300">
                  这间向阳的房间适合轻装出行，晚上可以舒服地睡一觉。
                  <button v-if="!expanded" type="button" class="cursor-pointer font-medium text-sky-600" @click="expanded = true">展开</button>
                  <span v-else>窗外就是湖面，厨房虽然小，但够煮一壶咖啡。</span>
                </p>
                <button type="button" class="mt-4 cursor-pointer rounded-full bg-gray-950 px-3 py-1.5 text-xs font-semibold text-white dark:bg-white dark:text-gray-950">查看可订日期</button>
              </div>
            </div>
          </div>
        </article>

        <article class="grid items-center gap-8 lg:grid-cols-2">
          <div class="lg:order-2">
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">滤镜</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">背景模糊、亮度、灰度、对比度、饱和度和棕褐可以叠在一起，直到设计师叫停。</p>
          </div>
          <div class="rounded-2xl border border-gray-200 p-4 dark:border-white/10">
            <div class="grid h-52 place-items-center overflow-hidden rounded-xl bg-[radial-gradient(circle_at_30%_20%,#7dd3fc,transparent_40%),radial-gradient(circle_at_70%_60%,#c084fc,transparent_45%),linear-gradient(#111827,#312e81)]">
              <div class="size-28 rounded-2xl bg-white/80 shadow-xl" :class="filterClass" />
            </div>
            <div class="mt-3 flex flex-wrap gap-2">
              <button v-for="(on, name) in filters" :key="name" type="button" class="cursor-pointer rounded-full border px-3 py-1 font-mono text-xs transition-colors duration-200" :class="on ? 'border-sky-500 bg-sky-50 text-sky-700 dark:bg-sky-400/10 dark:text-sky-300' : 'border-gray-200 text-gray-600 dark:border-white/10 dark:text-gray-300'" @click="filters[name] = !on">
                {{ name }}
              </button>
            </div>
          </div>
        </article>

        <article class="grid items-center gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">深色模式</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">不想刺眼时，在颜色类前加上 <code class="font-mono text-sky-600 dark:text-sky-400">dark:</code>。页脚还可以在系统、浅色和深色之间切换整站。</p>
          </div>
          <div class="rounded-2xl border border-gray-200 p-4 dark:border-white/10">
            <button type="button" class="cursor-pointer rounded-full bg-gray-950 px-3 py-1.5 text-xs font-semibold text-white dark:bg-white dark:text-gray-950" @click="darkCard = !darkCard">
              {{ darkCard ? '查看浅色' : '查看深色' }}
            </button>
            <div class="mt-4 rounded-xl p-5 transition-colors duration-200" :class="darkCard ? 'bg-gray-950 text-white' : 'bg-white text-gray-950 ring-1 ring-gray-200'">
              <p class="text-sm text-sky-400">夜间模式</p>
              <p class="mt-2 text-2xl font-medium">把亮度留给内容。</p>
              <p class="mt-2 text-sm" :class="darkCard ? 'text-gray-300' : 'text-gray-600'">边框、正文和次要说明需要分别设色，而不是整体反相。</p>
            </div>
          </div>
        </article>

        <article class="grid items-start gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">CSS 变量</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">改主题就是声明几条变量。字族、字号和颜色都会变成对应的实用类。</p>
          </div>
          <CodeBlock :code="themeCode" lang="css" filename="app.css" />
        </article>

        <article>
          <h3 class="text-xl font-semibold text-gray-950 dark:text-white">广色域调色板</h3>
          <p class="mt-3 max-w-2xl text-base leading-7 text-gray-600 dark:text-gray-300">默认颜色更鲜艳。你只要选色相和深浅，不必理解 oklch。</p>
          <div class="mt-6 flex gap-2 overflow-x-auto pb-2">
            <button v-for="item in hues" :key="item" type="button" class="cursor-pointer rounded-full px-3 py-1 text-xs font-semibold capitalize transition-colors duration-200" :class="hue === item ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'bg-gray-100 text-gray-700 dark:bg-white/10 dark:text-gray-200'" @click="hue = item">{{ item }}</button>
          </div>
          <div class="mt-4 grid grid-cols-11 overflow-hidden rounded-2xl">
            <div v-for="shade in shades" :key="shade" class="flex h-16 items-end justify-center pb-1 text-[10px] sm:h-24" :class="shade > 400 ? 'text-white' : 'text-gray-950'" :style="{ backgroundColor: swatch(hue, shade) }">{{ shade }}</div>
          </div>
        </article>

        <article class="grid items-start gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">网格布局</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">列数直接写在 HTML 上，复杂版面也容易推敲。点分类，看卡片如何重排。</p>
          </div>
          <div>
            <div class="flex flex-wrap gap-2">
              <button v-for="item in ['全部', '树屋', '湖滨', '设计', '庄园']" :key="item" type="button" class="cursor-pointer rounded-full px-3 py-1 text-xs font-semibold transition-colors duration-200" :class="category === item ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'bg-gray-100 text-gray-700 dark:bg-white/10 dark:text-gray-200'" @click="category = item">{{ item }}</button>
            </div>
            <div class="mt-4 grid gap-3 sm:grid-cols-2">
              <article v-for="item in visiblePlaces" :key="item.name" class="overflow-hidden rounded-2xl border border-gray-200 bg-white dark:border-white/10 dark:bg-gray-900">
                <div class="h-24 bg-gradient-to-br" :class="item.tone" />
                <div class="p-3">
                  <h4 class="font-semibold text-gray-950 dark:text-white">{{ item.name }}</h4>
                  <p class="text-sm text-gray-500">{{ item.place }}</p>
                </div>
              </article>
            </div>
          </div>
        </article>

        <article class="grid items-center gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">过渡与动画</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">加上时长和速度曲线就够了。界面反馈保持在几百毫秒内。</p>
          </div>
          <div class="rounded-2xl border border-gray-200 p-4 dark:border-white/10">
            <div class="flex flex-wrap gap-2">
              <button v-for="item in easings" :key="item" type="button" class="cursor-pointer rounded-full px-3 py-1 font-mono text-xs transition-colors duration-200" :class="easing === item ? 'bg-sky-500 text-white' : 'bg-gray-100 text-gray-700 dark:bg-white/10 dark:text-gray-200'" @click="easing = item; moved = false">{{ item }}</button>
            </div>
            <button type="button" class="mt-4 w-full cursor-pointer" @click="moved = !moved">
              <span class="relative block h-12 rounded-full bg-gray-100 dark:bg-white/10">
                <span class="absolute top-1 size-10 rounded-full bg-sky-500 transition duration-700" :class="[easing, moved ? 'left-[calc(100%-2.75rem)]' : 'left-1']" />
              </span>
            </button>
          </div>
        </article>

        <article class="grid items-start gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">级联层</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">样式被放进 theme、base、components、utilities。实用类位于最上层，你很少再和选择器优先级较劲。</p>
          </div>
          <CodeBlock :code="layerCode" lang="css" filename="app.css" />
        </article>

        <article class="grid items-center gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">逻辑属性</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">用起始边和结束边代替写死的左右，从左到右和从右到左可以共用一套间距。</p>
          </div>
          <div class="rounded-2xl border border-gray-200 p-4 dark:border-white/10" :dir="direction">
            <div class="flex gap-2">
              <button type="button" class="cursor-pointer rounded-full px-3 py-1 text-xs font-semibold" :class="direction === 'ltr' ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'bg-gray-100 dark:bg-white/10'" @click="direction = 'ltr'">从左到右</button>
              <button type="button" class="cursor-pointer rounded-full px-3 py-1 text-xs font-semibold" :class="direction === 'rtl' ? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950' : 'bg-gray-100 dark:bg-white/10'" @click="direction = 'rtl'">从右到左</button>
            </div>
            <div class="mt-4 rounded-xl bg-gray-50 ps-6 dark:bg-white/5">
              <div class="border-s-4 border-sky-500 py-4 pe-4">
                <p class="font-semibold text-gray-950 dark:text-white">{{ direction === 'ltr' ? 'Will Winton' : 'سارة أحمد' }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-300">{{ direction === 'ltr' ? '运营总监' : '项目经理' }}</p>
              </div>
            </div>
          </div>
        </article>

        <article class="grid items-center gap-8 lg:grid-cols-2">
          <div class="lg:order-2">
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">容器查询</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">把元素标成容器后，子元素按容器宽度而不是窗口宽度变化。拖动滑块看看列数。</p>
          </div>
          <div>
            <label class="flex items-center justify-between text-xs text-gray-500" for="container-width">容器宽度 {{ containerWidth }}px</label>
            <input id="container-width" v-model.number="containerWidth" class="mt-2 w-full accent-sky-500" type="range" min="240" max="720" />
            <div class="@container mt-3 overflow-hidden rounded-2xl border border-gray-200 p-3 dark:border-white/10" :style="{ width: `${containerWidth}px`, maxWidth: '100%' }">
              <div class="grid grid-cols-1 gap-2 @min-[420px]:grid-cols-2">
                <div v-for="n in 4" :key="n" class="aspect-square rounded-lg bg-gradient-to-br from-sky-400 to-indigo-600 @min-[420px]:aspect-3/2" />
              </div>
            </div>
          </div>
        </article>

        <article class="overflow-hidden rounded-3xl bg-gradient-to-br from-sky-500 via-indigo-600 to-fuchsia-600 p-8 text-white sm:p-12">
          <p class="text-sm font-semibold text-white/80">渐变</p>
          <h3 class="mt-3 max-w-xl text-3xl font-medium tracking-tight sm:text-4xl">重新定义实时性能</h3>
          <p class="mt-3 max-w-xl text-sm leading-6 text-white/85">不必记住那串渐变语法。几个类就能铺开平滑的颜色。</p>
          <dl class="mt-8 grid gap-4 sm:grid-cols-3">
            <div v-for="item in [{ k: '渲染耗时', v: '6.4x' }, { k: '实时帧率', v: '4.2x' }, { k: '多平台构建', v: '2.7x' }]" :key="item.k" class="rounded-2xl bg-white/15 p-4 backdrop-blur-md">
              <dt class="text-xs text-white/80">{{ item.k }}</dt>
              <dd class="mt-2 text-3xl font-semibold tabular-nums">{{ item.v }}</dd>
            </div>
          </dl>
        </article>

        <article class="grid items-center gap-8 lg:grid-cols-2">
          <div>
            <h3 class="text-xl font-semibold text-gray-950 dark:text-white">三维变换</h3>
            <p class="mt-3 text-base leading-7 text-gray-600 dark:text-gray-300">两个轴不够时，再绕 X 和 Y 转一下。拖动滑块，卡片会在透视里倾斜。</p>
          </div>
          <div>
            <div class="grid h-56 place-items-center [perspective:900px]">
              <div class="w-56 rounded-2xl bg-gray-950 p-5 text-white shadow-2xl transition-transform duration-200 dark:bg-white dark:text-gray-950" :style="{ transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg)` }">
                <p class="text-xs text-sky-400 dark:text-sky-600">rotate-x / rotate-y</p>
                <p class="mt-3 text-xl font-semibold">有一点深度就够了。</p>
              </div>
            </div>
            <label class="mt-2 block text-xs text-gray-500" for="rx">rotateX {{ rotateX }}</label>
            <input id="rx" v-model.number="rotateX" class="w-full accent-sky-500" type="range" min="-40" max="40" />
            <label class="mt-2 block text-xs text-gray-500" for="ry">rotateY {{ rotateY }}</label>
            <input id="ry" v-model.number="rotateY" class="w-full accent-sky-500" type="range" min="-40" max="40" />
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
