DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    uid serial NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    -- created_date DATE DEFAULT CURRENT_DATE
    created_date TIMESTAMP(0) WITH TIME ZONE DEFAULT NOW()
);

-- postgres sha256 cannot be unhashed by sha256_crypt
-- The set 'scram-sha-256' doesn't work either:
-- set password_encryption = 'scram-sha-256';
-- INSERT INTO users (username, password) VALUES ('Michelle', sha256('test_pw1'));
-- INSERT INTO users (username, password) VALUES ('Jasmine', sha256('test_pw2'));
INSERT INTO users (username, password) VALUES ('Michelle', 'test_pw1');
INSERT INTO users (username, password) VALUES ('Jasmine', 'test_pw2');

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    pid serial NOT NULL PRIMARY KEY,
    author serial NOT NULL,
    content TEXT NOT NULL,
    -- created_date DATE DEFAULT CURRENT_DATE
    created_date TIMESTAMP(0) WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (author) REFERENCES users(uid)
);

INSERT INTO posts (author, content) VALUES (1, 'test_post_1');
INSERT INTO posts (author, content) VALUES (2, 'test_post_2');
