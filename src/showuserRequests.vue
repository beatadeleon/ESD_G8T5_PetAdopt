<script setup>
import { auth } from './firebaseConfig';
</script>
<template>
    <div>
      <h1>User Adoption Requests</h1>
      <div v-if="isLoading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>
        <div class="card" v-for="application in adoptionRequests" :key="application.requestId">
          <h2>{{ application.pet }}</h2>
          <p>Name: {{ application.name }}</p>
          <p>Email: {{ application.email }}</p>
          <p>Status: {{ application.status }}</p>
          <!-- Add more details as needed -->
          <button v-if="application.status !== 'cancelled'" @click="cancelRequest(application.requestId)">Cancel Request</button>
          <router-link to="/booking" v-if="application.status === 'pending'">Book</router-link>


        </div>
      </div>
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'UserRequests',
    data() {
      return {
        isLoading: true,
        error: null,
        adoptionRequests: []
      };
    },
    async created() {
      try {
        const currentUser = auth.currentUser;
        if (!currentUser) {
          throw new Error('No user logged in');
        }
        const userId = currentUser.uid;
        const response = await fetch(`http://localhost:5110/adoptionRequests/userId/${userId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch adoption requests');
        }
        const data = await response.json();
        if (data.code === 200) {
          this.adoptionRequests = data.data;
        } else {
          throw new Error(data.message || 'Failed to fetch adoption requests');
        }
      } catch (error) {
        this.error = error.message;
      } finally {
        this.isLoading = false;
      }
    },
    methods: {
        async cancelRequest(requestId) {
            try {
                const response = await fetch('http://localhost:5100/cancel_request', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        requestId,
                        status: 'cancelled'
                    })
                });
                if (!response.ok) {
                    throw new Error('Failed to cancel request');
                }
                const data = await response.json();
                console.log(data);
                // Reload the page after successfully canceling the request
                window.location.reload();
            } catch (error) {
                console.error('Error cancelling request:', error);
                // Optionally show error message to user
            }
        }
    }
};

  
  </script>
  
  <style>
  .card {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
  }
  </style>
  