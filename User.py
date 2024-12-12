
class User:

    # Constructor
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id

    # Getters

    def get_name(self):
        return self.__name

    def get_library_id(self):
        return self.__library_id

    def __str__(self):
        return f"User: {self.__name}, Library ID: {self.__library_id}"