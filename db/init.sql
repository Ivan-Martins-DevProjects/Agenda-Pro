CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(10),
    instance VARCHAR(255),
    isconnected BOOLEAN,
    nome VARCHAR(50)
);

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    userid VARCHAR(250) NOT NULL,
    clientid VARCHAR(250),
    nome VARCHAR(50),
    email VARCHAR(100),
    last_contact TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    status VARCHAR(255) DEFAULT 'true',
    telefone VARCHAR(20),

    CONSTRAINT fk_user
        FOREIGN KEY(userid)
        REFERENCES users(id)
        ON DELETE CASCADE
);
