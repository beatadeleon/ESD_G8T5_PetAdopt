<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <h1>All open applications</h1>
  <div class="card-container">
    <div v-for="application in openApplications" :key="application.requestId" class="card">
      <h2>{{ application.name }}</h2>
      <p><strong>Email:</strong> {{ application.email }}</p>
      <p><strong>Phone:</strong> {{ application.phone }}</p>
      <p><strong>Pet:</strong> {{ application.pet }}</p>
      <p><strong>Message:</strong> {{ application.message }}</p>
      <button>Click</button>
    </div>
  </div>
</template>



<script>

export default {
  name: 'AdminDashboardComponent',
  data() {
    return {
      openApplications: [],
    };
  },
  mounted() {
    this.fetchOpenApplications();
  },
  methods: {
    async fetchOpenApplications() {
      try {
        const response = await fetch('http://localhost:5110/adoptionRequests/open');
        if (!response.ok) {
          throw new Error('Failed to fetch open applications');
        }
        const data = await response.json();
        this.openApplications = data.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>


<style scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.card {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 20px;
  width: 300px;
}

.card h2 {
  margin-top: 0;
}

.card p {
  margin: 0;
  margin-bottom: 10px;
}
</style>