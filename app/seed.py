from app.database import engine, SessionLocal, Base
from app.models import Book, Customer

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Seed books
db.add_all([
    Book(isbn="111", title="Clean Code", author="Robert C. Martin", stock=10, price=30),
    Book(isbn="222", title="The Pragmatic Programmer", author="Andrew Hunt", stock=5, price=40),
])

# Seed customers
db.add_all([
    Customer(id=1, name="Alice", email="alice@mail.com"),
    Customer(id=2, name="Bob", email="bob@mail.com"),
])

db.commit()
db.close()

print("Database seeded successfully.")

