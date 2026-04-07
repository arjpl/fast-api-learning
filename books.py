from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {
        "id": 1,
        "title": "The Song of Achilles",
        "author": "Madeleine Miller",
        "category": "Fiction",
        "year": "2012",
    },
    {
        "id": 2,
        "title": "Algorithms",
        "author": "Jeff Erickson",
        "category": "Computer Science",
        "year": "1998",
    },
    {
        "id": 3,
        "title": "Neural Networks & Deep Learning",
        "author": "Michael Nielsen",
        "category": "Computer Science",
        "year": "2015",

    },
    {
        "id": 4,
        "title": "The Handmaid's Tale",
        "author": "Margaret Atwood",
        "category": "Fiction",
        "year": "1980",

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

@app.get("/books/{year}/")
async def read_books_by_year_and_category(year: str, category: str):
    """
    Find books published in a given `year`,
    and query for a certain `category` for this `year`.
    """
    year_books = [
                    b for b in BOOKS
                        if (b.get("year","")==year
                            and b.get("category","").lower()==category.lower())
                  ]
    return year_books

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
        
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == updated_book.get("id"):
            BOOKS[i] = updated_book
            
@app.delete("/books/delete_book/{id}")
async def delete_book(id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == id:
            BOOKS.pop(i)
            break