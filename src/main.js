
import { createApp } from 'vue'
import App from './App.vue'

import router from './routes/index'
import { auth } from './firebaseConfig'
import  store  from './store'

const app = createApp(App);

app.use(router);
app.use(store);


// Use the authentication
app.use(auth);

// Mount the app to the HTML element with id 'app'
app.mount('#app');


