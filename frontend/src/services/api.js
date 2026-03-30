import axios from 'axios';

// This is the URL of your FastAPI backend!
const API_URL = "http://localhost:8000/api/v1";

export const sendMessage = async (question) => {
    try {
        const response = await axios.post(`${API_URL}/chat`, {
            question: question
        });
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};