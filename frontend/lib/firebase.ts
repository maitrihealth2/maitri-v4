import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCWPPqQjCQN5EmvwfdzNHggCU6NWz3wgfk",
  authDomain: "mindbridge-e0c62.firebaseapp.com",
  projectId: "mindbridge-e0c62",
  storageBucket: "mindbridge-e0c62.firebasestorage.app",
  messagingSenderId: "695579262057",
  appId: "1:695579262057:web:7a6e6b359a15c98fa936f8",
  measurementId: "G-DBD64NEBF5"
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { app, auth, googleProvider };
