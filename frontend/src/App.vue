<template>
  <div>
    <PageHeader/>
    <router-view />
    <PageFooter v-if="!$route.meta.hideFooter" />
  </div>
</template>

<style>
  @import "@/assets/sass/index.scss";
</style>

<script setup>
  import PageHeader from '@/components/PageHeader.vue';
  import PageFooter from '@/components/PageFooter.vue';
  

</script>

