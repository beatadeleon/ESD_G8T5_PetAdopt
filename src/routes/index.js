import { createRouter, createWebHistory } from 'vue-router';
import { auth, database } from '../firebaseConfig';
import Login from '../auth/login.vue';
import RegisterComponent from '../auth/register.vue';
import Home from '../home.vue'
import AdminDashboardComponent from '../adminDashboard.vue';
import UserDashboardComponent from '../userDashboard.vue';
import ApplicationFormComponent from '../applicationForm.vue';
import showuserRequestsComponent from '../showuserRequests.vue';
import bookingComponent from '../booking.vue'
import { ref, get } from 'firebase/database';




const routes = [
    {
        path: '/auth/login',
        name: 'login',
        component: Login,
        meta: { requiresAuth: false },
    },
    {
        path: '/auth/register',
        name: 'Register',
        component: RegisterComponent,
        meta: { requiresAuth: false },
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: { requiresAuth: false },
    },

    {
        path: '/adminDashboard',
        name: 'AdminDashboard',
        component: AdminDashboardComponent, // Replace AdminDashboardComponent with the actual component for the admin dashboard
        meta: {
          requiresAuth: true, // You can set meta fields if authentication is required for the admin dashboard
          requiredRole: 'admin', // You can specify the required role for accessing the admin dashboard
        },
    },
    {
        path: '/userDashboard',
        name: 'UserDashboard',
        component: UserDashboardComponent, 
        meta: {
          requiresAuth: true, // You can set meta fields if authentication is required for the admin dashboard
          requiredRole: 'user', // You can specify the required role for accessing the admin dashboard
        },
    },
    {
      path: '/applicationForm',
      name: 'ApplicationForm',
      component: ApplicationFormComponent,
    },
    {
      path:'/showuserRequests',
      name: 'showuserRequests',
      component: showuserRequestsComponent,
    },
    {
      path:'/booking',
      name: 'booking',
      component: bookingComponent,
    }  
]


const router = createRouter({ 
    history: createWebHistory(),
    routes
})




router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiredRole = to.meta.requiredRole;
  
    const user = await new Promise(resolve => {
      auth.onAuthStateChanged(resolve);
    });
  
    if (requiresAuth && !user) {
      // If authentication is required but user is not logged in, redirect to login page
      next('/auth/login');
      return;
    }
  
    if (requiredRole && user) {
      const userRef = ref(database, `users/${user.uid}/role`);
      try {
        const snapshot = await get(userRef);
        const userRole = snapshot.val();
        if (userRole !== requiredRole) {
          // If user role doesn't match required role, redirect to homepage
          next('/');
          return;
        }
      } catch (error) {
        console.error("Error fetching user role:", error);
        next('/');
        return;
      }
    }
  
    // Proceed to the route
    next();
  });
  




export default router