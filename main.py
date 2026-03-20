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


def safe_int_input(prompt, allow_empty=False):
    while True:
        val = input(prompt).strip()
        if allow_empty and val == "":
            return None
        try:
            return int(val)
        except ValueError:
            print(Fore.RED + "❌ Ошибка: введите число")


def safe_year_input(prompt, allow_empty=False):
    current_year = datetime.now().year
    while True:
        val = input(prompt).strip()
        if allow_empty and val == "":
            return None
        if val == "-":
            return ""
        try:
            year = int(val)
            if 0 <= year <= current_year:
                return year
            else:
                print(Fore.RED + f"❌ Год должен быть от 0 до {current_year}")
        except ValueError:
            print(Fore.RED + "❌ Ошибка: введите число")


def safe_input(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            if value == "-":
                return ""
            return value
        print(Fore.RED + "❌ Поле не может быть пустым")


def print_books(books):
    if not books:
        print(Fore.YELLOW + "📭 Ничего не найдено")
        return

    for b in books:
        read_status = "✅" if b[6] else "❌"
        fav_status = "⭐" if b[7] else "❌"

        print(Fore.BLUE + "─" * 50)

        # Название — главный акцент
        print(Fore.YELLOW + Style.BRIGHT + f"📖 {b[1]}")

        # Остальная инфа — аккуратно и читаемо
        print(Fore.CYAN + f"ID: {b[0]}")
        print(Fore.WHITE + f"Автор: {b[2]}")
        print(Fore.WHITE + f"Жанр: {b[3]} | Год: {b[4]}")

        # Описание чуть приглушённое
        print(Fore.LIGHTBLACK_EX + f"Описание: {b[5]}")

        # Статусы с цветом
        print(
            (Fore.GREEN if b[6] else Fore.RED) + f"Прочитана: {read_status}  " +
            (Fore.YELLOW if b[7] else Fore.RED) + f"| Избранное: {fav_status}"
        )

    print(Fore.BLUE + "─" * 50)


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
3. Поиск книги
4. Удалить книгу
5. Добавить/убрать метку "прочитанное"
6. Избранное (вкл/выкл)
7. Только избранные
8. Сортировка и фильтры
9. GitHub — инструкция по использованию
0. Выход
""")

        choice = input(Fore.GREEN + Style.BRIGHT +
                       "Выберите действие: ").strip()

        try:
            if choice == "1":
                clear_screen()
                print(Fore.YELLOW + "📚 Добавление новой книги")
                print("(введите '-' чтобы оставить пустым, Enter - выйти в меню)")
                title = safe_input(
                    "Название : ", allow_empty=True)
                if title == "":
                    main()
                author = safe_input(
                    "Автор : ", allow_empty=True)
                genre = safe_input(
                    "Жанр : ", allow_empty=True)
                year = safe_year_input(
                    "Год : ", allow_empty=True)
                description = safe_input(
                    "Описание : ", allow_empty=True)

                book = Book(title, author, genre, year, description)
                add_book(book)

                print(Fore.GREEN + "✅ Книга добавлена")
                pause()

            elif choice == "2":
                clear_screen()
                print(Fore.YELLOW + "📖 Список всех книг")
                books = get_all_books()
                print_books(books)
                pause()

            elif choice == "3":
                clear_screen()
                field_map = {"1": "all", "2": "title",
                             "3": "author", "4": "description"}
                print(Fore.YELLOW + "🔍 Поиск книги")
                print(
                    "Где искать:\n1. Везде\n2. По названию\n3. По автору\n4. По описанию\n")
                search_choice = input(Fore.BLUE + "Выбор: ").strip()
                keyword = safe_input(
                    "Введите слово для поиска (Enter чтобы выйти): ", allow_empty=True)
                if keyword == "":
                    continue
                books = search_books(
                    keyword, field_map.get(search_choice, "all"))
                print_books(books)
                pause()

            elif choice == "4":
                clear_screen()
                print(Fore.YELLOW + "🗑 Удаление книги")
                books = get_all_books()
                if not books:
                    print(Fore.RED + "📭 Нет книг для удаления")
                    pause()
                    continue
                for b in books:
                    print(Fore.BLUE + f"ID: {b[0]} | {b[1]}")
                val = input(
                    "Введите ID книги для удаления (через запятую (без пробелов!), Enter — выход): ").strip()
                if not val:
                    continue
                try:
                    ids = [int(x.strip()) for x in val.split(",")]
                except ValueError:
                    print(Fore.RED + "❌ Некорректный ввод")
                    pause()
                    continue
                for book_id in ids:
                    if not any(b[0] == book_id for b in books):
                        print(Fore.RED + f"❌ Книга с ID {book_id} не найдена")
                        continue
                    delete_book(book_id)
                    print(Fore.GREEN + f"🗑 Книга ID {book_id} удалена")
                pause()

            elif choice == "5":
                clear_screen()
                print(Fore.YELLOW + "📖 Отметить/снять прочитанное")
                books = get_all_books()
                for b in books:
                    status = "Прочитано" if b[6] else "Не прочитано"
                    print(Fore.BLUE + f"ID: {b[0]} | {b[1]} | {status}")
                val = input(
                    "Введите ID книги (через запятую (без пробелов!), Enter — выход): ").strip()
                if not val:
                    continue
                try:
                    ids = [int(x.strip()) for x in val.split(",")]
                except ValueError:
                    print(Fore.RED + "❌ Некорректный ввод")
                    pause()
                    continue
                for book_id in ids:
                    book = next((b for b in books if b[0] == book_id), None)
                    if not book:
                        print(Fore.RED + f"❌ Книга с ID {book_id} не найдена")
                        continue
                    mark_as_read(book_id, 0 if book[6] else 1)
                    print(
                        Fore.GREEN + f"✅ ID {book_id} обновлён: {'Прочитано' if not book[6] else 'Не прочитано'}")
                pause()

            elif choice == "6":
                clear_screen()
                print(Fore.YELLOW + "⭐ Изменение статуса избранного")
                books = get_all_books()
                for b in books:
                    status = "В избранном" if b[7] else "Не в избранном"
                    print(Fore.BLUE + f"ID: {b[0]} | {b[1]} | {status}")
                val = input(
                    "Введите ID книги (через запятую (без пробелов!), Enter — выход): ").strip()
                if not val:
                    continue
                try:
                    ids = [int(x.strip()) for x in val.split(",")]
                except ValueError:
                    print(Fore.RED + "❌ Некорректный ввод")
                    pause()
                    continue
                for book_id in ids:
                    if not any(b[0] == book_id for b in books):
                        print(Fore.RED + f"❌ Книга с ID {book_id} не найдена")
                        continue
                    toggle_favorite(book_id)
                    print(Fore.GREEN +
                          f"✅ Статус избранного обновлён для ID {book_id}")
                pause()

            elif choice == "7":
                clear_screen()
                print(Fore.YELLOW + "⭐ Только избранные книги")
                print_books(get_favorite_books())
                pause()

            elif choice == "8":
                clear_screen()
                print(Fore.YELLOW + "📊 Сортировка и фильтры")
                pause()

            elif choice == "9":
                clear_screen()
                print(
                    Fore.BLUE + "🌐 GitHub проекта: https://github.com/Max1m4ik/T-Library")
                pause()

            elif choice == "0":
                clear_screen()
                print(Fore.MAGENTA + "👋 Выход из программы. До встречи!")
                break

            else:
                print(Fore.RED + "❌ Неверный выбор")
                pause()

        except Exception:
            print(
                Fore.RED + "❌ Произошла непредвиденная ошибка, подробнее в файле error.log")
            with open("error.log", "a", encoding="utf-8") as f:
                f.write("\n--- Ошибка ---\n")
                f.write(f"Дата: {datetime.now()}\n")
                f.write(traceback.format_exc())
            pause()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(Fore.RED + "💥 Критическая ошибка приложения, подробнее в файле error.log")
        with open("error.log", "a", encoding="utf-8") as f:
            f.write("\n=== КРИТИЧЕСКАЯ ОШИБКА ===\n")
            f.write(traceback.format_exc())
