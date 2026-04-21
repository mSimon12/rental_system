DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS items_rent_control;

CREATE TABLE roles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  role TEXT(50) UNIQUE NOT NULL
);

INSERT INTO roles (id, role) VALUES
    (0, "Admin"),
    (1, "Employee"),
    (2, "User");

CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  stock_size INTEGER NOT NULL,
  available INTEGER
);

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT(50) UNIQUE NOT NULL,
  email TEXT(50) UNIQUE NOT NULL,
  password TEXT(128) NOT NULL,
  role_id INTEGER NOT NULL,
  FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE items_rent_control (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  rent_date DATE NOT NULL,
  return_date DATE,
  FOREIGN KEY (item_id) REFERENCES generic_shelf(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
