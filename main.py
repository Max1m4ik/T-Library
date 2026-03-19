from db import init_db
from library import *
from models import Book
import traceback
from datetime import datetime


def pause():
    input("\nНажмите Enter, чтобы продолжить...")


def safe_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Ошибка: введите число")


def safe_year_input(prompt):
    current_year = datetime.now().year

    while True:
        try:
            year = int(input(prompt))
            if 0 <= year <= current_year:
                return year
            else:
                print(f"❌ Год должен быть от 0 до {current_year}")
        except ValueError:
            print("❌ Ошибка: введите число")


def safe_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ Поле не может быть пустым")


def print_books(books):
    if not books:
        print("📭 Ничего не найдено")
        return

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
6. Избранное (вкл/выкл)
7. Только прочитанные
8. Только избранные
9. Сортировка
0. Выход
""")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                title = safe_input("Название: ")
                author = safe_input("Автор: ")
                genre = safe_input("Жанр: ")
                year = safe_year_input("Год: ")
                description = safe_input("Описание: ")

                book = Book(title, author, genre, year, description)
                add_book(book)

                print("✅ Книга добавлена")
                pause()

            elif choice == "2":
                books = get_all_books()
                print_books(books)
                pause()

            elif choice == "3":
                field_map = {
                    "1": "all",
                    "2": "title",
                    "3": "author",
                    "4": "description"
                }

                print("""
Выберите где будете искать:
1. Везде
2. По названию
3. По автору
4. По описанию
""")

                search_choice = input("Выбор: ")
                keyword = safe_input("Введите слово для поиска: ")

                books = search_books(
                    keyword, field_map.get(search_choice, "all"))
                print_books(books)
                pause()

            elif choice == "4":
                books = get_all_books()

                if not books:
                    print("📭 Нет книг для удаления")
                    pause()
                    continue

                print("Список книг:")
                for b in books:
                    print(f"ID: {b[0]} | {b[1]}")

                book_id = safe_int_input("Введите ID книги для удаления: ")

                if not any(b[0] == book_id for b in books):
                    print("❌ Книга с таким ID не найдена")
                    pause()
                    continue

                delete_book(book_id)

                print("🗑 Книга удалена")
                pause()

            elif choice == "5":
                book_id = safe_int_input("ID книги: ")
                mark_as_read(book_id, 1)

                print("📖 Отмечено как прочитанное")
                pause()

            elif choice == "6":
                book_id = safe_int_input("ID книги: ")
                toggle_favorite(book_id)

                print("⭐ Обновлено избранное")
                pause()

            elif choice == "7":
                print_books(get_read_books())
                pause()

            elif choice == "8":
                print_books(get_favorite_books())
                pause()

            elif choice == "9":
                print("""
1. Название (А → Я)
2. Название (Я → А)
3. Автор (А → Я)
4. Год (старые → новые)
5. Год (новые → старые)
""")

                option = input("Выберите вариант: ")

                if option == "1":
                    books = get_books_sorted("title", descending=False)

                elif option == "2":
                    books = get_books_sorted("title", descending=True)

                elif option == "3":
                    books = get_books_sorted("author", descending=False)

                elif option == "4":
                    books = get_books_sorted("year", descending=False)

                elif option == "5":
                    books = get_books_sorted("year", descending=True)

                else:
                    print("❌ Неверный выбор")
                    pause()
                    continue

                print_books(books)
                pause()

            elif choice == "0":
                break

            else:
                print("❌ Неверный выбор")
                pause()

        except Exception:
            print("❌ Произошла непредвиденная ошибка")

            with open("error.log", "a", encoding="utf-8") as f:
                f.write("\n--- Ошибка ---\n")
                f.write(f"Дата: {datetime.now()}\n")
                f.write(traceback.format_exc())

            pause()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("💥 Критическая ошибка приложения")

        with open("error.log", "a", encoding="utf-8") as f:
            f.write("\n=== КРИТИЧЕСКАЯ ОШИБКА ===\n")
            f.write(traceback.format_exc())
