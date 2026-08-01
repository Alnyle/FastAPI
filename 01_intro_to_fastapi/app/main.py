from fastapi import FastAPI, Body


app = FastAPI()

# always put your static or smaller api first because fastapi looks
# in a chronological order for api endpoint from top to bottom
# to see what matches the URL that's coming in

BOOKS = [
    {"id": 1, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Paulo Coelho", "category": "Classic"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Paulo Coelho", "category": "Romance"},
    {"id": 5, "title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy"},
    {"id": 6, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Literary Fiction"},
    {"id": 7, "title": "Brave New World", "author": "Aldous Huxley", "category": "Dystopian"},
    {"id": 8, "title": "Moby Dick", "author": "Paulo Coelho", "category": "Classic"},
    {"id": 9, "title": "The Alchemist", "author": "Paulo Coelho", "category": "Philosophical Fiction"},
    {"id": 10, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "category": "Fantasy"},
    {"id": 11, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "category": "Fantasy"},
]


@app.get('/books')
async def get_all_books():
    return BOOKS


@app.get('/books/{book_id}')
async def get_book(book_id: int):
    
    for book in BOOKS:
        if book_id == book.get("id"):
            return {"book": book}
            
            
    return {"message": f"Book {book_id} not found"}


# casefold(): Return a version of the string suitable for caseless comparisons.
# query parameters are parameters are attach after "?" for example:
# http://127.0.0.1:8000/books/?category=Fantasy
@app.get('/books/')
async def get_category_by_query(category: str):
    result = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            result.append(book)
    
    if result:
        return {"results": result}
    else: 
        return {"message": f"There is no category called {category}"}

# we can also use path parameters and query parameters togther
@app.get('/books/{author_name}/')
async def get_book_by_author_and_category(author: str, category: str):
    
    result = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            if book.get("category").casefold() == category.casefold():
                result.append(book)
    
    if result:
        return {"results": result}
    else: 
        return {"message": f"There is no author called {author}"}

# post request: used when you want to insert a new record in the database 
# post request: where data send it in request body instead of url 
@app.post('/books/create_book')
async def create_book(new_book=Body()):
    
    BOOKS.append(new_book)
    
    
# put request: typically used to update data that already exist in the database (like updating a user’s info).
# put request: also has body where data send it in request body
@app.put('/books/{book_id}')
async def update_book_info(book_id: int, new_update=Body()):
    
    bk = None
    for book in BOOKS:
        if book_id == book.get("id"):
            book = new_update
            return {"updated book": book}
            
    return {"message": f"Book with id {book_id} not found"}


# delete request: is used to delete to resource in the database 
# In FastAPI, a DELETE request is used to remove a resource from the server (like deleting a user or a product).
@app.delete('/books/{book_id}')
async def delete_book(book_id: int):
    
    index = None
    for i in range(len(BOOKS)):
        if book_id == BOOKS[i].get("id"):
            index = i
            break
    
    if index:
        BOOKS.pop(index)
        return {"message": f"Book {book_id} deleted successfully"}
    else:
        return {"message": f"cloud not delete Book with id {book_id} not found"}
