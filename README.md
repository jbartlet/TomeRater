# TomeRater
I have added documentation inline within the TomeRater explaining
changes made to support unique ISBN functionality. These changes
will cause populate.py, as originally written, to throw an error
since the Book.set_isbn() method has been relocated to the TomeRater
class. The __hash__ method in Book was broken as it was based on a
mutable attribute, isbn. Updating the ISBN directly on the Book object
caused duplicate entries in the TomeRater.books dict since the hashes
were different pre and post ISBN update, despite the contents being the same.
The Book object is now removed from the dict, ISBN updated, and then the Book
is placed back into the dict with the new hash in tow.

