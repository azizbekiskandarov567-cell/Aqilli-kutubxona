import uuid
from sqlalchemy import (Column, Integer, String, Text, Boolean, DateTime, Date,
                        ForeignKey, SmallInteger, Float, Numeric, UniqueConstraint, CheckConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="reader")
    student_id = Column(String(30))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"))


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    bio = Column(Text)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    isbn = Column(String(20), unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    publisher = Column(String(150))
    publish_year = Column(Integer)
    language = Column(String(30))
    cover_url = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, server_default=func.now())


class BookCopy(Base):
    __tablename__ = "book_copies"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    inventory_code = Column(String(30), unique=True, nullable=False)
    shelf_location = Column(String(50))
    status = Column(String(20), default="available")


class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True)
    copy_id = Column(Integer, ForeignKey("book_copies.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    librarian_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    loan_date = Column(Date, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    status = Column(String(20), default="active")


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (UniqueConstraint("user_id", "book_id"),
                      CheckConstraint("rating BETWEEN 1 AND 5"))
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    rating = Column(SmallInteger)
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
