import { createStore } from 'vuex';
import { auth } from './firebaseConfig';
import { getDatabase, ref, set} from 'firebase/database';

import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  updateProfile,

} from 'firebase/auth'

//creates a store with action for authentication. 

const store = createStore({
  state: {
    user: {
      loggedIn: false,
      data: null,
    }
  },

  getters: {
    user(state) {
      return state.user
    }
  },
  mutations: {
    SET_USER(state, payload) {
      state.user.data = payload
    },
    SET_LOGGED_IN(state, value) {
      state.user.loggedIn = value
    },
  },
  actions: {
    async registerUser(context, { email, password, name, address, pcode, role, pnum }) {
      try {
        // Create the user in Firebase Authentication
        const response = await createUserWithEmailAndPassword(auth, email, password);
        if (response) {
          const user = response.user;
          await updateProfile(user, { displayName: name });
          const db = getDatabase();
          await set(ref(db, 'users/' + user.uid), {
            displayName: name,
            email: email,
            address: address,
            pcode: pcode,
            role: role,
            phoneNumber: pnum,
            // Add any other user information you want to store
          });
          context.commit('SET_USER', user);
        } else {
          throw new Error('Unable to register user');
        }
      } catch (error) {
        console.error('Registration error:', error);
        throw error;
      }
    },

    async loginUser(context, { email, password }) {
      const response = await signInWithEmailAndPassword(auth, email, password)
      if (response) {
        context.commit('SET_USER', response.user);
      } else {
        throw new Error('login failed')
      }
    },

    async logoutUser(context) {
      await signOut(auth);
      context.commit('SET_USER', null);
      window.location.reload();
    },

    async fetchUser(context, user) {
      context.commit('SET_LOGGED_IN', user !== null)
      if (user) {
        context.commit('SET_USER', {
          userId: user.userId,
          displayName: user.displayName,
          email: user.email,
          role: user.role,
        })
      } else {
        context.commit('SET_USER', null)
      }
    },

    
  }
})

// export the store
export default store