import re

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}


    def get_email(self):
        return self.email


    def change_email(self, address):
        try:
            self.email = address
            return "Email for {} successfully updated.".format(self.name)
        except:
            "There was an error updating the email address for {}.".format(self.name)


    def __repr__(self):
        return "User {name}, email: {email}, books read: {books}".format(name = self.name, email = self.email, books = len(self.books.keys()))


    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email


    def read_book(self, book, rating = None):
        if (type(rating) == int and 0 <= rating <= 4) or rating == None:
            self.books[book] = rating
        else:
            return "An invalid rating was submitted for the following read book: {}".format(book.get_title())


    def get_average_rating(self):
        rating_sum = 0
        rating_list = []
        for i in self.books.values():
            if i != None:
                rating_list.append(i)
        for i in rating_list:
            rating_sum += i
        if len(rating_list) != 0:
            return rating_sum / len(rating_list)
        else:
            return 0



class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []


    def get_title(self):
        return self.title


    def get_isbn(self):
        return self.isbn


    def _set_isbn(self, new_isbn):
        """
            This method has been switched to use the weak 'internal use' designation
            in order to ensure unique ISBNs and prevent hash issues in the
            TomeRater.books dict. It is called only by the 'set_isbn' method
            in the TomeRater class. The populate.py script will generate an error
            when trying to call novel1.set_isbn() method. It should be updated to
            call Tome_Rater.set_isbn() and pass in book and new ISBN.
        """
        self.isbn = new_isbn
        print("ISBN for {} successfully updated.".format(self.title))


    def add_rating(self, rating):
        if (type(rating) == int and 0 <= rating <= 4) or rating == None:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")


    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn


    def get_average_rating(self):
        rating_sum = 0
        rating_list = []
        for i in self.ratings:
            if i != None:
                rating_list.append(i)
        if len(rating_list) == 0:
            return 0
        else:
            for i in rating_list:
                rating_sum += i
            return rating_sum / len(rating_list)


    def __hash__(self):
        return hash((self.title, self.isbn))


    def __repr__(self):
        """ Added for consistency when being printed """
        return "Book title: {title} with ISBN: {isbn}".format(title = self.title, isbn = self.isbn)



class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author


    def get_author(self):
        return self.author


    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)



class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level


    def get_subject(self):
        return self.subject


    def get_level(self):
        return self.level


    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)



class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}


    def isbn_unique(self, isbn):
        for i in self.books.keys():
            if isbn == i.get_isbn():
                return False
        return True


    def create_book(self, title, isbn):
        if self.isbn_unique(isbn):
            new_book = Book(title, isbn)
            self.books[new_book] = 0
            return new_book
        else:
            print("Duplicate ISBN found for {num}, {title}".format(num = isbn, title = title))


    def create_novel(self, title, author, isbn):
        if self.isbn_unique(isbn):
            new_novel = Fiction(title, author, isbn)
            self.books[new_novel] = 0
            return new_novel
        else:
            print("Duplicate ISBN found for {num}, {title}".format(num = isbn, title = title))


    def create_non_fiction(self, title, subject, level, isbn):
        if self.isbn_unique(isbn):
            new_non_fiction = Non_Fiction(title, subject, level, isbn)
            self.books[new_non_fiction] = 0
            return new_non_fiction
        else:
            print("Duplicate ISBN found for {num}, {title}".format(num = isbn, title = title))


    def set_isbn(self, book, isbn):
        """
        This method updates ISBNs for book objects and prevents the hash issues
        that occur if set_isbn() was called directly from the Book object. It calls
        the Book._set_isbn "semi-private" method, which is not exposed via
        the wildcard import statement in populate.py.
        """
        if book in self.books:
            read_count = self.books.pop(book)
            book._set_isbn(isbn)
            self.books[book] = read_count



    def add_book_to_user(self, book, email, rating = None):
            if email in self.users:
                user = self.users[email]
                user.read_book(book, rating)
                book.add_rating(rating)
                if book in self.books:
                    self.books[book] += 1
                else:
                    self.books[book] = 1
            else:
                print("No user with email {email}!".format(email = email))


    def add_user(self, name, email, user_books = None):
        if re.search("^\w+@\w+\.(com|edu|org)$", email) != None:
            if email not in self.users:
                new_user = User(name, email)
                self.users[email] = new_user
                if type(user_books) == list:
                    for i in user_books:
                        self.add_book_to_user(i, email)
            else:
                print("User with email address {address} already exists!".format(address = email))
        else:
            print("{mail} is not a valid email address".format(mail = email))


    def print_catalog(self):
        print("\nThe following books are in the catalog:")
        for i in self.books.keys():
            print(i.get_title() + " " + str(i.get_isbn()))


    def print_users(self):
        print("\nThere are {num} users:".format(num = len(self.users.values())))
        for i in self.users.values():
            print(i)
        print("\n")


    def most_read_book(self):
        read_count = 0
        read_book = ""
        for book, count in self.books.items():
             if count > read_count:
                 read_count = count
                 read_book = book.get_title()
        if read_count > 0:
            return read_book + "\n"
        else:
            return "\nNo books read yet."


    def highest_rated_book(self):
        highest_average = 0
        book_title = ""
        for i in self.books.keys():
            average = i.get_average_rating()
            if average > highest_average:
                highest_average = average
                book_title = i.get_title()
        return "{name} has an everage rating of {rating}".format(name = book_title, rating = highest_average)


    def most_positive_user(self):
        highest_average = 0
        positive_user = ''
        for i in self.users.values():
            average = i.get_average_rating()
            if average > highest_average:
                highest_average = average
                positive_user = i.name
        return positive_user
