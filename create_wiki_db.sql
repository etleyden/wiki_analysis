BEGIN;

CREATE TABLE IF NOT EXISTS page(
    title TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS link(
    from_page TEXT,
    to_page TEXT,
    rank INTEGER NOT NULL,
    FOREIGN KEY(from_page) REFERENCES page(title),
    FOREIGN KEY(to_page) REFERENCES page(title),
    PRIMARY KEY(from_page, to_page)
);

CREATE TABLE IF NOT EXISTS keyword(
    page_title TEXT,
    keyword TEXT,
    rank INTEGER,
    FOREIGN KEY(page_title) REFERENCES page(title),
    PRIMARY KEY(page_title, keyword)
);

COMMIT;