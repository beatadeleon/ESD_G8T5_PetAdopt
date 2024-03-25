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
    <button v-if="application.status === 'open'" @click="updateStatus(application, 'pending')">Move to Pending</button>
    <button v-if="application.status === 'pending'" @click="updateStatus(application, 'confirmed')">Confirm</button>
  </div>
</div>
</div>

</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const applications = ref([]);
const filteredApplications = ref([]);
const filteredStatus = ref('');

const fetchApplications = async (status) => {
  try {
    const response = await fetch(`http://localhost:5110/adoptionRequests/${status}`);
    if (response.ok) {
      const data = await response.json();
      applications.value = data.data || [];
      filteredApplications.value = applications.value;
      filteredStatus.value = status.charAt(0).toUpperCase() + status.slice(1);
    } else if (response.status === 404) {
      applications.value = [];
      filteredApplications.value = applications.value;
      filteredStatus.value = status.charAt(0).toUpperCase() + status.slice(1);
    } else {
      console.error('Failed to fetch applications:', response.statusText);
    }
  } catch (error) {
    console.error('Failed to fetch applications:', error);
  }
};



const filterApplications = (status) => {
  fetchApplications(status);
};

const updateStatus = async (application, status) => {
  try {
    const response = await fetch(`http://localhost:5400/accept_request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"application": application,
    "status": status})
    });

    if (response.ok) {
      console.log(`Successfully updated status of application ${application.requestId} to ${status}`);
      application.status = status;
      if (status === 'confirmed') {
        filteredApplications.value = filteredApplications.value.filter(app => app.status !== 'rejected');
      }
    } else {
      console.error('Failed to update status:', response.statusText);
    }
  } catch (error) {
    console.error('Failed to update status:', error);
  }
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
