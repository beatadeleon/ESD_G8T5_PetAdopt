<template>
    <div>
      <h1>Application Form</h1>
      <form @submit.prevent="submitApplication">
        <div>
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="formData.name" required>
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="formData.email" required>
        </div>
        <div>
          <label for="phone">Phone:</label>
          <input type="tel" id="phone" v-model="formData.phone" required>
        </div>
        <div>
          <label for="message">Message:</label>
          <textarea id="message" v-model="formData.message" rows="4"></textarea>
        </div>
        <div>
          <label for="pet">Select Pet:</label>
          <select id="pet" v-model="formData.pet" required>
            <option v-for="pet in petListings" :key="pet.name" :value="pet.name">{{ pet.name }}</option>
          </select>
        </div>
        <div>
          <button type="submit">Submit Application</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'; // Import ref from Vue
  import { ref as dbRef, getDatabase, onValue, push, set } from 'firebase/database'; // Import dbRef and other functions from firebase/database
  import { auth } from './firebaseConfig';

  const db = getDatabase();
  // Initialize an empty array to hold the pet listings
  const petListings = ref([]);
  
  // Reference to the 'petListings' node in the Firebase database
  const petListingsRef = dbRef(db, 'petListings');
  
  // Fetch the pet listings from the database
  onValue(petListingsRef, (snapshot) => {
    const data = snapshot.val();
    if (data) {
      // Convert the object of pet listings into an array
      petListings.value = Object.values(data);
    }
  });
  
  // Define the form data object
  const formData = ref({
    name: '',
    email: '',
    phone: '',
    message: '',
    pet: ''
  });
  

 // Define the submitApplication method and call adoption service
const submitApplication = async () => {
  const user = auth.currentUser;
  if (user) {
    const adoptionRequestRef = dbRef(db, 'adoptionRequests');
    const newRequestRef = push(adoptionRequestRef);
    
    // Prepare the data to be sent to the Flask server
    const requestData = {
      requestId: newRequestRef.key,
      userId: user.uid,
      name: formData.value.name,
      email: formData.value.email,
      phone: formData.value.phone,
      message: formData.value.message,
      pet: formData.value.pet
    };
    
    // Make an HTTP POST request to the Flask server
    const response = await fetch('http://localhost:5000/submit_application', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });

    if (response.ok) {
      // Reset form data after submission
      formData.value = {
        name: '',
        email: '',
        phone: '',
        message: '',
        pet: ''
      };
      console.log('Application submitted successfully!');
    } else {
      console.error('Failed to submit application:', response.statusText);
    }
  } else {
    console.log('User not logged in.');
  }
};
</script>
