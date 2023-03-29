from collections import UserDict



class Field:
    def __init__(self, value=None):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    pass
        
class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)
        
    def change_phone(self, index, phone):
        self.phones[index] = phone
        
    def delete_phone(self, phone):
        self.phones.remove(phone)
    
class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        self.data[name] = record
        

contacts = AddressBook()

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError:
            return "Number is incorrect"
        except KeyError:
            return "There is no contact with that name"
        except IndexError:
            return "Give me a name and phone please"
    return wrapper

def help(*args):
    return """
help: To see this message
add <Name> <phone>: add contact
change <Name> <new_phone>: change contact's name of phone
show all: List of contacts
hello: hello
phone <Name>: To see phone number of <Name>
exit: If you want to exit
"""

def hello(*args):
    return "How can I help you?"


@input_error
def add(*args):
    obj = args[0].split()
    name = Name(obj[0])
    phone = Phone(obj[1])
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return f"Added <{name.value}> with phone <{phone.value}>"

@input_error
def phone(*args):
    name = args[0]
    if name in contacts.data:
        for key, val in contacts.data.items():
            record = contacts.data[key]
            if name == key:
                return f"{name}: {', '.join(str(phone) for phone in record.phones)}"
    raise KeyError
            

@input_error
def change(*args):
    obj = args[0].split()
    name = Name(obj[0])
    phone = Phone(obj[1])
    record = contacts[name.value]
    record.change_phone(0, phone)
    return f"Changed phone <{phone}>, with name <{name}>"

@input_error
def show_all(*args):
    list = []
    if len(contacts.data) == 0:
        return "list of contacts is empty..."
    for k, v in contacts.data.items():
        record = contacts.data[k]
        list.append(f"{k}: {', '.join(str(phone) for phone in record.phones)}")
    return "\n".join([f"{item}"for item in list])
    
@input_error
def exit(*args):
    return "Good bye"

@input_error
def unknown_command(*args):
    return "Invalid command"

COMMANDS = {
    help:"help",
    hello:"hello",
    add:"add",
    phone:"phone",
    change:"change",
    show_all:"show all",
    exit:"exit"
}


def handler(string):
    for key, value in COMMANDS.items():
        if string.startswith(value):
            return key, string.replace(value, "").strip()
    return unknown_command, contacts

def main():
    while True:
        user_input = input("Enter command: ")
        command, data = handler(user_input)
        print(command(data))
        if command == exit:
            break
        
if __name__ == "__main__":
    print(hello() + " Type <help> if you need help.")
    main()