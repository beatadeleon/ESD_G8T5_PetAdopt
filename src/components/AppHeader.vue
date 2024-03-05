<script setup>
import { getCurrentScope} from 'vue'

console.log(getCurrentScope())


</script>

<template>
    <router-link v-if="isUser" to="/dashboard"></router-link>
    <router-link v-else to="/auth/register"></router-link>


</template>



<script>
import { auth, database } from '../firebaseConfig';
import { ref, get } from 'firebase/database';
// import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
// import { useDatabaseList } from 'vuefire'


// const foodEvents = useDatabaseList(ref(database, "foodEvent"));
// const crowdfunding = useDatabaseList(ref(database, "crowdfundingEvent"));
// console.log(foodEvents)

export default {
  data() {
    return {
      userRole: null,
      // store: useStore(),
      router: useRouter(),

      currentTime: new Date().getTime(),
      // firebaseFoodEvents: foodEvents,
      // firebaseCrowdfundEvents: crowdfunding,
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
      auth.onAuthStateChanged((user) => {
        if (user && user.uid) { // Null check added here
          const userRef = ref(database, `users/${user.uid}/role`);
          get(userRef)
            .then((snapshot) => {
              this.userRole = snapshot.val();
              console.log("User Role from Database:", this.userRole);
            })
            .catch((error) => {
              console.error("Error fetching user role:", error);
            });
        } else {
          // Handle the case where the user or user.uid is null
          console.log("User or user UID is null");
        }
  });
},

  },
    async signOut() {
      await this.store.dispatch('logoutUser');
      this.router.push('/');
    },
  };
</script>


