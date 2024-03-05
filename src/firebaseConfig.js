// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from 'firebase/auth'
import {getDatabase} from 'firebase/database'
import {getAnalytics} from 'firebase/analytics'


//to initliase firebase to your vue JS application



// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAPL9GntkLJzbJ9TG4p78p0GZAt405JQnI",
  authDomain: "petadopt-e0fe8.firebaseapp.com",
  databaseURL: "https://petadopt-e0fe8-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "petadopt-e0fe8",
  storageBucket: "petadopt-e0fe8.appspot.com",
  messagingSenderId: "44424730789",
  appId: "1:44424730789:web:f199a002aee390e6dc154c",
  measurementId: "G-BLL612Z6RW"
};

  
// Initialize Firebase
const app = initializeApp(firebaseConfig);

const auth = getAuth(app)
const database = getDatabase(app)
const analytics = getAnalytics(app)


export { app, auth, database, analytics }