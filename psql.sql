CREATE OR REPLACE FUNCTION updated_row() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = date_trunc('second', now());
    RETURN NEW; 
END;
$$ language 'plpgsql';

CREATE TABLE users (
    id serial NOT NULL PRIMARY KEY,
    username varchar(255) NOT NULL,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER users_update_row BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE updated_row();

CREATE TABLE stores (
    id serial NOT NULL PRIMARY KEY,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())
);
CREATE TRIGGER stores_update_row BEFORE UPDATE ON stores FOR EACH ROW EXECUTE PROCEDURE updated_row();

CREATE TABLE products (
    id serial NOT NULL PRIMARY KEY,
    created_at      timestamp       DEFAULT date_trunc('second',now()),
    updated_at      timestamp       DEFAULT date_trunc('second',now())

);
CREATE TRIGGER products_update_row BEFORE UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE updated_row();
