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


def search_books(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    all_books = cursor.fetchall()

    conn.close()

    keyword = keyword.lower()
    result = []

    for book in all_books:
        if (keyword in book[1].lower() or
            keyword in book[2].lower() or
            keyword in book[3].lower() or
                keyword in book[5].lower()):
            result.append(book)

    return result
