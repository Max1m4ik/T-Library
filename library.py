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

    query = f"%{keyword}%"
    cursor.execute("""
    SELECT * FROM books
    WHERE title LIKE ? OR author LIKE ? OR description LIKE ?
    """, (query, query, query))

    result = cursor.fetchall()
    conn.close()
    return result
