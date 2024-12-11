// src/components/SearchForm.js
import React from 'react';
import { Form, Input, Select, Button } from 'antd';

const SearchForm = ({ options, onSearch }) => {
  const [form] = Form.useForm();

  return (
    <Form form={form} onFinish={onSearch} layout="vertical">
      <Form.Item name="manufacturer" label="Производител на автомобил">
        <Select options={options.carManufacturers} />
      </Form.Item>
      <Form.Item name="model" label="Модел на автомобил">
        <Select options={options.carManufacturers} />
      </Form.Item>
      <Form.Item name="category" label="Категория на продукта">
        <Select options={options.productCategories} />
      </Form.Item>
      <Form.Item name="serial_num" label="Сериен номер">
        <Input />
      </Form.Item>
      <Form.Item name="product_manufacturer" label="Производител на продукт">
        <Select options={options.productManufacturers} />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Търси
        </Button>
      </Form.Item>
    </Form>
  );
};

export default SearchForm;
