from collections import UserList
import pickle

class NoteBook(UserList):
    
    def add_note(self, note):
        self.data.append(note)

    def delete_note(self, note):
        self.data.remove(note)

    def find_note(self, note_title):
        for note in self.data:

            if note_title == note.title.value:
                return note

        else:
            raise NoteNotFoundError(f"Note {note_title} doesn't exist.")
        
    def read_data(self):
        try:
            with open("note_book\\data.bin", "rb") as file:
                contacts = pickle.load(file)
        except FileNotFoundError:
            contacts = self
        except EOFError:
            contacts = self
        finally:
            return contacts
        
    def write_data(self):
        with open("note_book\\data.bin", "wb") as file:
            pickle.dump(self, file)


class NoteNotFoundError(Exception):
    pass


class Note:

    def __init__(self, title, body, tags):
        self.title = title
        self.body = body
        self.tags = tags

    def __repr__(self):
        return str(self.title)
    
    def __str__(self):
        return str(self.title)

    def add_tags(self, row_new_tags):
        new_tags = list(map(lambda x: Tag(x), row_new_tags.split()))
        self.tags.extend(new_tags)

    def edit_note(self, new_body):
        self.body = new_body

    def read_note(self):
        tags_values = list(map(lambda x: f"#{x}", self.tags))
        print(self.body, " ".join(tags_values), sep='\n')


class Field:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)
    

class Title(Field):

    def __init__(self, value):  
        if 1 <= len(value) <= 50:
            self.value = value
        else:
            raise AttributeError("Title length must be between 1 and 50 characters.")



class Body(Field):
    pass


class Tag(Field):

    def __init__(self, value):  
        if 1 <= len(value) <= 20:
            self.value = value
        else:
            raise AttributeError("Title length must be between 1 and 20 characters.")
    

if __name__ == '__main__':
    a = Note(Title('q'), Body('asd'), Tag('#'),)

    print([a])
