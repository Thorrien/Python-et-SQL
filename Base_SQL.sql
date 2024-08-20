
CREATE TABLE IF NOT EXISTS role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO role (id, role) VALUES
(1, 'Admin'),
(2, 'Management'),
(3, 'Sale'),
(4, 'Support');

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

INSERT INTO user (nom, email, mot_de_passe, role_id)
VALUES ('VotreNom', 'VotreNom@domaine.com', 'MotDePasse', 1);


CREATE TABLE IF NOT EXISTS company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    company_name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    address VARCHAR(255),
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);


CREATE TABLE IF NOT EXISTS client_contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compagny_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    signatory BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (compagny_id) REFERENCES company(id)
);


CREATE TABLE IF NOT EXISTS event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_date_start DATE NOT NULL,
    event_date_end DATE NOT NULL,
    location TEXT NOT NULL,
    id_user INT,
    attendees INT NOT NULL,
    notes TEXT,
    FOREIGN KEY (id_user) REFERENCES user(id)
);


CREATE TABLE IF NOT EXISTS contract (
    id CHAR(36) PRIMARY KEY,
    compagny_id INT NOT NULL,
    user_id INT,
    total_amont FLOAT NOT NULL,
    current_amont FLOAT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    sign BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (compagny_id) REFERENCES company(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);


CREATE TABLE IF NOT EXISTS event_contract (
    event_id INT NOT NULL,
    contract_id CHAR(36) NOT NULL,
    PRIMARY KEY (event_id, contract_id),
    FOREIGN KEY (event_id) REFERENCES event(id),
    FOREIGN KEY (contract_id) REFERENCES contract(id)
);


CREATE TABLE IF NOT EXISTS texts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data VARCHAR(3000) NOT NULL
);