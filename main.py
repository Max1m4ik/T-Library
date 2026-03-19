from db import init_db
from library import *
from models import Book
import traceback
from datetime import datetime
import os
from colorama import init, Fore, Style


init(autoreset=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input(Fore.CYAN + "\nНажмите Enter, чтобы продолжить...")


def safe_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(Fore.RED + "❌ Ошибка: введите число")


def safe_year_input(prompt):
    current_year = datetime.now().year
    while True:
        try:
            year = int(input(prompt))
            if 0 <= year <= current_year:
                return year
            else:
                print(Fore.RED + f"❌ Год должен быть от 0 до {current_year}")
        except ValueError:
            print(Fore.RED + "❌ Ошибка: введите число")


def safe_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(Fore.RED + "❌ Поле не может быть пустым")


def print_books(books):
    if not books:
        print(Fore.YELLOW + "📭 Ничего не найдено")
        return
    for b in books:
        read_status = Fore.GREEN + "Да" if b[6] else Fore.RED + "Нет"
        fav_status = Fore.YELLOW + "Да" if b[7] else Fore.RED + "Нет"
        print(Fore.BLUE + "-" * 40)
        print(Fore.CYAN + f"ID: {b[0]} | Название: {b[1]}")
        print(Fore.CYAN + f"Автор: {b[2]} | Жанр: {b[3]} | Год: {b[4]}")
        print(Fore.CYAN + f"Описание: {b[5]}")
        print(Fore.CYAN +
              f"Прочитана: {read_status} | Избранное: {fav_status}")
    print(Fore.BLUE + "-" * 40)


def main():
    init_db()
    while True:
        clear_screen()
        print(Fore.MAGENTA + Style.BRIGHT + "=" * 50)
        print(Fore.YELLOW + Style.BRIGHT + "                   T-Библиотека")
        print(Fore.MAGENTA + Style.BRIGHT + "=" * 50)
        print(Fore.CYAN + """
1. Добавить книгу
2. Показать все книги
3. Поиск
4. Удалить книгу
5. Отметить/снять прочитанное
6. Избранное (вкл/выкл)
7. Только избранные
8. Сортировка
0. Выход
""")

        choice = input(Fore.BLUE + "Выберите действие: ")

        try:
            if choice == "1":
                clear_screen()
                print(Fore.YELLOW + "📚 Добавление новой книги\n")
                title = safe_input("Название: ")
                author = safe_input("Автор: ")
                genre = safe_input("Жанр: ")
                year = safe_year_input("Год: ")
                description = safe_input("Описание: ")

                book = Book(title, author, genre, year, description)
                add_book(book)

                print(Fore.GREEN + "✅ Книга добавлена")
                pause()

            elif choice == "2":
                clear_screen()
                print(Fore.YELLOW + "📖 Список всех книг\n")
                books = get_all_books()
                print_books(books)
                pause()

            elif choice == "3":
                clear_screen()
                field_map = {"1": "all", "2": "title",
                             "3": "author", "4": "description"}
                print(Fore.YELLOW + "🔍 Поиск книги\n")
                print(
                    "Где искать:\n1. Везде\n2. По названию\n3. По автору\n4. По описанию\n")
                search_choice = input(Fore.BLUE + "Выбор: ")
                keyword = safe_input("Введите слово для поиска: ")
                books = search_books(
                    keyword, field_map.get(search_choice, "all"))
                print_books(books)
                pause()

            elif choice == "4":
                clear_screen()
                print(Fore.YELLOW + "🗑 Удаление книги\n")
                books = get_all_books()
                if not books:
                    print(Fore.RED + "📭 Нет книг для удаления")
                    pause()
                    continue
                print("Список книг:")
                for b in books:
                    print(Fore.CYAN + f"ID: {b[0]} | {b[1]}")
                book_id = safe_int_input("Введите ID книги для удаления: ")
                if not any(b[0] == book_id for b in books):
                    print(Fore.RED + "❌ Книга с таким ID не найдена")
                    pause()
                    continue
                delete_book(book_id)
                print(Fore.GREEN + "🗑 Книга удалена")
                pause()

            elif choice == "5":
                clear_screen()
                print(Fore.YELLOW + "📖 Отметить/снять прочитанное\n")
                books = get_all_books()
                for b in books:
                    status = "Прочитано" if b[6] else "Не прочитано"
                    print(Fore.CYAN + f"ID: {b[0]} | {b[1]} | {status}")
                book_id = safe_int_input("Введите ID книги: ")
                book = next((b for b in books if b[0] == book_id), None)
                if not book:
                    print(Fore.RED + "❌ Книга с таким ID не найдена")
                    pause()
                    continue
                # Переключаем статус прочитанности
                mark_as_read(book_id, 0 if book[6] else 1)
                print(
                    Fore.GREEN + f"✅ Статус прочитанного обновлён: {'Прочитано' if not book[6] else 'Не прочитано'}")
                pause()

            elif choice == "6":
                clear_screen()
                print(Fore.YELLOW + "⭐ Изменение статуса избранного\n")
                books = get_all_books()
                for b in books:
                    status = "В избранном" if b[7] else "Не в избранном"
                    print(Fore.CYAN + f"ID: {b[0]} | {b[1]} | {status}")
                book_id = safe_int_input("Введите ID книги: ")
                if not any(b[0] == book_id for b in books):
                    print(Fore.RED + "❌ Книга с таким ID не найдена")
                    pause()
                    continue
                toggle_favorite(book_id)
                print(Fore.GREEN + "✅ Статус избранного обновлён")
                pause()

            elif choice == "7":
                clear_screen()
                print(Fore.YELLOW + "⭐ Только избранные книги\n")
                print_books(get_favorite_books())
                pause()

            elif choice == "8":
                clear_screen()
                print(Fore.YELLOW + "📊 Сортировка и фильтры\n")
                print("Выберите фильтры и сортировку (через запятую, напр. 1,6,4):")
                print(
                    "1. Название (А → Я)\n2. Название (Я → А)\n3. Автор (А → Я)\n4. Год (старые → новые)")
                print(
                    "5. Год (новые → старые)\n6. Только прочитанные\n7. Только непрочитанные\n")
                options = input(Fore.BLUE + "Ваш выбор: ").split(",")
                sort_order = []
                filter_read = None
                for o in options:
                    o = o.strip()
                    if o == "1":
                        sort_order.append(("title", False))
                    elif o == "2":
                        sort_order.append(("title", True))
                    elif o == "3":
                        sort_order.append(("author", False))
                    elif o == "4":
                        sort_order.append(("year", False))
                    elif o == "5":
                        sort_order.append(("year", True))
                    elif o == "6":
                        filter_read = True
                    elif o == "7":
                        filter_read = False
                # Фильтр по прочитанности
                if filter_read is True:
                    books = get_read_books()
                elif filter_read is False:
                    books = [b for b in get_all_books() if not b[6]]
                else:
                    books = get_all_books()
                # Применяем сортировку
                for col, desc in reversed(sort_order):
                    books = sorted(books, key=lambda b: b[{
                                   "title": 1, "author": 2, "year": 4}[col]], reverse=desc)
                print_books(books)
                pause()

            elif choice == "0":
                clear_screen()
                print(Fore.MAGENTA + "👋 Выход из программы. До встречи!")
                break

            else:
                print(Fore.RED + "❌ Неверный выбор")
                pause()

        except Exception:
            print(Fore.RED + "❌ Произошла непредвиденная ошибка")
            with open("error.log", "a", encoding="utf-8") as f:
                f.write("\n--- Ошибка ---\n")
                f.write(f"Дата: {datetime.now()}\n")
                f.write(traceback.format_exc())
            pause()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(Fore.RED + "💥 Критическая ошибка приложения")
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("\n=== КРИТИЧЕСКАЯ ОШИБКА ===\n")
            f.write(traceback.format_exc())
