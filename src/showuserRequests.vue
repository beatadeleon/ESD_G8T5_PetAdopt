<script setup>
import { auth } from './firebaseConfig';
</script>
<template>
    <div>
      <h1>User Adoption Requests</h1>
      <div v-if="isLoading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>
        <div class="card" v-for="request in adoptionRequests" :key="request.requestId">
          <h2>{{ request.pet }}</h2>
          <p>Name: {{ request.name }}</p>
          <p>Email: {{ request.email }}</p>
          <p>Message: {{request.message}}</p>
          <p>Status: {{ request.status }}</p>
          <!-- Add more details as needed -->
          <button v-if="request.status =='pending' || request.status == 'open'" @click="cancelRequest(request)" class="cancel-button">Cancel Request</button>
          <router-link to="/booking" v-if="request.status === 'pending'" class="button-link">Book</router-link>


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
          throw new Error('No adoption requests found.');
        }
        const data = await response.json();
        if (data.code === 200) {
          this.adoptionRequests = data.data;
          console.log(this.adoptionRequests)
        } else {
          throw new Error(data.message || 'No adoption requests found.');
        }
      } catch (error) {
        this.error = error.message;
      } finally {
        this.isLoading = false;
      }
    },
    methods: {
      async cancelRequest(request) {
        try {
          const currentUser = auth.currentUser;

          const response = await fetch('http://localhost:5100/cancel_request', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(
              {"request": request}
            )

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
  .button-link {
  display: inline-block;
  padding: 10px 20px;
  background-color: rgb(74, 213, 109);
  color: #fff;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
  .cancel-button {
  display: inline-block;
  margin-right: 10px;
  padding: 10px 20px;
  background-color: rgb(228, 62, 98);
  color: #fff;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.button-link:hover {
  background-color: rgb(7, 186, 51);
}
.cancel-button:hover {
  background-color: rgb(232, 4, 4);
}
  </style>
  