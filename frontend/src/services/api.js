import axios from 'axios';

//create an instance of axios with the base URL
const api = axios.create({
  baseURL: 'http://localhost:8000'
});

export const scrapeInstagram = async (username) => {
  try {
    const response = await api.post('/social-media', { username });
  return response.data; // { followers, followees }
  } catch (error) {
    // Throw a cleaned-up error message for the caller
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    } else {
      throw new Error(error.message || 'Unknown error occurred');
    }
  }
};


export const uploadPDFs = async (file1, file2) => {
  try {
    const formData = new FormData();
  if (file1) formData.append('balance_sheet', file1);
  if (file2) formData.append('general_info', file2);
    console.log('Uploading PDFs:', { file1, file2 });
    const response = await api.post('/pdf-media', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    } else {
      throw new Error(error.message || 'Unknown error occurred');
    }
  }
};


export default api;
