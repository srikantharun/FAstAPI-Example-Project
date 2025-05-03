from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Basic FastAPI Example",
    description="A simple REST API with in-memory storage",
    version="1.0.0"
)

# Data model
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

# In-memory database
db = []
counter = 0

# Routes
@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Welcome to the Basic FastAPI Example!"}

@app.get("/items", response_model=List[Item])
def read_items():
    """Get all items."""
    return db

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    """Get a specific item by ID."""
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    """Create a new item."""
    global counter
    counter += 1
    item.id = counter
    db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    """Update an existing item."""
    for i, item in enumerate(db):
        if item.id == item_id:
            updated_item.id = item_id
            db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item."""
    for i, item in enumerate(db):
        if item.id == item_id:
            db.pop(i)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)