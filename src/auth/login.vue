<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref(null)

const store = useStore()
const router = useRouter()

const Login = async () => {
  try {
    await store.dispatch('loginUser', {
      email: email.value,
      password: password.value
    })
    router.push('/') // Redirect to the desired route after successful login
  } catch (err) {
    error.value = err.message
  }
}


// const signInWithGoogle = async () => {
//   try {
//     await store.dispatch('signInWithGoogle',{
//       role: 'user',
//     });
//     router.push('/');
//   } catch (err) {
//     error.value = err.message;
//   }
// };
</script>
<template>
  
  <div class="container">
    <br/>
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="card">
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <h4 class="card-header text-center">Login</h4>
            <form @submit.prevent="Login">
              <div class="mb-3">
                <label for="email" class="col-md-5 py-2 col-form-label">Email</label>
                <input
                  id="email"
                  type="email"
                  class="form-control"
                  value
                  required
                  autofocus
                  v-model="email"
                />
              </div>
              <div class="mb-3">
                <label for="password" class="col-md-5 py-2 col-form-label">Password</label>
                <input
                  id="password"
                  type="password"
                  class="form-control"
                  required
                  v-model="password"
                />
              </div>
              <br /> 
              <div class="row mb-4 text-center justify-content-md-center">
                <div class="col-auto">
                  <button type="submit" class="btn btn-outline-primary">Login</button>
                </div>

                <div class="col-auto">
                  <router-link to="/auth/register">
                      <button>Register</button>
                  </router-link>
              </div>


          
                
              </div>
              <hr/>
              <!-- <div class="row-md-4 text-center justify-content-md-center">
                <div class="col">
                  <a class="btn btn-outline-dark" role="button" style="text-transform:none" @click="signInWithGoogle">
                    <i class="bi bi-google"></i>
                    Login with Google
                  </a>
                </div>
              </div> -->
            </form>
          </div>
        </div>
      </div>    
    </div>
  </div>
</template>
<script>

  import { mapActions } from 'vuex';


  export default {
      name: "LoginComponent",
      methods: {
        ...mapActions(['signInWithGoogle']),
      },
  };
</script>
