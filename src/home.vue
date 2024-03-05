<script setup>
import { useRouter } from 'vue-router'
import { auth, database } from './firebaseConfig'; // Import auth from firebaseConfig
import { ref, get } from 'firebase/database';
import { useStore } from 'vuex'
import { computed } from 'vue'


const store = useStore()
const router = useRouter()

auth.onAuthStateChanged((user) => {
  store.dispatch('fetchUser', user)
})

const user = computed(() => {
  return store.getters.user
  
})

</script>

<template>
  <div>
    <h1>Welcome to PetAdopt</h1>

    <!-- Conditional rendering based on user role -->
    <div v-if="userRole !== null">
      <p v-if="isUser">
        <h1 class="mt-3">
          Hi <span style="text-transform: uppercase;">{{ user.data.displayName }}</span>,
          Adopt a pet today!
        </h1>
        <router-link to="/userDashboard">
          <button>User Dashboard</button>
        </router-link>
      </p>
      <p v-else-if="isAdmin">
        <router-link to="/adminDashboard">
          <button>Admin Dashboard</button>
        </router-link>
      </p>
    </div>
    
    
    <!-- Default route for unauthorized users -->
    <router-link v-else to="/auth/login">
      <button>Go to Dashboard</button>
    </router-link>
  </div>
</template>




<script>
  import { auth as firebaseAuth, database as firebaseDatabase } from './firebaseConfig'; 
  import { ref, get, update } from 'firebase/database';
 

  export default {
    name: 'HomeComponent',
    data() {
        return {
          userRole: null,
        };
    },
  mounted() {
        this.fetchUserRole();
    },
    computed: {
        isUser() {
            return this.userRole === 'user';
        },
        isAdmin() {
            return this.userRole === 'admin';
        },

    },
    methods: {
  fetchUserRole() {
    firebaseAuth.onAuthStateChanged((user) => {
      if (user && user.uid) { // Check if user is not null and has a UID
        const userRef = ref(firebaseDatabase, `users/${user.uid}/role`);
        get(userRef)
          .then((snapshot) => {
            this.userRole = snapshot.val();
            //console.log("User Role from Database:", this.userRole);
          })
          .catch((error) => {
            //console.error("Error fetching user role:", error);
          });
      } else {
        // Handle the case when user is null or undefined
        // For example, you can redirect the user to the login page
        this.userRole = null;
      }
    });
  },
}


}
</script>