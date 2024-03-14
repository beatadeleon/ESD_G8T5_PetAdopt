<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div>
    <h1>All Applications</h1>
    <div>
      <button @click="filterApplications('open')">Open</button>
      <button @click="filterApplications('pending')">Pending</button>
      <button @click="filterApplications('confirmed')">Confirmed</button>
      <button @click="filterApplications('rejected')">Rejected</button>
    </div>
    <h2>{{ filteredStatus }}</h2>
    <div class="card-container">
      <div v-for="application in filteredApplications" :key="application.requestId" class="card">
        <h2>{{ application.name }}</h2>
        <p><strong>Email:</strong> {{ application.email }}</p>
        <p><strong>Phone:</strong> {{ application.phone }}</p>
        <p><strong>Pet:</strong> {{ application.pet }}</p>
        <p><strong>Message:</strong> {{ application.message }}</p>
        <button @click="updateStatus(application, 'pending')">Update Status</button>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  name: 'AdminDashboardComponent',
  data() {
    return {
      applications: [],
      filteredApplications: [],
      filteredStatus: 'All Applications',
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
        this.applications = data.data;
        this.filteredApplications = this.applications;
      } catch (error) {
        console.error(error);
      }
    },
    filterApplications(status) {
      if (status === 'all') {
        this.filteredApplications = this.applications;
        this.filteredStatus = 'All Applications';
      } else {
        this.filteredApplications = this.applications.filter(application => application.status === status);
        this.filteredStatus = status.charAt(0).toUpperCase() + status.slice(1);
      }
    },
    async updateStatus(application, status) {
      // Code to update application status
      console.log(`Updating status of application ${application.requestId} to ${status}`);
    }
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