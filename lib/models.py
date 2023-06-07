from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
# here we are importing date to help us with the formating of our publication date format
from datetime import datetime

# we start by creating the baseclass for our sqlite database 
Base = declarative_base()

engine = create_engine('sqlite:///Bookstore.db')
Base.metadata.bind = engine

if __name__ == "__main__":
   
 Session = sessionmaker(bind=engine)

# defining the many-to-many relationship book and genre and 
#Book class has a many-to-many relationship with the Genre class
book_genre_table = Table('book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.book_id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.genre_id'), primary_key=True)
 )
# we defining the book class with its columns and the relationships
class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publication_date = Column(Date)
    price = Column(Float)
    quantity = Column(Integer)
    
    #Book class has a many-to-many relationship with the Genre class
    genres = relationship("Genre", secondary=book_genre_table, back_populates="books")
    #Book class has a one-to-many relationship with the Order class
    orders = relationship("Order", back_populates="book")

    # we define functions for our book contex for adding,updating,displaying and deleting books to and from our store.
def add_book(title, author, publication_date, price, quantity):
    session = Session()
    new_book = Book(title=title, author=author, publication_date=publication_date, price=price, quantity=quantity)
    session.add(new_book)
    session.commit()

    print(f"Book '{title}' by {author} added to the database.")

def update_book(book_id, title, author, publication_date, price, quantity):
    session = Session()
    book = session.query(Book).filter(Book.book_id == book_id).one()
    book.title = title
    book.author = author
    book.publication_date = publication_date
    book.price = price
    book.quantity = quantity
    session.commit()

    print(f"Book ID {book_id} updated in the database.")

def display_books():
    session = Session()
    books = session.query(Book).all()
    session.commit()
    print("\n*** Books ***")
    for book in books:
     print(f"ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Publication Date: {book.publication_date}, Price: {book.price}, Quantity: {book.quantity}")

def delete_book(book_id):
    session = Session()
    book = session.query(Book).filter(Book.book_id == book_id).one()
    session.delete(book)
    session.commit()
    print(f"Book ID {book_id} deleted from the database.")

# we also defining our order class with its columns and relationships
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

    # we defining functions in context to our order class for creating,displaying and deleting orders
def create_order(customer_id, book_id, order_date, quantity):
    session = Session()
    new_order = Order(customer_id=customer_id, book_id=book_id, order_date=order_date, quantity=quantity)
    session.add(new_order)
    session.commit()

    print(f"Order for customer ID {customer_id} and book ID {book_id} created.")

def display_orders():
    session = Session()
    orders = session.query(Order).all()
    print("\n*** Orders ***")
    for order in orders:
     print(f"ID: {order.order_id}, Customer ID: {order.customer_id}, Book ID: {order.book_id}, Order Date: {order.order_date}, Quantity: {order.quantity}")

def delete_order(order_id):
    session = Session()
    order = session.query(Order).filter(Order.order_id == order_id).one()
    session.delete(order)
    session.commit()

    print(f"Order ID {order_id} deleted from the database.")

# we also defininmg our class customer with its respective columns and relationships 
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    
    #Customer class has a one-to-many relationship with the Order class
    orders = relationship("Order", back_populates="customer")

    # Initializing our customer class function for adding, displaying and deleting customers
def add_customer(name, email, phone):
    session = Session()
    new_customer = Customer(name=name, email=email, phone=phone)
    session.add(new_customer)
    session.commit()
    
    print(f"Customer '{name}' added to the database.")

def display_customers():
    session = Session()
    customers = session.query(Customer).all()
    session.commit()
    print("\n*** Customers ***")
    for customer in customers:
     print(f"ID: {customer.customer_id}, Name: {customer.name}, Email: {customer.email}, Phone: {customer.phone}")

def delete_customer(customer_id):
    session = Session()
    customer = session.query(Customer).filter(Customer.customer_id == customer_id).one()
    session.delete(customer)
    session.commit()

    print(f"Customer ID {customer_id} deleted from the database.")

def display_all():
    print("\n*** Display All ***")
    display_books()
    display_customers()
    display_orders()

# Here we are also difining our genre class
class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    name = Column(String)
    
    #Genre class has a many-to-many relationship with the Book class
    books = relationship("Book", secondary=book_genre_table, back_populates="genres")

    # we are defining this function main to handle our user input and calls the appropriate functions
def main():
    print("Welcome to the Bookstore!")
    user_name = input("Please enter your name: ")
    print(f"Welcome, {user_name}!")

    global Session
    Session = sessionmaker(bind=engine) 
    while True:
        print("\n*** Bookstore Services ***")
        print("1. Add a book")
        print("2. Update a book")
        print("3. Display books")
        print("4. Delete a book")
        print("5. Add a customer")
        print("6. Display customers")
        print("7. Delete a customer")
        print("8. Create an order")
        print("9. Display orders")
        print("10. Delete an order")
        print("11. Display All in Store")
        print("12.Exit")

        choice = int(input("\nPlease select an option (1-11): "))

        if choice == 1:
            title = input("Enter the book title: ")
            author = input("Enter the book author: ")
            publication_date_str = input("Enter the publication date (DD-MM-YYYY): ")
            publication_date=datetime.strptime(publication_date_str, "%d-%m-%Y").date()
            price = float(input("Enter the book price: "))
            quantity = int(input("Enter the book quantity: "))
            add_book(title, author, publication_date, price, quantity)
        elif choice == 2:
            book_id = int(input("Enter the book ID to update: "))
            title = input("Enter the new book title: ")
            author = input("Enter the new book author: ")
            publication_date_str= input("Enter the new publication date (DD-MM-YYYY): ")
            publication_date = datetime.strptime(publication_date_str, "%d-%m-%Y").date()
            price = float(input("Enter the new book price: "))
            quantity = int(input("Enter the new book quantity: "))
            update_book(book_id, title, author, publication_date, price, quantity)

        elif choice ==3:
            display_books()    

        elif choice == 4:
            book_id = int(input("Enter the book ID to delete: "))
            delete_book(book_id)
        elif choice == 5:
            name = input("Enter the customer's name: ")
            email = input("Enter the customer's email: ")
            phone = input("Enter the customer's phone number: ")
            add_customer(name, email, phone)
        elif choice ==6:
            display_customers()    
        elif choice == 7:
            customer_id = int(input("Enter the customer ID to delete: "))
            delete_customer(customer_id)
        elif choice == 8:
            customer_id = int(input("Enter the customer ID: "))
            book_id = int(input("Enter the book ID: "))
            order_date_str = input("Enter the order date (DD-MM-YYYY): ")
            order_date = datetime.strptime(order_date_str, "%d-%m-%Y").date()
            quantity = int(input("Enter the order quantity: "))
            create_order(customer_id, book_id, order_date, quantity)
        elif choice ==9:
            display_orders()    
        elif choice == 10:
            order_id = int(input("Enter the order ID to delete: "))
            delete_order(order_id)
        elif choice == 11:
            display_all()    
        elif choice == 12:
            print("Exiting the Bookstore application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# this is helping us run the the main function if the script is run directly
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()