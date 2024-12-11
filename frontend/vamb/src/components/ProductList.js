// src/components/ProductList.js
import React from 'react';
import { List, Card } from 'antd';

const ProductList = ({ products }) => {
  return (
    <List
      grid={{ gutter: 16, column: 4 }}
      dataSource={products}
      renderItem={(product) => (
        <List.Item>
          <Card title={product.name} bordered={false}>
            <p>{product.description}</p>
            <p>Цена: {product.price} лв.</p>
          </Card>
        </List.Item>
      )}
    />
  );
};

export default ProductList;
