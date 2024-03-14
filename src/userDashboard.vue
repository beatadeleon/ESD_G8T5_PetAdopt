<template>
  <div>
    <div class="application-form-link">
      <router-link to="/applicationForm">Apply Now</router-link>
    </div>
    <div class="pet-card-container">
      <div class="pet-card" v-for="pet in petData" :key="pet.name">
        <h2>{{ pet.name }}</h2>
        <img :src="pet.image" alt="Pet Image" style="max-width: 100%;">
        <p>Species: {{ pet.species }}</p>
        <p>Age: {{ pet.age }}</p>
        <p>Breed: {{ pet.breed }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();

// Initialize petData as a ref
const petData = ref([]);

// Fetch pet listings data from the microservice
async function fetchPetListings() {
  try {
    const response = await fetch('http://localhost:8082/petListings');
    if (!response.ok) {
      throw new Error('Failed to fetch pet listings');
    }
    const data = await response.json();
    petData.value = data.data;
  } catch (error) {
    console.error('Error fetching pet listings:', error);
  }
}

fetchPetListings();
</script>

<style>
.application-form-link {
  text-align: center;
  margin-bottom: 20px;
}

.pet-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.pet-card {
  width: calc(25% - 10px); /* Adjust the width based on the number of cards per row */
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
}

/* Adjust the card style as needed */
.pet-card img {
  width: 100%;
  height: auto;
}
</style>