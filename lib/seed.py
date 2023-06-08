from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from sqlalchemy.exc import IntegrityError

from models import Book, Customer, Order, Genre, Base

# Create the engine and bind it to the session
engine = create_engine('sqlite:///db/bookstore.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.query(Book).delete()
session.query(Customer).delete()
session.query(Order).delete()
session.query(Genre).delete()

# Seed the database with sample data
def seed_data():
    # Create genres
    genre1 = Genre(name='Fiction')
    genre2 = Genre(name='Science Fiction')
    genre3 = Genre(name='Non Fiction')
    genre4 = Genre(name='Narrative')
    genre5 = Genre(name='Novel')
    session.add_all([genre1, genre2, genre3, genre4, genre5])

    # Create books
    book1 = Book(title='Queen of Eternity', author='Olivia Smith', publication_date=date(2021, 1, 1), price=9.99, quantity=10)
    book2 = Book(title='Aliens and Armies', author='Diana Johnson', publication_date=date(2021, 2, 1), price=14.99, quantity=5)
    book3 = Book(title='Queen of The South', author='John Obama', publication_date=date(2022, 10, 10), price=20.99, quantity=20)

    session.add_all([book1, book2, book3])
    session.commit()
    try:
        book1.genres.append(genre1)
        book2.genres.append(genre1)
        book2.genres.append(genre2)
        book3.genres.append(genre2)
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Error: Genre already assigned to the book.")


    # Create customers
    customer1 = Customer(name='Duncan Andrew', email='dun@example.com', phone='1234567890')
    customer2 = Customer(name='Ken Nicholas', email='ken@example.com', phone='9876543210')
    session.add_all([customer1, customer2])

    # Create orders
    order1 = Order(customer=customer1, book=book1, order_date=date(2021, 3, 1), quantity=2)
    order2 = Order(customer=customer2, book=book2, order_date=date(2021, 4, 1), quantity=1)
    session.add_all([order1, order2])

    # Commit the changes to the database
    session.commit()

if __name__ == '__main__':
    seed_data()