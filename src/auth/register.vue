<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref(null)
const pnum = ref('')
const address = ref('')
const Pcode = ref('')
const calendlyUuid = ref(null)

const store = useStore()
const router = useRouter()

const Register = async () => {
  try {
    if (validatePassword(password.value)) {
      await store.dispatch('registerUser', {
        email: email.value,
        password: password.value,
        name: name.value,
        address: address.value,
        pcode: Pcode.value,
        pnum: pnum.value,
        role: 'user',
        calendlyUuid: 'null'
      })
      router.push('/')
    } else {
      error.value = 'Password must contain at least one non-letter and non-number character.'
    }
  } catch (err) {
    error.value = err.message
  }
}

const validatePassword = (password) => {
  // Regular expression to check for at least one non-letter and non-number character
  const regex = /[^a-zA-Z0-9]/;
  return regex.test(password);
}
</script>
<template>
  <div class="container">
    <div class="row justify-content-center mt-4">
      <div class="col-md-10">
        <div class="card">
          <div class="row g-0">
            <!-- <div class="col-md-5">
              <img class="img-fluid" src="../../assets/images/registerPhoto.jpg" alt="login photo" style="height: 100%"/>
            </div> -->
            <div class="col justify-content-center">
              <div class="card-body">
                <div v-if="error" class="alert alert-danger">{{ error }}</div>
                <h4 class="card-header text-center">Register your account</h4>
                <br/>
                <form action="#" @submit.prevent="Register">
                  <div class="form-group mb-3">
                    <label for="name" class="col-md-4 col-form-label">Name<span style="color:red;">*</span>:</label>
                    <input
                      id="name"
                      type="name"
                      class="form-control"
                      name="name"
                      value
                      required
                      autofocus
                      v-model="name"
                    />
                  </div>
                  <br/>
                  <input
                        type="hidden"
                        v-model="calendlyUuid"
                      />
                  <div class="form-group mb-3">
                    <label for="email" class="col-md-6 col-form-label ">Email<span style="color:red;">*</span>:</label>
                      <input
                        id="email"
                        type="email"
                        class="form-control"
                        name="email"
                        value
                        required
                        autofocus
                        v-model="email"
                      />
                  </div>
                  <br/>
                  <div class="form-group row">
                    <div class="col-md-6">
                      <label for="pnum" class="col-md-6 col-form-label ">Phone Number<span style="color:red;">*</span>:</label>
                      <input
                        id="pnum"
                        type="number"
                        pattern="\d*"
                        class="form-control"
                        maxlength="8"
                        name="pnum"
                        oninput="this.value = this.value.slice(0, 8)"
                        value
                        required
                        v-model="pnum"
                      />
                    </div>
                    <div class="col-md-6">
                      <label for="password" class="col-md-6 col-form-label">Password<span style="color:red;">*</span>:</label>
                      <input
                        id="password"
                        type="password"
                        class="form-control"
                        name="password"
                        required
                        v-model="password"
                        @input="validatePassword"
                      />
                    </div>
                  </div>
                  <br/>
                  <div class="form-group row">
                    <div class="col-md-6">
                      <label for="address" class="col-md-6 col-form-label">Address<span style="color:red;">*</span>:</label>
                      <input
                        id="address"
                        type="address"
                        class="form-control"
                        name="address"
                        required
                        v-model="address"
                      />
                    </div>
                    <div class="col-md-6">
                      <label for="Pcode" class="col-md-6 col-form-label">Postal Code<span style="color:red;">*</span>:</label>
                      <input
                        id="Pcode"
                        type="number"
                        class="form-control"
                        pattern="\d*"
                        name="Pcode"
                        maxlength="6"
                        oninput="this.value = this.value.slice(0, 6)"
                        required
                        v-model="Pcode"
                      />
                    </div>
                  </div>
                  <br/><br/>
                  <div class="row mb-4 text-center justify-content-md-center">
                    <div class="col-5">
                      <button type="submit" class="btn btn-outline-primary">Submit</button>
                    </div>

                    <div class="col-4">
                      <router-link to="/auth/login">
                        <button role="link" class="btn btn-outline-dark">Cancel</button>
                      </router-link>
                    </div>

                


                    
                  </div>
                </form>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'RegisterComponent',
}
</script>
