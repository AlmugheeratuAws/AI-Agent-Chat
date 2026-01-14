from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from datetime import datetime
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    isbn = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    stock = Column(Integer)
    price = Column(Integer)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    isbn = Column(String, ForeignKey("books.isbn"))
    qty = Column(Integer)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    role = Column(String)  # user | agent
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    name = Column(String)
    args_json = Column(Text)
    result_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

