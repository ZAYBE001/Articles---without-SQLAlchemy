-- lib/db/schema.sql
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS magazines;
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS magazines (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER,
    magazine_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(id)
);