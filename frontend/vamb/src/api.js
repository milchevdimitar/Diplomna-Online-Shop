// src/api.js
const API_URL = 'http://localhost:5000/api';

export const getProducts = async () => {
  const response = await fetch(`${API_URL}/products`);
  const data = await response.json();
  return data;
};

export const searchProducts = async (filters) => {
  const response = await fetch(`${API_URL}/search-products`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(filters),
  });
  const data = await response.json();
  return data;
};

export const getFormOptions = async () => {
  const response = await fetch(`${API_URL}/form-options`);
  const data = await response.json();
  return data;
};
