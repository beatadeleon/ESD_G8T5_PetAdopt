<script setup>
// import Header from './components/AppHeader.vue'
import Footer from './components/AppFooter.vue'
// import login from './auth/login.vue'

</script>
<template>
  <div>
    <!-- <Header /> -->
    <div>
      <main class="py-4">
        <router-view></router-view>
      </main>
    </div>
    <Footer />
  </div>
</template>

