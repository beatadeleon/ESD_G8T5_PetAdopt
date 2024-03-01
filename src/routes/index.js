import { createRouter, createWebHistory } from 'vue-router';
import { auth, database } from '../firebaseConfig';
import Login from '../auth/login.vue';
import RegisterComponent from '../auth/register.vue';
import Home from '../home.vue'
import { ref, get } from 'firebase/database'




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
  
]


const router = createRouter({ 
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
    const requiredRole = to.meta.requiredRole;
    auth.onAuthStateChanged((user) => {
        if (requiresAuth && !user) {
            // If the route requires authentication and the user is not logged in, redirect to the login page
            next('/auth/login');
        } else {
            if (requiredRole && user) {
                const userRef = ref(database, `users/${user.uid}/role`);
                get(userRef).then((snapshot) => {
                    const userRole = snapshot.val();
                    if (userRole !== requiredRole) {
                        // Redirect only if the user has a role and it doesn't match the required role
                        next('/'); // Redirect to the homepage or another appropriate route
                    } else {
                        next(); // Proceed to the route
                    }
                }).catch((error) => {
                    console.error("Error fetching user role:", error);
                    next('/');
                });
            } else {
                next(); // Proceed to the route
            }
        }
    });
});



export default router