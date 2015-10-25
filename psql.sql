DROP TABLE if EXISTS records;
DROP TABLE if EXISTS products;
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

CREATE TABLE products (
    id              serial          NOT NULL PRIMARY KEY,
    user_id         integer         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            varchar(255)    NOT NULL DEFAULT '快速交易 at ' || date_trunc('second',now()),
    price           integer         NOT NULL DEFAULT 100,
    description     text,
    qrcode          varchar(255),
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER products_update_row BEFORE UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE updated_row();

CREATE TABLE records (
    id              serial          NOT NULL PRIMARY KEY,
    from_user_id    integer         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    to_user_id      integer         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id      integer         NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    latitude        integer         DEFAULT -1,
    longitude       integer         DEFAULT -1,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER records_update_row BEFORE UPDATE ON records FOR EACH ROW EXECUTE PROCEDURE updated_row();
