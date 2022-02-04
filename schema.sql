CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
CREATE TABLE moderators (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    given_at TIMESTAMP
);
CREATE TABLE bans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    given_at TIMESTAMP,
    reason TEXT
);
