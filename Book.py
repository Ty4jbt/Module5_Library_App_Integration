
class Book:

    # Constructor
    def __init__(self, id, title, author_name, isbn, publication_date, availability=True):
        self.__id = id
        self.__title = title
        self.__author_name = author_name
        self.__isbn = isbn
        self.__publication_date = publication_date
        self.__availability = availability

    # Getters

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_author_name(self):
        return self.__author_name

    def get_isbn(self):
        return self.__isbn

    def get_publication_date(self):
        return self.__publication_date

    def get_availability(self):
        return self.__availability

    # Setters

    def set_availability(self, status):
        self.__availability = status

    def __str__(self):
        return f"{self.__title}, Author: {self.__author_name}, ISBN: {self.__isbn}, Publication Date: {self.__publication_date} - {'Available' if self.__availability else 'Borrowed'}"