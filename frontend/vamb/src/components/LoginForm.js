// src/components/LoginForm.js
import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';

const LoginForm = ({ onLogin }) => {
  const [loading, setLoading] = useState(false);

  const handleLoginSubmit = async (values) => {
    setLoading(true);
    try {
      // Логин API обаждане тук (примерно чрез onLogin)
      await onLogin(values.email, values.password);
    } catch (error) {
      message.error('Грешка при логване.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form onFinish={handleLoginSubmit} layout="vertical">
      <Form.Item name="email" label="Имейл" rules={[{ required: true, message: 'Моля, въведете имейл!' }]}>
        <Input />
      </Form.Item>
      <Form.Item name="password" label="Парола" rules={[{ required: true, message: 'Моля, въведете парола!' }]}>
        <Input.Password />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Влез
        </Button>
      </Form.Item>
    </Form>
  );
};

export default LoginForm;
