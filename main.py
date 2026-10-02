from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="FastAPI CRUD Tutorial")

# 1. Define the Schema for an Item
class Item(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# 2. In-Memory "Database" (simple Python list to store items)
db_items: list[Item] = []
print(f"db_items initialized : {db_items}")


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI CRUD Tutorial!"}

# 3. Create a new item (POST)
@app.post("/items/", status_code=status.HTTP_201_CREATED, response_model=Item)
def create_item(item: Item):
    # Check if an item with this ID already exists
    for existing_item in db_items:
        if existing_item.id == item.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item with id {item.id} already exists"
            )
    
    # Add to our list
    db_items.append(item)
    return item

# # 4. Read all items (GET)
# @app.get("/items/", response_model=list[Item])
# def get_all_items():
#     return db_items

# 4. Read all items with Query Parameters (Filtering & Pagination)
@app.get("/items/", response_model=list[Item])
def get_all_items(
    search: Optional[str] = None,
    is_available: Optional[bool] = None,
    limit: int = 10
):
    results = db_items

    # 1. Filter by keyword in title if provided
    if search:
        results = [item for item in results if search.lower() in item.title.lower()]

    # 2. Filter by availability if provided
    if is_available is not None:
        results = [item for item in results if item.is_available == is_available]

    # 3. Limit the maximum items returned
    return results[:limit]



# 5. Read single item by dynamic URL / path parameter (GET)
@app.get("/items/{item_id}", response_model=Item)
def get_item_by_id(item_id: int):
    for item in db_items:
        if item.id == item_id:
            return item
    
    # If item not found, return 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )


# 6. Update an existing item (PUT)
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db_items):
        if item.id == item_id:
            # Ensure the ID matches the path parameter and update
            updated_item.id = item_id
            db_items[index] = updated_item
            return updated_item
            
    # If not found, return 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

# 7. Delete an item (DELETE)
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(db_items):
        if item.id == item_id:
            deleted_item = db_items.pop(index)
            return {"message": f"Item '{deleted_item.title}' (id: {item_id}) deleted successfully"}
            
    # If not found, raise 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

