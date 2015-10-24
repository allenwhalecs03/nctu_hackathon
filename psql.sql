DROP TABLE if EXISTS products;
DROP TABLE if EXISTS stores;
DROP TABLE if EXISTS users;
CREATE OR REPLACE FUNCTION updated_row() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = date_trunc('second', now());
    RETURN NEW; 
END;
$$ language 'plpgsql';

CREATE TABLE users (
    id              serial          NOT NULL PRIMARY KEY,
    username        varchar(255)    NOT NULL,
    account_id      varchar(255)    NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER users_update_row BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE updated_row();

CREATE TABLE stores (
    id              serial          NOT NULL PRIMARY KEY,
    user_id         integer         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            varchar(255)    NOT NULL,
    description     text,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER stores_update_row BEFORE UPDATE ON stores FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON stores (id)

CREATE TABLE products (
    id              serial          NOT NULL PRIMARY KEY,
    store_id        integer         NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    title           varchar(255),
    description     text,
    qrcode          varchar(255),
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER products_update_row BEFORE UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE updated_row();
CREATE INDEX ON products (store_id);
