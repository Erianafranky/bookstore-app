from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from colorama import init, Fore, Style

from models import Book, Customer, Order, Genre, Base

# Initialize colorama
init(autoreset=True)

# Create the engine and bind it to the session
engine = create_engine('sqlite:///db/bookstore.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def print_success(message):
    print(Fore.GREEN + message)

def print_error(message):
    print(Fore.RED + message)

def print_input(message):
    return input(Fore.YELLOW + message + Style.RESET_ALL)

def print_exit(message):
    print(Fore.CYAN + message)

def create_book():
    title = print_input("Enter the book title: ")
    author = print_input("Enter the author: ")
    publication_date_str = print_input("Enter the publication date (YYYY-MM-DD): ")
    price = float(print_input("Enter the price: "))
    quantity = int(print_input("Enter the quantity: "))
    genre_name = print_input("Enter the genre: ")

    # Convert the publication date string to a Python date object
    publication_date = datetime.strptime(publication_date_str, "%Y-%m-%d").date()

    # Check if the genre already exists in the database
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        print_error("Genre not found.")
        return
    
    book = Book(title=title, author=author, publication_date=publication_date, price=price, quantity=quantity)
    #Associate the book with the genre
    book.genres.append(genre)
    session.add(book)
    session.commit()
    print_success(f"Book '{title}' by {author} added successfully!")

def update_book():
    # Function to update an existing book record
    book_id = int(print_input("Enter the ID of the book you want to update: "))
    book = session.query(Book).filter_by(book_id=book_id).first()
    if not book:
        print_error("Book not found.")
        return

    # Get the updated book details
    title = print_input("Enter the updated title: ")
    author = print_input("Enter the updated author: ")
    publication_date_str = print_input("Enter the updated publication date (YYYY-MM-DD): ")
    price = float(print_input("Enter the updated price: "))
    quantity = int(print_input("Enter the updated quantity: "))

    # Update the book attributes
    book.title = title
    book.author = author
    book.publication_date = datetime.strptime(publication_date_str, "%Y-%m-%d").date()
    book.price = price
    book.quantity = quantity

    session.commit()
    print_success(f"Book ID {book_id} updated successfully!")


def delete_book():
    # Function to delete an existing book record
    book_id = int(print_input("Enter the ID of the book you want to delete: "))
    book = session.query(Book).filter_by(book_id=book_id).first()
    if not book:
        print_error("Book not found.")
        return

    session.delete(book)
    session.commit()
    print_success(f"Book ID {book_id} deleted successfully!")

def display_books():
    session = Session()
    books = session.query(Book).all()
    session.commit()
    print("\n*** Books ***")
    for book in books:
    #print_success(f"ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Publication Date: {book.publication_date}, Price: {book.price}, Quantity: {book.quantity}")
        print(f"{Fore.GREEN}ID: {Fore.BLUE}{book.book_id}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Title: {Fore.YELLOW}{book.title}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Author: {Fore.YELLOW}{book.author}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Publication Date: {Fore.CYAN}{book.publication_date}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Price: {Fore.MAGENTA}{book.price}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Quantity: {Fore.MAGENTA}{book.quantity}{Style.RESET_ALL}")


def create_customer():
    name = print_input("Enter the customer name: ")
    email = print_input("Enter the customer email: ")
    phone = print_input("Enter the customer phone: ")

    customer = Customer(name=name, email=email, phone=phone)
    session.add(customer)
    session.commit()
    print_success(f"Customer '{name}' added successfully!")

def display_customers():
    customers = session.query(Customer).all()
    session.commit()
    print("\n*** Customers ***")
    for customer in customers:
        print(f"{Fore.GREEN}ID: {Fore.BLUE}{customer.customer_id}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Name: {Fore.YELLOW}{customer.name}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Email: {Fore.YELLOW}{customer.email}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Phone: {Fore.CYAN}{customer.phone}{Style.RESET_ALL}, ")
        
def delete_customer():
    customer_id = int(print_input("Enter the ID of the customer you want to delete: "))
    customer = session.query(Customer).filter_by(customer_id=customer_id).one()
    if not customer:
        print_error("Customer not found.")
        return
    session.delete(customer)
    session.commit()
    print_success(f"Customer ID {customer_id} deleted successfully!")

def create_order():
    # Get customer
    customer_id = int(print_input("Enter the customer ID: "))
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        print_error("Customer not found.")
        return

    # Get book
    book_id = int(input("Enter the book ID: "))
    book = session.query(Book).filter_by(book_id=book_id).first()
    if not book:
        print_error("Book not found.")
        return

    order_date_str = print_input("Enter the order date (YYYY-MM-DD): ")
    quantity = int(print_input("Enter the quantity: "))

    # Convert the order date string to a Python date object
    order_date = datetime.strptime(order_date_str, "%Y-%m-%d").date()

    order = Order(customer=customer, book=book, order_date=order_date, quantity=quantity)
    session.add(order)
    session.commit()
    print_success(f"Order for customer ID {customer_id} created successfully!")

def display_orders():
    orders = session.query(Order).all()
    print_success("\n*** Orders ***")
    for order in orders:
        print(f"{Fore.GREEN}Order ID: {Fore.BLUE}{order.order_id}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Customer: {Fore.YELLOW}{order.customer.name}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Book: {Fore.YELLOW}{order.book.title}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Quantity: {Fore.CYAN}{order.quantity}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Date: {Fore.MAGENTA}{order.order_date}{Style.RESET_ALL}, ")

def delete_order():
    order_id = int(print_input("Enter the order ID you want to delete: "))
    order = session.query(Order).filter_by(order_id=order_id).one()
    if not order:
        print_error("Order not found.")
        return
    session.delete(order)
    session.commit()

    print_success(f"Order ID {order_id} deleted from the database.")

def search_books_by_genre():
    genre_name = print_input("Enter the genre name to search for books: ")
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        print_error("Genre not found.")
        return

    books = genre.books
    if not books:
        print_error("No books found for the given genre.")
        return

    print_exit("\nBooks in the '{}' Genre:".format(genre_name))
    for book in books:
        #print_success("Title: {}, Author: {}".format(book.title, book.author))
        title_key = f"{Fore.GREEN}Title: {Style.RESET_ALL}"
        author_key = f"{Fore.GREEN}Author: {Style.RESET_ALL}"
        title_value = f"{Fore.YELLOW}{book.title}{Style.RESET_ALL}"
        author_value = f"{Fore.YELLOW}{book.author}{Style.RESET_ALL}"

        print_success(f"{title_key} {title_value}, {author_key} {author_value}")


if __name__ == '__main__':
    while True:
        print("\n--- Bookstore CLI ---")
        print_success("\n*** Our Bookstore Services ***")
        print("1. Create Book")
        print("2. Create Customer")
        print("3. Create Order")
        print("4. Display Books")
        print("5. Display Customers")
        print("6. Display Orders")
        print("7. Update Book")
        print("8. Delete Book")
        print("9. Delete Customer")
        print("10. Delete an order")
        print("11. Search Books by Genre")
        print("12. Exit")

        choice = print_input("Enter your choice: ")

        if choice == '1':
            create_book()
        elif choice == '2':
            create_customer()
        elif choice == '3':
            create_order()
        elif choice == '4':
            display_books()
        elif choice == '5':
            display_customers()
        elif choice == '6':
            display_orders()
        elif choice == '7':
            update_book()
        elif choice == '8':
            delete_book()
        elif choice == '9':
            delete_customer()
        elif choice == '10':
            delete_order()
        elif choice == '11':
            search_books_by_genre()
        elif choice == '12':
            print_exit("Exiting the Bookstore application. Goodbye!")
            break
        else:
            print_error("Invalid option. Please try again.")


