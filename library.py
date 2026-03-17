from db import get_connection


def add_book(book):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO books (title, author, genre, year, description, is_read, is_favorite)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (book.title, book.author, book.genre, book.year, book.description, book.is_read, book.is_favorite))

    conn.commit()
    conn.close()


def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()
    return books


def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()


def mark_as_read(book_id, is_read):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE books SET is_read = ? WHERE id = ?",
                   (is_read, book_id))
    conn.commit()
    conn.close()


def toggle_favorite(book_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE books 
    SET is_favorite = NOT is_favorite 
    WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()


def search_books(keyword, field="all"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    all_books = cursor.fetchall()

    conn.close()

    keyword = keyword.lower()
    result = []

    for book in all_books:
        title = book[1].lower()
        author = book[2].lower()
        description = book[5].lower()

        if field == "title" and keyword in title:
            result.append(book)

        elif field == "author" and keyword in author:
            result.append(book)

        elif field == "description" and keyword in description:
            result.append(book)

        elif field == "all":
            if (keyword in title or
                keyword in author or
                    keyword in description):
                result.append(book)

    return result


def get_books_sorted(sort_by="title"):
    conn = get_connection()
    cursor = conn.cursor()

    if sort_by not in ["title", "author", "year"]:
        sort_by = "title"

    cursor.execute(f"SELECT * FROM books ORDER BY {sort_by}")
    books = cursor.fetchall()

    conn.close()
    return books


def get_read_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE is_read = 1")
    books = cursor.fetchall()

    conn.close()
    return books


def get_favorite_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE is_favorite = 1")
    books = cursor.fetchall()

    conn.close()
    return books
