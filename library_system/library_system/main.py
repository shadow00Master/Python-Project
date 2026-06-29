"""
main.py
Command-line interface for the Library Management System.
Run: python main.py
"""

from library import Library


def print_menu():
    print("""
==== LIBRARY MANAGEMENT SYSTEM ====
1. Add Book
2. Add Magazine
3. Add Member
4. Borrow Item
5. Return Item
6. List Available Items
7. List Overdue Items
8. List All Members
9. Save & Exit
""")


def main():
    library = Library()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                item_id = input("Item ID: ")
                title = input("Title: ")
                author = input("Author: ")
                genre = input("Genre: ")
                library.add_book(item_id, title, author, genre)
                print("Book added.")

            elif choice == "2":
                item_id = input("Item ID: ")
                title = input("Title: ")
                author = input("Author: ")
                issue = input("Issue number: ")
                library.add_magazine(item_id, title, author, issue)
                print("Magazine added.")

            elif choice == "3":
                member_id = input("Member ID: ")
                name = input("Name: ")
                library.add_member(member_id, name)
                print("Member added.")

            elif choice == "4":
                member_id = input("Member ID: ")
                item_id = input("Item ID: ")
                due = library.borrow_item(member_id, item_id)
                print(f"Borrowed. Due back: {due.strftime('%Y-%m-%d')}")

            elif choice == "5":
                member_id = input("Member ID: ")
                item_id = input("Item ID: ")
                library.return_item(member_id, item_id)
                print("Returned. Thanks!")

            elif choice == "6":
                items = library.list_available()
                if not items:
                    print("No items available right now.")
                for item in items:
                    print(item)

            elif choice == "7":
                overdue = library.list_overdue()
                if not overdue:
                    print("No overdue items.")
                for item in overdue:
                    print(item)

            elif choice == "8":
                if not library.members:
                    print("No members yet.")
                for member in library.members.values():
                    print(member)

            elif choice == "9":
                library.save()
                print("Data saved. Goodbye!")
                break

            else:
                print("Invalid option, try again.")

        except (KeyError, ValueError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
