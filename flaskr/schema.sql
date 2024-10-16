DROP TABLE IF EXISTS shelves;
DROP TABLE IF EXISTS generic_shelf;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS items_rent_control;

CREATE TABLE shelves (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE generic_shelf (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  stock_size INTEGER NOT NULL,
  available INTEGER
);

CREATE TABLE clients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  age INTEGER
);

CREATE TABLE items_rent_control (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  client_id INTEGER NOT NULL,
  rent_date DATE NOT NULL,
  return_date DATE,
  FOREIGN KEY (item_id) REFERENCES generic_shelf(id),
  FOREIGN KEY (client_id) REFERENCES clients(id)
);
