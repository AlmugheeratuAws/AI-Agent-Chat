import time
import json
from app.database import SessionLocal
from app.models import Book, Order, OrderItem, ToolCall


def order_status(order_id: int):
    db = SessionLocal()

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        db.close()
        return {"error": "Order not found"}

    items = (
        db.query(OrderItem, Book)
        .join(Book, Book.isbn == OrderItem.isbn)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    result = {
        "order_id": order.id,
        "customer_id": order.customer_id,
        "items": [
            {
                "title": book.title,
                "qty": item.qty,
                "price": book.price
            }
            for item, book in items
        ]
    }

    db.close()
    return result


def restock_book(isbn: str, qty: int):
    db = SessionLocal()

    book = db.query(Book).filter(Book.isbn == isbn).first()
    if not book:
        db.close()
        return {"error": "Book not found"}

    book.stock += qty
    db.commit()

    result = {"isbn": isbn, "new_stock": book.stock}
    db.close()
    return result


def update_price(isbn: str, price: int):
    db = SessionLocal()

    book = db.query(Book).filter(Book.isbn == isbn).first()
    if not book:
        db.close()
        return {"error": "Book not found"}

    book.price = price
    db.commit()

    result = {"isbn": isbn, "new_price": price}
    db.close()
    return result


def inventory_summary():
    db = SessionLocal()
    books = db.query(Book).all()

    result = {
        "total_titles": len(books),
        "low_stock": [
            {"title": b.title, "stock": b.stock}
            for b in books if b.stock < 3
        ]
    }

    db.close()
    return result


def find_books(q: str, by: str | None = None):
    db = SessionLocal()

    if by == "title":
        books = db.query(Book).filter(Book.title.contains(q)).all()
    elif by == "author":
        books = db.query(Book).filter(Book.author.contains(q)).all()
    else:
        books = db.query(Book).filter(
            (Book.title.contains(q)) | (Book.author.contains(q))
        ).all()

    result = [
        {
            "isbn": b.isbn,
            "title": b.title,
            "author": b.author,
            "stock": b.stock,
            "price": b.price,
        }
        for b in books
    ]

    db.close()
    return result


def create_order(customer_id: int, items: list):
    db = SessionLocal()

    order = Order(
        id=int(time.time()),
        customer_id=customer_id
    )
    db.add(order)
    db.flush()

    order_id = order.id

    for item in items:
        book = db.query(Book).filter(Book.isbn == item["isbn"]).first()

        if not book:
            db.close()
            raise ValueError("Book not found")

        if book.stock < item["qty"]:
            db.close()
            raise ValueError("Not enough stock")

        book.stock -= item["qty"]
        db.add(OrderItem(
            order_id=order_id,
            isbn=item["isbn"],
            qty=item["qty"]
        ))

    db.commit()
    db.close()

    return {"order_id": order_id, "status": "created"}


