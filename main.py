from addressBook import AddressBook, Record
import re
import pickle


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    contact = book.find(name)
    if contact is None:
        return f"Contact {name} not found."
    return ', '.join(p.value for p in contact.phones)

def show_all(args, book):
    return '\n'.join(str(record) for record in book.values())

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    else:
        return "Contact or birthday not found."
    
@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return '\n'.join(f"{record.name.value} - {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming)
    else:
        return "No upcoming birthdays."


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
                print(add_contact(args, book))
            
        elif command == "change":
                print(change_phone(args, book))
            
        elif command == "phone":
            if len(args) == 1:
                print(show_phone(args, book))
            else:
                print("Command 'phone' should have two arguments: name.")

        elif command == "all":
            print(show_all(args, book))


        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))


        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")
        
if __name__ == "__main__":
    main()