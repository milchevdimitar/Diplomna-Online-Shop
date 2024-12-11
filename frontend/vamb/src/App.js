// src/App.js
import React, { useState, useEffect } from 'react';
import { Layout, Menu, Spin, message } from 'antd';
import { HomeOutlined, ShoppingCartOutlined } from '@ant-design/icons';
import LoginForm from './components/LoginForm';
import ProductList from './components/ProductList';
import SearchForm from './components/SearchForm';
import { searchProducts, getFormOptions } from './api'; // Предполага се, че имаш файл за API

const { Header, Content, Footer } = Layout;

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchData, setSearchData] = useState({});
  const [options, setOptions] = useState({ carManufacturers: [], productCategories: [], productManufacturers: [] });

  // Търсене на продукти
  const handleSearch = async (values) => {
    setLoading(true);
    setSearchData(values);

    try {
      const result = await searchProducts(values);
      setProducts(result);
    } catch (error) {
      message.error('Грешка при търсене на продукти.');
    } finally {
      setLoading(false);
    }
  };

  // Логин обработка
  const handleLogin = (email, password) => {
    // Логика за логин
    setIsLoggedIn(true);
  };

  // Извличане на опции за търсене
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const data = await getFormOptions();
        setOptions(data);
      } catch (error) {
        console.error('Грешка при зареждане на опции:', error);
      }
    };
    fetchOptions();
  }, []);

  // Възможни елементи на менюто
  const menuItems = [
    { label: 'Начало', key: '1', icon: <HomeOutlined /> },
    { label: 'Продукти', key: '2', icon: <ShoppingCartOutlined /> },
  ];

  return (
    <Layout>
      <Header>
        <Menu theme="dark" mode="horizontal" items={menuItems} />
      </Header>
      <Content style={{ padding: '20px' }}>
        {!isLoggedIn ? (
          <div>
            <h2>Влезте в профила си</h2>
            <LoginForm onLogin={handleLogin} />
          </div>
        ) : (
          <>
            <SearchForm options={options} onSearch={handleSearch} />
            {loading ? (
              <Spin size="large" />
            ) : (
              <ProductList products={products} />
            )}
          </>
        )}
      </Content>
      <Footer style={{ textAlign: 'center' }}>Онлайн магазин ©2024</Footer>
    </Layout>
  );
};

export default App;
