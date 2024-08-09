from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str("Field: value: {self.value}")

class Name(Field):
    def __str__(self):
        return str(self.value)

class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)
        
    def __str__(self):
        return str("Phone: value: {self.value}")
    

class Birthday(Field):
        def __init__(self, value):
            try:
                self.value = datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone == phone_number:
                return phone
        return None

    def add_phone(self, phone):
            self.phones.append(Phone(phone))
            
        
    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            return ('This phone desn`t exist')
        
    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            return ('This phone desn`t exist')
        
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        
    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = ', '.join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Name: {self.name}, Phones: {phones}, Birthday: {birthday}"
    
    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            
    def get_upcoming_birthdays(self, within_days=7):
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                days_to_birthday = record.days_to_birthday()
                if 0 <= days_to_birthday <= within_days:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays