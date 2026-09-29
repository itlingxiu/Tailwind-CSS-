<template>
  <div>
    <NuxtRouteAnnouncer />
    <AppHeader />
    <main>
      <slot />
    </main>
    <AppFooter />
    <SearchDialog />
  </div>
</template>
