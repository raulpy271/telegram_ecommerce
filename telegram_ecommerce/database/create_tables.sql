

CREATE TABLE IF NOT EXISTS customers (
    user_id INT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password_hash VARCHAR(64),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);


CREATE TABLE IF NOT EXISTS photo (
    photo_id VARCHAR(150) PRIMARY KEY,
    image BLOB DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(30) NOT NULL,
    category_description VARCHAR(500) NOT NULL,
    tags VARCHAR(100),
    image_id VARCHAR(150),
    FOREIGN KEY (image_id)
    REFERENCES photo (photo_id)
);


CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(30) NOT NULL,
    product_description VARCHAR(500) NOT NULL,
    unit_price FLOAT NOT NULL,
    quantity_in_stock INT NOT NULL,
    quantity_purchased INT NOT NULL,
    category_id INT NOT NULL,
    image_id VARCHAR(150),
    FOREIGN KEY (image_id)
    REFERENCES photo (photo_id),
    FOREIGN KEY (category_id)
    REFERENCES category (category_id)
);


CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    price FLOAT NOT NULL,
    quantity INT NOT NULL,
    rating INT NOT NULL,
    total_price FLOAT GENERATED ALWAYS AS (quantity * price),
    user_id INT,
    product_id INT,
    FOREIGN KEY (user_id)
    REFERENCES customers (user_id),
    FOREIGN KEY (product_id)
    REFERENCES products (product_id)
);


