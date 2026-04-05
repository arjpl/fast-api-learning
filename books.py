from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {
        "id": 1,
        "title": "The Song of Achilles",
        "author": "Madeleine Miller",
        "category": "Fiction"
    },
    {
        "id": 2,
        "title": "Algorithms",
        "author": "Jeff Erickson",
        "category": "Computer Science"
    },
    {
        "id": 3,
        "title": "Neural Networks & Deep Learning",
        "author": "Michael Nielsen",
        "category": "Computer Science"
    },
    {
        "id": 4,
        "title": "The Handmaid's Tale",
        "author": "Margaret Atwood",
        "category": "Fiction"
    }
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{id}")
async def read_book(id: int):    
    book = [b for b in BOOKS if b.get("id",0) == id]
    return book
        
@app.get("/books/")
async def get_category(category: str):
    response = []
    for book in BOOKS:
        if book.get("category", "").lower() == category.lower():
            response.append(book)
    return response