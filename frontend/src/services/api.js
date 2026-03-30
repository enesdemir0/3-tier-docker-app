import axios from 'axios';

// --- 🍯 THE SMART LOGIC ---
const getBaseUrl = () => {
  // 1. Priority: If we specifically set an environment variable, use it.
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }

  // 2. Smart Detection: Look at the URL in the browser's address bar.
  // If you are on 'localhost', hostname is 'localhost'.
  // If you are on AWS '54.12.34.56', hostname is '54.12.34.56'.
  const { hostname } = window.location;
  
  // We always want to talk to our Backend on Port 8000
  return `http://${hostname}:8000/api/v1`;
};

const API_URL = getBaseUrl();
// --------------------------

export const sendMessage = async (question) => {
    try {
        const response = await axios.post(`${API_URL}/chat`, {
            question: question
        });
        return response.data;
    } catch (error) {
        console.error("API Connection Error:", error);
        throw error;
    }
};