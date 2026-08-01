from fastapi import FastAPI, Body, Query, Path,HTTPException
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Annotated
from starlette import status
# - Pydantic is a Python library for data validation and settings management.
# - FastAPI uses Pydantic to handle request bodies, query parameters, and responses.
# - It makes sure the data your API receives (e.g., JSON from a client) matches the expected types and structure.

# BaseModel is the base class provided by Pydantic.
# You create your own data models by subclassing BaseModel.
# These models define the shape (schema) of your data.
 
# FastAPI then:
# 1. Validates incoming data automatically
# 2. Parses it into Python objects



app = FastAPI()


class Book():
    
    def __init__(self, id: int, title: str, author: str, description: str, rating: float):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating



class BookRequest(BaseModel):
    
    # id: int | None = None
    id: int | None = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=-1, le=5)
    
    
    # to change the default value for the generated scheme in swagger ui
    # we use
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codejson",
                "description": "A new book",
                "rating": 5,
            }
        }
    }
    

BOOKS = [
    Book(1, "To Kill a Mockingbird", "Harper Lee", 
         "A story of racial injustice and moral growth in the American South", 4.5),
    Book(2, "1984", "George Orwell", 
         "A dystopian novel about totalitarianism and surveillance", 4.7),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald", 
         "A portrait of the Jazz Age and the American Dream", 4.3),
    Book(4, "Pride and Prejudice", "Jane Austen", 
         "A romantic novel about the Bennet family in rural England", 4.8),
    Book(5, "The Hobbit", "J.R.R. Tolkien", 
         "A fantasy adventure about Bilbo Baggins' quest", 4.6)
]

# it saying after this function return it's output successful return with it status code 200 ok: successful request
@app.get('/', status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    
    new_book = Book(**book_request.model_dump()) # convert the request object to dictionary then pass the field as arguments
    BOOKS.append(new_book)
    

@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
    
    for book in BOOKS:
        if book.id == book_id:
            return {"book": book}
    
    raise HTTPException(status_code=404, detail="Item nof found")


@app.get('/books')
async def get_books_by_rating(rating: Annotated[float | None, Query(alias="rating-filter", description="filter books by rate")] = None):
    
    result = []    
    if rating:
        for book in BOOKS:
            if book.rating >= rating:
                result.append(book)
        return {"result": result}
    else:
        return {"books": BOOKS}
    

@app.put('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: int, updated_book: BookRequest):
    
    
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i] = updated_book
            return {"message": f"book {book_id} has been updated"}
    
    return {"message": f"book with id {book_id} not found"}
    
@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": f"book with id {book_id} has been deleted"}  
    
    return {"message": f"book with id {book_id} not found"}    

@dataclass
class Item:
        
    name: str
    price: float


ITEMS = {
    1: Item("Apple", 1.2),
    2: Item("Orange", 4),
    3: Item("Pineapple", 2.12),
    4: Item("Plum", 1.2),
    5: Item("grape", 2.2),
}

# q: is a query parameter which is a parameter came after '?'
# q: can be of type str or None and has default value is None
@app.get('/items/')
async def read_items(q: str | None = None):
    
    if q:
        return {
            "message": f"query = {q}",
            "items": ITEMS,
            }
    else:
        return {"items": ITEMS}


# put some validation on query parameter
# Annotated is from Python’s typing module.
#  - It allows you to add extra metadata to a type. In FastAPI, this metadata is usually validation or documentation rules.

# Query is a FastAPI helper for defining validation rules and documentation for query parameters.
# Keep in mind that when using `Query`` inside of `Annotated` you cannot use the default parameter for Query.


# async def items_query_rules(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
@app.get('/items_query_rules/')
async def items_query_rules(q: Annotated[str | None, Query(max_length=50)] = None):
    
    if q:
        return {
            "message": f"query = {q}",
            "items": ITEMS,
            }
    else:
        return {"items": ITEMS}
    
    
# regular expression 
@app.get('/items_with_regx')
async def items_with_regx(
    q: Annotated[str | None, Query(min_length=3, max_length=50, pattern=r"\b(price|name)\b")] = None
    ):
    
    if q:
        return {
            "message": f"query = {q}",
            "items": ITEMS,
            }
    else:
        return {"items": ITEMS}
    


# Query parameter list / multiple values
@app.get('/items_query_list/')
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    
    if q:
        return {
            "message": f"query = {q}",
            "items": ITEMS,
            }
    else:
        return {"items": ITEMS}


# Declare more metadata: You can add more information about the parameter.
# you can title and description 
@app.get('/items_query_more_metadata/')
async def read_items(
    q: Annotated[
        str | None, 
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
        ),
        ] = None):
    
    if q:
        return {
            "message": f"query = {q}",
            "items": ITEMS,
            }
    else:
        return {"items": ITEMS}
