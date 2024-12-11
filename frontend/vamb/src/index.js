import React from 'react';
import ReactDOM from 'react-dom/client'; // Забележете новия импорт
import './index.css';
import App from './App';

const rootElement = document.getElementById('root');

// Създаване на root с новия метод
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
