CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  full_name VARCHAR(150) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'reader' CHECK (role IN ('admin','librarian','reader')),
  student_id VARCHAR(30),
  phone VARCHAR(20),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE authors (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR(150) NOT NULL,
  bio TEXT
);

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  parent_id INT REFERENCES categories(id)
);

CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR(20) UNIQUE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  publisher VARCHAR(150),
  publish_year INT,
  language VARCHAR(30),
  cover_url VARCHAR(255),
  category_id INT REFERENCES categories(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE book_authors (
  book_id INT REFERENCES books(id) ON DELETE CASCADE,
  author_id INT REFERENCES authors(id) ON DELETE CASCADE,
  PRIMARY KEY (book_id, author_id)
);

CREATE TABLE book_copies (
  id SERIAL PRIMARY KEY,
  book_id INT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
  inventory_code VARCHAR(30) UNIQUE NOT NULL,
  shelf_location VARCHAR(50),
  status VARCHAR(20) DEFAULT 'available' CHECK (status IN ('available','loaned','reserved','lost','damaged'))
);

CREATE TABLE loans (
  id SERIAL PRIMARY KEY,
  copy_id INT NOT NULL REFERENCES book_copies(id),
  user_id UUID NOT NULL REFERENCES users(id),
  librarian_id UUID REFERENCES users(id),
  loan_date DATE DEFAULT CURRENT_DATE,
  due_date DATE NOT NULL,
  return_date DATE,
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','returned','overdue'))
);

CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  book_id INT NOT NULL REFERENCES books(id),
  user_id UUID NOT NULL REFERENCES users(id),
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','fulfilled','cancelled','expired')),
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP
);

CREATE TABLE fines (
  id SERIAL PRIMARY KEY,
  loan_id INT NOT NULL REFERENCES loans(id),
  amount NUMERIC(10,2) NOT NULL,
  reason VARCHAR(100),
  is_paid BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  paid_at TIMESTAMP
);

CREATE TABLE reviews (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  book_id INT REFERENCES books(id) ON DELETE CASCADE,
  rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE (user_id, book_id)
);

CREATE TABLE user_book_interactions (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  book_id INT REFERENCES books(id) ON DELETE CASCADE,
  type VARCHAR(20) CHECK (type IN ('view','loan','wishlist','search_click')),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recommendations (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  book_id INT REFERENCES books(id) ON DELETE CASCADE,
  score REAL,
  algorithm VARCHAR(30),
  generated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE notifications (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(40),
  message TEXT,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_books_title ON books (title);
CREATE INDEX idx_loans_user ON loans (user_id, status);
CREATE INDEX idx_interactions_user ON user_book_interactions (user_id);
