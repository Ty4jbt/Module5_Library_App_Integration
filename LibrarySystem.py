
# Importing the required classes
from db_connection import get_connection
from Book import Book
from User import User
from Author import Author

class LibrarySystem:

    # Constructor
    def __init__(self):
        self.db = get_connection()
        self.cursor = self.db.cursor()

    # Methods
    def add_book(self, book):

        author_name = book.get_author_id()

        author_id = self.find_author_by_name(book.get_author_id())

        if not author_id:
            author = Author(author_name, "")

            author_id = self.add_author(author)

        query = "INSERT INTO books (title, author_id, isbn, publication_date) VALUES (%s, %s, %s, %s)"

        values = (book.get_title(), author_id, book.get_isbn(), book.get_publication_date())

        self.cursor.execute(query, values)
        
        self.db.commit()

    def add_user(self, user):
        
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s)"

        values = (user.get_name(), user.get_library_id())

        self.cursor.execute(query, values)

        self.db.commit()

    def add_author(self, author):
        
        query = "INSERT INTO authors (name, biography) VALUES (%s, %s)"

        values = (author.get_name(), author.get_biography())

        self.cursor.execute(query, values)

        self.db.commit()

        return self.cursor.lastrowid

    def find_book(self, title):
        
        query = """

        SELECT b.id, b.title, a.name, b.isbn, b.publication_date, b.availability
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.title = %s
        """

        self.cursor.execute(query, (title, ))

        book = self.cursor.fetchone()

        if book:
            return Book(None, book[1], book[2], book[3], book[4], book[5])

        return None

    def find_user(self, library_id):
        
        query = "SELECT * FROM users WHERE library_id = %s"

        self.cursor.execute(query, (library_id, ))

        user = self.cursor.fetchone()

        if user:
            return User(user[1], user[2])
        
        return None

    def find_author_by_name(self, name):
        
        query = "SELECT name, biography FROM authors WHERE name = %s"

        self.cursor.execute(query, (name, ))

        author = self.cursor.fetchone()

        if author:
            return Author(author[0], author[1])
        else:
            print("Author not found")
            return None

    def borrow_book(self, user, book_title):

        book = self.find_book(book_title)
        
        if book and book.get_availability():
            
            update_query = "UPDATE books SET availability = FALSE WHERE title = %s"

            self.cursor.execute(update_query, (book_title, ))

            insert_query = "INSERT INTO borrowed_books (user_id, book_id, borrowed_date) VALUES (%s, %s, CURDATE())"

            self.cursor.execute(insert_query, (user.get_library_id(), book.get_id()))

            self.db.commit()

            return True

        return False
    
    def return_book(self, user, book_title):
        
        book = self.find_book(book_title)

        if book:
            update_book_query = "UPDATE books SET availability = TRUE WHERE title = %s"

            self.cursor.execute(update_book_query, (book_title, ))

            update_borrowed_books_query = "UPDATE borrowed_books SET return_date = CURDATE() WHERE user_id = %s AND book_id = %s and return_date IS NULL"

            self.cursor.execute(update_borrowed_books_query, (user.get_library_id(), book.get_id()))

            self.db.commit()

            return True
        
        return False

    def display_all_books(self):
        
        query = """
        SELECT b.id, b.title, a.name, b.isbn, b.publication_date, b.availability
        FROM books b
        JOIN authors a ON b.author_id = a.id
        """

        self.cursor.execute(query)

        books = self.cursor.fetchall()

        for book in books:
            print(f"Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Publication Date: {book[4]}, Availibility: {book[5]}")

    def display_all_users(self):
        
        query = "SELECT * FROM users"

        self.cursor.execute(query)

        users = self.cursor.fetchall()

        for user in users:
            print(f"Name: {user[1]}, Library ID: {user[2]}")

    def display_all_authors(self):
       
        query = "SELECT * FROM authors"

        self.cursor.execute(query)

        authors = self.cursor.fetchall()

        for author in authors:
            print(f"Name: {author[1]}, Biography: {author[2]}")