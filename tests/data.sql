INSERT INTO users (username, email, password, role_id)
VALUES
  ('test', 'test.email@example.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 0),
  ('other', 'other.email@example.com', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 2);

INSERT INTO items (item, description, stock_size, available)
VALUES
  ('test item', 'fake description', 10, 5);

