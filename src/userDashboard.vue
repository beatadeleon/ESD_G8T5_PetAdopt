<template>
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
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue'; // Import ref from Vue
import { getDatabase, ref as dbRef, onValue } from 'firebase/database'; // Import getDatabase and ref from firebase/database

const router = useRouter();

const db = getDatabase();

// Define the reference path to your pet listings in the database
const petListingsRef = dbRef(db, 'petListings');

// Initialize petData as a ref
const petData = ref([]);

// Fetch pet listings data from Firebase Realtime Database
onValue(petListingsRef, (snapshot) => {
  const data = snapshot.val();
  if (data) {
    // Convert the data object to an array
    const petList = Object.values(data);
    // Update the petData ref with the fetched pet listings
    petData.value = petList;
  } else {
    petData.value = [];
  }
});
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
