
CREATE TABLE sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    product_name VARCHAR(100),
    product_category VARCHAR(50),
    sales DECIMAL(10, 2),
    customer_segment VARCHAR(50),
    sales_channel VARCHAR(50)
);
