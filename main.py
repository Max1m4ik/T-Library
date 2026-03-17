from db import init_db
from library import *
from models import Book


def print_books(books):
    for b in books:
        print(f"""
ID: {b[0]}
Название: {b[1]}
Автор: {b[2]}
Жанр: {b[3]}
Год: {b[4]}
Описание: {b[5]}
Прочитана: {'Да' if b[6] else 'Нет'}
Избранное: {'Да' if b[7] else 'Нет'}
------------------------
""")


def main():
    init_db()

    while True:
        print("""
1. Добавить книгу
2. Показать все книги
3. Поиск
4. Удалить книгу
5. Отметить как прочитанную
6. Добавить/убрать из избранного
0. Выход
""")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Название: ")
            author = input("Автор: ")
            genre = input("Жанр: ")
            year = int(input("Год: "))
            description = input("Описание: ")

            book = Book(title, author, genre, year, description)
            add_book(book)

        elif choice == "2":
            books = get_all_books()
            print_books(books)

        elif choice == "3":
            keyword = input("Введите ключевое слово: ")
            books = search_books(keyword)
            print_books(books)

        elif choice == "4":
            book_id = int(input("ID книги: "))
            delete_book(book_id)

        elif choice == "5":
            book_id = int(input("ID книги: "))
            mark_as_read(book_id, 1)

        elif choice == "6":
            book_id = int(input("ID книги: "))
            toggle_favorite(book_id)

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
