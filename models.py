class Book:
    def __init__(self, title, author, genre, year, description, is_read=0, is_favorite=0):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.description = description
        self.is_read = is_read
        self.is_favorite = is_favorite
