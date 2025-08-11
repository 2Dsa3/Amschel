import axios from 'axios';

//create an instance of axios with the base URL
const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export const scrapeInstagram = async (username) => {
  try {
    const response = await api.post('/social-media', { username });
    // return response.data; // { followers, followees }
  } catch (error) {
    // Throw a cleaned-up error message for the caller
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    } else {
      throw new Error(error.message || 'Unknown error occurred');
    }
  }
};

export default api;
