from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int
        
    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year
        
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed for `create-book`", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=500)
    rating: int = Field(ge=1, le=5)
    published_year: int = Field(ge=0, le=2027)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My Book",
                "author": "Myself",
                "description": "Description of my book",
                "rating": 5,
                "published_year": 2025,
            }
        }
    }
    

BOOKS = [
    Book(1, "The Art of Computer Programming", "Donald Knuth", "The book under consideration here is a classic, but no ordinary one. An ordinary classic is a work that never gets stale. This extraordinary classic is one that is never even finished! First published in 1962 in a single volume consisting of twelve chapters, the book has gradually but continuously expanded over the intervening 60 years.", 5, 2022),
    Book(2, "Introduction to Algorithms", "Thomas H. Cormen , Charles E. Leiserson , Ron Rivest , and Clifford Stein", "Introduction to Algorithms is just what its title says: an introductory textbook to algorithms used in computer science.", 4, 1980),
    Book(3, "Things a Computer Scientist Rarely Talks About", "Donald Knuth", "With this book, Knuth has given us the benefit of his unparalleled experience and wisdom concerning the connection between computer technology and religion.", 5, 1967),
    Book(4, "Wuthering Heights", "Emily Bronte", "A dark and passionate story about the intense love between Heathcliff and Catherine Earnshaw and its destructive effects on those around them.", 4, 1880),
    Book(5, "War and Peace", "Leo Tolstoy", "A sprawling epic set against the backdrop of the Napoleonic Wars, following the lives of aristocratic families and exploring themes of love, fate, and the futility of war.", 3, 1890),
    Book(6, "Anna Karenina", "Leo Tolstoy", "This novel tells the tragic love story of Anna, a married woman, and her affair with the charming Count Vronsky, set against a rich portrayal of Russian society.", 5, 1803),
    Book(7, "Les Misérables", "Victor Hugo", "This monumental novel weaves together the stories of several characters, most notably ex-convict Jean Valjean, exploring themes of justice, love, and redemption in post-revolutionary France.", 4, 1932),
    Book(8, "Things Fall Apart", "Chinua Achebe", "This novel follows the life of Okonkwo, a respected leader in an Igbo village in Nigeria, as European colonization disrupts the traditional way of life, leading to tragedy.", 5, 1923),
    Book(9, "The Hobbit", "J. R. R. Tolkien", "Bilbo Baggins, a hobbit, embarks on an unexpected adventure with a group of dwarves to reclaim their homeland from the dragon Smaug, discovering courage and friendship along the way.", 4, 1962),
    Book(10, "The Lord of the Rings", "J. R. R. Tolkien", "A high-fantasy epic that follows the journey of hobbit Frodo Baggins and his companions as they attempt to destroy a powerful ring that could bring about the downfall of Middle-earth.", 5, 1982),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    
def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

@app.get("/books/id/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    response = []
    for book in BOOKS:
        if book.rating == book_rating:
            response.append(book)
    return response

@app.put("/books/update")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if book.id == BOOKS[i].id:
            BOOKS[i] = book
            
@app.delete("/books/id/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
        
@app.get("/books/published_year")
async def filter_by_published_year(year: int):
    response = []
    for book in BOOKS:
        if book.published_year == year:
            response.append(book)
    return response
        
    