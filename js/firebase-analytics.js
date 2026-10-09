import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-app.js";
import { getAnalytics, isSupported } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-analytics.js";

const firebaseConfig = {
  apiKey: "AIzaSyBhdQVl_G8dBCuBEhA7eARbxPNVdH_Uww8",
  authDomain: "hipobuy-website.firebaseapp.com",
  projectId: "hipobuy-website",
  storageBucket: "hipobuy-website.firebasestorage.app",
  messagingSenderId: "59289522752",
  appId: "1:59289522752:web:f88feb94532e6632edc5a5",
  measurementId: "G-XP1GYVEZSP",
};

const app = initializeApp(firebaseConfig);

isSupported()
  .then((ok) => {
    if (!ok) return;
    getAnalytics(app);
  })
  .catch(() => {});
