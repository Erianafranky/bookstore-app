from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#Book class has a many-to-many relationship with the Genre class
book_genre_table = Table('book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.book_id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.genre_id'), primary_key=True)
 )

class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publication_date = Column(Date)
    price = Column(Float)
    quantity = Column(Integer)
    
    #Book class has a one-to-many relationship with the Order class
    genres = relationship("Genre", secondary=book_genre_table, back_populates="books")
    orders = relationship("Order", back_populates="book")

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    order_date = Column(Date)
    quantity = Column(Integer)
    
    #Order class has many-to-one relationships with both the Customer and Book classes
    customer = relationship("Customer", back_populates="orders")
    book = relationship("Book", back_populates="orders")

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    
    #Customer class has a one-to-many relationship with the Order class
    orders = relationship("Order", back_populates="customer")

class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    name = Column(String)
    
    #Genre class has a many-to-many relationship with the Book class
    books = relationship("Book", secondary=book_genre_table, back_populates="genres")
