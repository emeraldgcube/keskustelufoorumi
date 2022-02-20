CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    rights INTEGER
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    topic_id INTEGER REFERENCES topics
    
);
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    title TEXT,
    forum_id INTEGER REFERENCES forums
    
);

CREATE TABLE bans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    given_at TIMESTAMP,
    reason TEXT
);
CREATE TABLE forums (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    hidden BOOLEAN
);
