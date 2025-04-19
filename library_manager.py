import json
import os

# File to save and load library data
LIBRARY_FILE = "library.txt"

# Load library data from file if it exists
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library data to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Display the menu options
def display_menu():
    print("\n--- Personal Library Manager ---")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")

# Add a book to the library
def add_book(library):
    title = input("Enter book title: ")
    author = input("Enter author: ")
    year = int(input("Enter publication year: "))
    genre = input("Enter genre: ")
    read_status = input("Have you read this book? (y/n): ").lower() == 'y'
    
    book = {
        "title": title,
        "author": author ,
        "year": year,
        "genre": genre,
        "read": read_status
    }
    library.append(book)
    print("Book added successfully.")

# Remove a book by title
def remove_book(library):
    title = input("Enter the title of the book to remove: ")
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            print("Book removed.")
            return
    print("Book not found.")

# Search for a book by title or author
def search_books(library):
    keyword = input("Enter title or author to search: ").lower()
    matches = [book for book in library if keyword in book["title"].lower() or keyword in book["author"].lower()]
    
    if matches:
        for book in matches:
            display_book(book)
    else:
        print("No matching books found.")

# Display a single book in a formatted way
def display_book(book):
    status = "Read" if book["read"] else "Unread"
    print(f"\nTitle: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Year: {book['year']}")
    print(f"Genre: {book['genre']}")
    print(f"Status: {status}")

# Display all books in the library
def display_all_books(library):
    if not library:
        print("Library is empty.")
        return
    for book in library:
        display_book(book)

# Display statistics about the library
def display_statistics(library):
    total = len(library)
    if total == 0:
        print("Library is empty.")
        return
    read_count = sum(1 for book in library if book["read"])
    percent_read = (read_count / total) * 100
    print(f"Total books: {total}")
    print(f"Books read: {read_count} ({percent_read:.2f}%)")

# Main function to run the program
def main():
    library = load_library()

    while True:
        display_menu()
        choice = input("Choose an option (1-6): ")

        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_books(library)
        elif choice == '4':
            display_all_books(library)
        elif choice == '5':
            display_statistics(library)
        elif choice == '6':
            save_library(library)
            print("Library saved. Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point
if __name__ == "__main__":
   main()
