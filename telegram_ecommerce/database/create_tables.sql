

CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password_hash VARCHAR(64),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
) engine=InnoDB;


CREATE TABLE IF NOT EXISTS photo (
    id VARCHAR(150) PRIMARY KEY,
    image_blob BLOB DEFAULT NULL
) engine=InnoDB;


CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(500) NOT NULL,
    tags VARCHAR(100),
    image_id VARCHAR(150),
    FOREIGN KEY (image_id)
    REFERENCES photo (id)
) engine=InnoDB;


CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(30) NOT NULL,
    description VARCHAR(500) NOT NULL,
    price FLOAT NOT NULL,
    quantity_in_stock INT NOT NULL,
    quantity_purchased INT NOT NULL,
    category_id INT NOT NULL,
    image_id VARCHAR(150),
    FOREIGN KEY (image_id)
    REFERENCES photo (id),
    FOREIGN KEY (category_id)
    REFERENCES category (id),
    FULLTEXT(name, description)
) engine=InnoDB;


CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(150) PRIMARY KEY,
    price FLOAT NOT NULL,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT,
    FOREIGN KEY (user_id)
    REFERENCES customers (id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (product_id)
    REFERENCES products (id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) engine=InnoDB;


