DROP DATABASE IF EXISTS CROPDETECTION;
CREATE DATABASE CROPDETECTION;
USE CROPDETECTION;

-- Tables 
-- user tables
CREATE TABLE user (
	id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone NUMERIC(10, 0) UNIQUE NOT NULL, 
    password VARCHAR(100) NOT NULL
);

CREATE TABLE user_address (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    line_one VARCHAR(50) NOT NULL,
    line_two VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    landmark VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(20) NOT NULL,
    zip_code NUMERIC(6, 0) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE user_verification (
    id VARCHAR(50) PRIMARY KEY,
    phone NUMERIC(10, 0) UNIQUE NOT NULL,
    phoneVerified BOOLEAN DEFAULT FALSE,
    phoneOTP NUMERIC(6, 0),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_search_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    search_query VARCHAR(255) NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- seller tables
CREATE TABLE seller (
	id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    business_name VARCHAR(100) NOT NULL,
    phone NUMERIC(10, 0) UNIQUE NOT NULL, 
    email VARCHAR(100) NOT NULL UNIQUE,
    gst VARCHAR(15) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE seller_verification (
    id VARCHAR(50) PRIMARY KEY,
    phone NUMERIC(10, 0) UNIQUE,
    phoneVerified BOOLEAN DEFAULT FALSE,
    phoneOTP NUMERIC(6, 0),
    email VARCHAR(50) UNIQUE,
    emailVerified BOOLEAN DEFAULT FALSE,
    emailOTP NUMERIC(6, 0),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- consultant tables
CREATE TABLE consultant (
    id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone NUMERIC(10, 0) UNIQUE, 
    email VARCHAR(50) NOT NULL UNIQUE,
    expertise VARCHAR(50) NOT NULL,
    experience NUMERIC(2, 0) NOT NULL,
    starting_charges NUMERIC(6, 2) NOT NULL,
    profile VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE consultant_verification (
    id VARCHAR(50) PRIMARY KEY,
    phone NUMERIC(10, 0) UNIQUE,
    phoneVerified BOOLEAN DEFAULT FALSE,
    phoneOTP NUMERIC(6, 0),
    email VARCHAR(50) UNIQUE,
    emailVerified BOOLEAN DEFAULT FALSE,
    emailOTP NUMERIC(6, 0),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE appointment (
	id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    consultant_id VARCHAR(50) NOT NULL,
    mode VARCHAR(7) CHECK(mode IN ('online', 'offline')),
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(10) CHECK(status IN ('pending', 'confirmed', 'cancelled')) DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (consultant_id) REFERENCES consultant(id) ON DELETE CASCADE
);
select * from product;
-- product tables 
CREATE TABLE product (
    id VARCHAR(50) PRIMARY KEY,
    seller_id VARCHAR(50),
    name VARCHAR(50) NOT NULL,
    brand_name VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(500) NOT NULL,
    category VARCHAR(20) NOT NULL,
    cost_price NUMERIC(6, 2) NOT NULL,
    selling_price NUMERIC(6, 2) NOT NULL,
    image VARCHAR(100) NOT NULL,
    about_company_line1 VARCHAR(500) NOT NULL,
    about_company_line2 VARCHAR(500),
    about_company_line3 VARCHAR(500),
    about_product_line1 VARCHAR(500) NOT NULL,
    about_product_line2 VARCHAR(500),
    about_product_line3 VARCHAR(500),
    about_product_line4 VARCHAR(500),
    quantity NUMERIC(5, 0),
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES seller(id) ON DELETE CASCADE
);
Select * from product;            
CREATE TABLE product_image (
    id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    image VARCHAR(100) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

-- cart tables 
CREATE TABLE cart (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE cart_item (
    id VARCHAR(50) PRIMARY KEY,
    cart_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity NUMERIC(3, 0) NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES cart(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE TABLE pending_cart_deletion (
    cart_id VARCHAR(50) PRIMARY KEY
);

-- order tables
CREATE TABLE order_history (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    user_address VARCHAR(100) NOT NULL,
    total_amount NUMERIC(6, 2) NOT NULL,
    transaction_id VARCHAR(50) NOT NULL,
    payment_id VARCHAR(50) NOT NULL,
    payment_method VARCHAR(10) NOT NULL CHECK(payment_method IN ('online', 'offline')),
    payment_status VARCHAR(10) NOT NULL CHECK(payment_status IN ('pending', 'success', 'failed')),
    order_status VARCHAR(10) NOT NULL CHECK(order_status IN ('confirmed', 'shipped', 'delivered', 'cancelled')) DEFAULT 'confirmed',
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    shipping_date DATETIME,
    delivery_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    id VARCHAR(50) PRIMARY KEY,
    order_history_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity NUMERIC(3, 0) NOT NULL,
    rate NUMERIC(6, 2) NOT NULL,
    total_price NUMERIC(6, 2) NOT NULL,
    FOREIGN KEY (order_history_id) REFERENCES order_history(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);


-- views
CREATE VIEW cart_summary AS
SELECT 
    u.id AS user_id,
    c.id AS cart_id,
    p.id AS product_id,
    p.name,
    p.title,
    p.selling_price AS rate,
    ci.quantity,
    (ci.quantity * p.selling_price) AS total_price,
    GROUP_CONCAT(pi.image) AS product_images -- Combines multiple images into a single string
FROM cart_item ci
JOIN cart c ON ci.cart_id = c.id
JOIN user u ON c.user_id = u.id
JOIN product p ON ci.product_id = p.id
LEFT JOIN product_image pi ON p.id = pi.product_id
GROUP BY ci.id, u.id, c.id, p.id, p.name, p.title, p.selling_price, ci.quantity;

CREATE VIEW user_order_summary AS
SELECT
    CONCAT(u.first_name, ' ', u.last_name) AS name,
    u.id AS user_id,
    oh.id AS order_history_id,
    oh.user_address,
    oh.total_amount,
    oh.transaction_id,
    oh.payment_id,
    oh.payment_method,
    oh.payment_status,
    oh.order_status,
    oh.order_date,
    oh.shipping_date,
    oh.delivery_date,
    p.seller_id,
    JSON_ARRAYAGG(
        JSON_OBJECT(
            'product_id', o.product_id,
            'product_name', p.name,
            'product_image', p.image,
            'quantity', o.quantity,
            'rate', o.rate,
            'total_price', o.total_price
        )
    ) AS orders
FROM
    `user` u
JOIN
    order_history oh ON u.id = oh.user_id
JOIN
    orders o ON oh.id = o.order_history_id
JOIN
    product p ON o.product_id = p.id
GROUP BY
    u.id, oh.id, p.seller_id;

-- events
DELIMITER $$

CREATE EVENT delete_empty_carts
ON SCHEDULE EVERY 1 MINUTE
DO
BEGIN
    DELETE FROM cart WHERE id IN (SELECT cart_id FROM pending_cart_deletion);
    DELETE FROM pending_cart_deletion;
END $$

DELIMITER ;


-- triggers 
DELIMITER $$

CREATE TRIGGER after_cart_item_delete
AFTER DELETE ON cart_item
FOR EACH ROW
BEGIN
    DECLARE item_count INT;

    -- Count remaining items in the cart
    SELECT COUNT(*) INTO item_count FROM cart_item WHERE cart_id = OLD.cart_id;

    -- If no items remain, add the cart_id to pending deletion table
    IF item_count <= 0 THEN
        INSERT IGNORE INTO pending_cart_deletion (cart_id) VALUES (OLD.cart_id);
    END IF;
END $$

DELIMITER ;


-- procedures 
DELIMITER $$

CREATE PROCEDURE ManageUserSearchHistory(
    IN p_user_id VARCHAR(50), 
    IN p_search_query VARCHAR(255)
)
BEGIN
    -- Insert new search history record
    INSERT INTO user_search_history (user_id, search_query) 
    VALUES (p_user_id, p_search_query);

    -- Delete the oldest record if more than 10 exist for this user
    DELETE FROM user_search_history 
    WHERE id IN (
        SELECT id FROM (
            SELECT id FROM user_search_history 
            WHERE user_id = p_user_id 
            ORDER BY searched_at ASC 
            LIMIT 1 OFFSET 20
        ) AS subquery
    );
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE UpsertUserVerification(
    IN p_id VARCHAR(50),
    IN p_phone VARCHAR(20),
    IN p_phoneOTP VARCHAR(10)
)
BEGIN
    DECLARE record_count INT;

    -- Check if the phone number already exists
    SELECT COUNT(*) INTO record_count FROM user_verification WHERE phone = p_phone;

    IF record_count = 0 THEN
        -- Insert if the phone number does not exist
        INSERT INTO user_verification (id, phone, phoneOTP) VALUES (p_id, p_phone, p_phoneOTP);
    ELSE
        -- Update if the phone number exists
        UPDATE user_verification SET phoneOTP = p_phoneOTP WHERE phone = p_phone;
    END IF;
END $$

DELIMITER ;

-- Procedure to remove entry from user verification table and insert it into user table
DELIMITER $$
CREATE PROCEDURE InsertUser(
    IN p_id VARCHAR(50),
    IN p_first_name VARCHAR(20),
    IN p_last_name VARCHAR(20),
    IN p_phone NUMERIC(12, 0),
    IN p_password VARCHAR(100),
    IN task VARCHAR(10)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    IF task = 'insert' THEN
        -- Insert into user table
        INSERT INTO user (id, first_name, last_name, phone, password)
        VALUES (p_id, p_first_name, p_last_name, p_phone, p_password);

    ELSEIF task = 'update' THEN
        -- Update user phone number
        UPDATE user
        SET phone = p_phone
        WHERE id = p_id;

    END IF;
    
    -- Delete from seller_verification table
    -- DELETE FROM user_verification WHERE id = p_id;
    DELETE FROM user_verification WHERE phone = p_phone;
    
    COMMIT;
END $$
DELIMITER ;

DELIMITER $$

CREATE PROCEDURE UpsertSellerVerificationByEmail(
    IN p_id VARCHAR(50),
    IN p_email VARCHAR(30),
    IN p_emailOTP NUMERIC(6, 0)
)
BEGIN
    DECLARE email_count INT;

    -- Check if the email already exists in seller_verification
    SELECT COUNT(*) INTO email_count FROM seller_verification WHERE email = p_email;

    IF email_count = 0 THEN
        -- Insert if the email does not exist
        INSERT INTO seller_verification (id, email, emailOTP, createdAt)
        VALUES (p_id, p_email, p_emailOTP, CURRENT_TIMESTAMP);
    ELSE
        -- Update if the email exists
        UPDATE seller_verification 
        SET emailOTP = p_emailOTP, createdAt = CURRENT_TIMESTAMP
        WHERE email = p_email;
    END IF;
END $$

DELIMITER $$

CREATE PROCEDURE UpsertSellerVerificationByPhone(
    IN p_id VARCHAR(50),
    IN p_phone NUMERIC(12, 0),
    IN p_phoneOTP NUMERIC(6, 0)
)
BEGIN
    DECLARE phone_count INT;

    -- Check if the phone number already exists in seller_verification
    SELECT COUNT(*) INTO phone_count FROM seller_verification WHERE id = p_id;

    IF phone_count = 0 THEN
        -- Insert if the phone number does not exist
        INSERT INTO seller_verification (id, phone, phoneOTP, createdAt)
        VALUES (p_id, p_phone, p_phoneOTP, CURRENT_TIMESTAMP);
    ELSE
        -- Update if the phone number exists
        UPDATE seller_verification 
        SET phone = p_phone, phoneOTP = p_phoneOTP, createdAt = CURRENT_TIMESTAMP
        WHERE id = p_id;
    END IF;
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE UpsertConsultantVerificationByEmail(
    IN p_id VARCHAR(50),
    IN p_email VARCHAR(30),
    IN p_emailOTP NUMERIC(6, 0)
)
BEGIN
    DECLARE email_count INT;

    -- Check if the email already exists in seller_verification
    SELECT COUNT(*) INTO email_count FROM consultant_verification WHERE email = p_email;

    IF email_count = 0 THEN
        -- Insert if the email does not exist
        INSERT INTO consultant_verification (id, email, emailOTP, createdAt)
        VALUES (p_id, p_email, p_emailOTP, CURRENT_TIMESTAMP);
    ELSE
        -- Update if the email exists
        UPDATE consultant_verification 
        SET emailOTP = p_emailOTP, createdAt = CURRENT_TIMESTAMP
        WHERE email = p_email;
    END IF;
END $$

DELIMITER $$

CREATE PROCEDURE UpsertConsultantVerificationByPhone(
    IN p_id VARCHAR(50),
    IN p_phone NUMERIC(12, 0),
    IN p_phoneOTP NUMERIC(6, 0)
)
BEGIN
    DECLARE phone_count INT;

    -- Check if the phone number already exists in seller_verification
    SELECT COUNT(*) INTO phone_count FROM consultant_verification WHERE id = p_id;

    IF phone_count = 0 THEN
        -- Insert if the phone number does not exist
        INSERT INTO consultant_verification (id, phone, phoneOTP, createdAt)
        VALUES (p_id, p_phone, p_phoneOTP, CURRENT_TIMESTAMP);
    ELSE
        -- Update if the phone number exists
        UPDATE consultant_verification 
        SET phone = p_phone, phoneOTP = p_phoneOTP, createdAt = CURRENT_TIMESTAMP
        WHERE id = p_id;
    END IF;
END $$

DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertSeller(
    IN p_id VARCHAR(50),
    IN p_first_name VARCHAR(20),
    IN p_last_name VARCHAR(20),
    IN p_business_name VARCHAR(50),
    IN p_phone NUMERIC(12, 0),
    IN p_email VARCHAR(30),
    IN p_gst VARCHAR(20),
    IN p_password VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Insert into seller table
    INSERT INTO seller (id, first_name, last_name, business_name, phone, email, gst, password)
    VALUES (p_id, p_first_name, p_last_name, p_business_name, p_phone, p_email, p_gst, p_password);
    
    -- Delete from seller_verification table
    DELETE FROM seller_verification WHERE id = p_id;
    
    COMMIT;
END $$
DELIMITER ;

DELIMITER $$

CREATE PROCEDURE InsertConsultant(
    IN p_id VARCHAR(50),
    IN p_first_name VARCHAR(20),
    IN p_last_name VARCHAR(20),
    IN p_expertise VARCHAR(50),
    IN p_experience NUMERIC(2, 0),
    IN p_starting_charges NUMERIC(6, 2),
    IN p_phone NUMERIC(12, 0),
    IN p_email VARCHAR(30),
    IN p_password VARCHAR(100),
    IN p_profile VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction in case of an exception
        ROLLBACK;
    END;

    -- Start the transaction
    START TRANSACTION;

    -- Insert the consultant into the consultant table
    INSERT INTO consultant (id, first_name, last_name, expertise, experience, starting_charges, phone, email, profile, password)
    VALUES (p_id, p_first_name, p_last_name, p_expertise, p_experience, p_starting_charges, p_phone, p_email, p_profile, p_password);

    -- Delete the corresponding row from the consultant_verification table
    DELETE FROM consultant_verification WHERE email = p_email;

    -- Commit the transaction if everything is fine
    COMMIT;
END $$

DELIMITER ;



-- Procedure to insert records in orders and history table and to remove cart items

DELIMITER $$

CREATE PROCEDURE PlaceOrder(
    IN b_order_id VARCHAR(50),
    IN b_history_id VARCHAR(50),
    IN b_user_id VARCHAR(50),
    IN b_user_address VARCHAR(50),
    IN b_total_amount NUMERIC(6, 2),
    IN b_transaction_id VARCHAR(50),
    IN b_payment_id VARCHAR(50),
    IN b_payment_method VARCHAR(20),
    IN b_payment_status VARCHAR(20)
)
BEGIN
    -- Declare exception handler for rollback in case of errors
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    -- Start the transaction
    START TRANSACTION;

    -- Insert into order_history table
    INSERT INTO order_history (id, user_id, user_address, total_amount, transaction_id, payment_id, payment_method, payment_status)
    VALUES (b_history_id, b_user_id, b_user_address, b_total_amount, b_transaction_id, b_payment_id, b_payment_method, b_payment_status);

    -- Insert into orders table using data from cart_summary
    INSERT INTO orders (id, order_history_id, product_id, quantity, rate, total_price)
	SELECT 
		b_order_id, 
		b_history_id, 
		cs.product_id, 
        cs.quantity, 
        cs.rate, 
        (cs.quantity * cs.rate) AS total_price
    FROM cart_summary AS cs
    WHERE cs.user_id = b_user_id;

    -- Delete items from the cart only after the order is placed
    DELETE FROM cart_item 
    WHERE cart_id = (SELECT id FROM cart WHERE user_id = b_user_id);

    -- Commit the transaction if all steps are successful
    COMMIT;
END $$

DELIMITER ;

-- CREATE TABLE diseases (
--     id UUID PRIMARY KEY,
--     name VARCHAR(100) UNIQUE NOT NULL,
--     cure TEXT,
--     precaution TEXT,
--     causes TEXT
-- );

-- Create Disease-Product junction table
CREATE TABLE diseases (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    cure TEXT,
    precaution TEXT,
    causes TEXT
);
CREATE TABLE disease_products (
    id CHAR(36) PRIMARY KEY,
    disease_id CHAR(36),
    product_id CHAR(36),
    FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES productmodule_product(id) ON DELETE CASCADE
);
CREATE TABLE disease_consultants (
    id CHAR(36) PRIMARY KEY,
    disease_id CHAR(36),
    consultant_id CHAR(36),
    FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE,
    FOREIGN KEY (consultant_id) REFERENCES consultant_consultantuser(id) ON DELETE CASCADE
);

-- 1. Potato Early Blight
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '11111111-1111-1111-1111-111111111111',
    'Potato Early Blight',
    'Fungicides like Mancozeb',
    'Avoid overhead irrigation',
    'Alternaria solani fungus'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0001-0001-0001-000000000001',
    '11111111-1111-1111-1111-111111111111',
    '03c079bb69c84a6883df79f1a892a56a'
);

INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0001-0001-0001-000000000001',
    '11111111-1111-1111-1111-111111111111',
    'd1e50c9ad47e470f88e0ac2a5887d9c4'
);

-- 2. Potato Healthy
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '22222222-2222-2222-2222-222222222222',
    'Potato Healthy',
    'No treatment needed',
    'Regular monitoring',
    'No disease present'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0002-0002-0002-000000000002',
    '22222222-2222-2222-2222-222222222222',
    '077e47c82051400fa0dc8f8b16c0d985'
);

INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0002-0002-0002-000000000002',
    '22222222-2222-2222-2222-222222222222',
    'a1d9a0e1577748b4af9266a0f5c5a775'
);

-- 3. Potato Late Blight
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '33333333-3333-3333-3333-333333333333',
    'Potato Late Blight',
    'Copper-based fungicides',
    'Avoid overcrowding',
    'Phytophthora infestans'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0003-0003-0003-000000000003',
    '33333333-3333-3333-3333-333333333333',
    '988d7e326a194fab88599348957c2600'
);

INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0003-0003-0003-000000000003',
    '33333333-3333-3333-3333-333333333333',
    '642f735e1a684756b4a356e5ea65f7d6'
);

-- 4. Tomato Bacterial Spot
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '44444444-4444-4444-4444-444444444444',
    'Tomato Bacterial Spot',
    'Copper sprays',
    'Use disease-free seeds',
    'Xanthomonas spp.'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0004-0004-0004-000000000004',
    '44444444-4444-4444-4444-444444444444',
    '687ef43d54154591b8db20f164c24b41'
);
INSERT INTO disease_products (id, product_id, disease_id) VALUES
('01f062d2-2a84-46aa-b87c-d24b7a66a084', '23a7fd81-8aa1-4a5d-b8b0-bbf169bee43e', '11111111-1111-1111-1111-111111111111'),
('7d0c27f1-4461-48c3-96b5-9bb636f7156f', '3e4fca81-e496-422b-85f9-8a03efa41ec7', '22222222-2222-2222-2222-222222222222'),
('2b93f25e-7333-4071-9e3b-647fa1df12a0', '4604d1e0-50d9-408e-b1db-5e6b4cf3b7b3', '33333333-3333-3333-3333-333333333333'),
('c1dfeab5-eaa6-48e4-b505-e81c7dcfbe92', '6c628153-1bbc-41ec-80cd-a1f456c8ac48', '44444444-4444-4444-4444-444444444444'),
('aa85ed1a-f364-4701-80c5-c2f857de5a8f', '86e7e4de-ba8b-4f8a-89e1-0d608c9b0e5f', '55555555-5555-5555-5555-555555555555'),
('edf58755-b5ce-4fcb-a490-38fc82f2de1b', 'a4a730d4-af02-4845-a4ef-93a3ed630168', '66666666-6666-6666-6666-666666666666'),
('77b055aa-9674-4a52-b3e3-2087ac0ea9c5', 'a986727e-1c34-4495-aa4d-cca9d4b211f3', '77777777-7777-7777-7777-777777777777'),
('fdf672c1-3f29-49cd-9b70-e22c6c682962', 'aad925cf-809a-4ab8-816f-2ef0783bae1c', '88888888-8888-8888-8888-888888888888');



INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0004-0004-0004-000000000004',
    '44444444-4444-4444-4444-444444444444',
    'd1e50c9ad47e470f88e0ac2a5887d9c4'
);

-- 5. Tomato Early Blight
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '55555555-5555-5555-5555-555555555555',
    'Tomato Early Blight',
    'Apply fungicides like chlorothalonil',
    'Crop rotation and sanitation',
    'Alternaria solani'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0005-0005-0005-000000000005',
    '55555555-5555-5555-5555-555555555555',
    '03c079bb69c84a6883df79f1a892a56a'
);

INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0005-0005-0005-000000000005',
    '55555555-5555-5555-5555-555555555555',
    'a1d9a0e1577748b4af9266a0f5c5a775'
);

-- 6. Tomato Healthy
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '66666666-6666-6666-6666-666666666666',
    'Tomato Healthy',
    'No treatment needed',
    'Healthy cultural practices',
    'No disease present'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0006-0006-0006-000000000006',
    '66666666-6666-6666-6666-666666666666',
    '077e47c82051400fa0dc8f8b16c0d985'
);

INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0006-0006-0006-000000000006',
    '66666666-6666-6666-6666-666666666666',
    '642f735e1a684756b4a356e5ea65f7d6'
);

-- 7. Tomato Late Blight
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '77777777-7777-7777-7777-777777777777',
    'Tomato Late Blight',
    'Fungicides like metalaxyl',
    'Remove infected leaves',
    'Phytophthora infestans'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0007-0007-0007-000000000007',
    '77777777-7777-7777-7777-777777777777',
    '988d7e326a194fab88599348957c2600'
);

INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0007-0007-0007-000000000007',
    '77777777-7777-7777-7777-777777777777',
    'd1e50c9ad47e470f88e0ac2a5887d9c4'
);

-- 8. Tomato Septoria Spot
INSERT INTO diseases (id, name, cure, precaution, causes) VALUES (
    '88888888-8888-8888-8888-888888888888',
    'Tomato Septoria Spot',
    'Use chlorothalonil fungicide',
    'Space plants properly',
    'Septoria lycopersici'
);

INSERT INTO disease_products (id, disease_id, product_id) VALUES (
    'dprod-0008-0008-0008-000000000008',
    '88888888-8888-8888-8888-888888888888',
    '687ef43d54154591b8db20f164c24b41'
);

INSERT INTO disease_consultants (id, disease_id, consultant_id) VALUES (
    'dcons-0008-0008-0008-000000000008',
    '88888888-8888-8888-8888-888888888888',
    'a1d9a0e1577748b4af9266a0f5c5a775'
);


