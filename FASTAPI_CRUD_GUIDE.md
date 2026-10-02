# FastAPI CRUD Step-by-Step Learning Guide

A beginner-friendly, step-by-step tutorial for building a RESTful CRUD API using FastAPI and Python.

---

## 📌 What is CRUD?

CRUD corresponds to the 4 fundamental database operations mapped to HTTP methods:

| Operation | Action | HTTP Method | Example Route |
|---|---|---|---|
| **C**reate | Add new item | `POST` | `/items/` |
| **R**ead | Get item(s) | `GET` | `/items/` or `/items/{id}` |
| **U**pdate | Edit an existing item | `PUT` / `PATCH` | `/items/{id}` |
| **D**elete | Remove an item | `DELETE` | `/items/{id}` |

---

## 🛠️ Step 1: Environment & Installation

### 1. Create a Virtual Environment
```powershell
python -m venv venv
```

### 2. Activate the Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```powershell
pip install fastapi uvicorn
```

* **FastAPI**: The web framework for building APIs.
* **Uvicorn**: Lightning-fast ASGI server that runs your FastAPI app.

## 🚀 Step 2: First Endpoint & Running the Server

### 1. Create `main.py`
```python
from fastapi import FastAPI

# 1. Create FastAPI application instance
app = FastAPI(title="FastAPI CRUD Tutorial")

# 2. Define a basic GET route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI CRUD Tutorial!"}
```

### 2. Breakdown of the Code
- `from fastapi import FastAPI`: Imports the FastAPI class.
- `app = FastAPI(...)`: Creates the main API application instance.
- `@app.get("/")`: Decorator telling FastAPI that when a user makes a `GET` request to `/`, run `read_root()`.
- `return {"message": ...}`: FastAPI automatically converts Python dictionaries into JSON!

### 3. Running the Server
```powershell
uvicorn main:app --reload
```
- `main`: Refers to `main.py` file.
- `app`: Refers to the `app = FastAPI()` object inside `main.py`.
- `--reload`: Auto-reloads the server whenever you save changes to your code.

### 4. Exploring the Automatic Interactive Docs
FastAPI automatically generates interactive API documentation for free:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📦 Step 3: Defining the Data Model (Pydantic Schema)

### 1. What is Pydantic?
FastAPI relies on **Pydantic** for:
- **Data validation**: Ensures request data matches expected types (e.g., `price` must be a number).
- **Serialization**: Converts Python objects to JSON automatically.
- **Auto Documentation**: Displays field schemas in `/docs`.

### 2. The Code to Add
```python
from typing import Optional
from pydantic import BaseModel

# 1. Define the Schema for an Item
class Item(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# 2. In-Memory "Database" (a simple Python list for now)
db_items: list[Item] = []
```

### 3. Key Concepts:
- `BaseModel`: Base class from Pydantic that your schema inherits from.
- `Optional[str] = None`: Optional field with a default value of `None`.
- `db_items`: An in-memory list where we'll temporarily store, read, update, and delete items.

---

## ➕ Step 4: "C" in CRUD — Create an Item (`POST`)

### 1. The Concept
- In REST APIs, the `POST` method is used to submit data to create a new resource.
- When an item is successfully created, we conventionally return HTTP status code **`201 Created`**.
- If a client tries to create an item with an ID that already exists, we raise an **`HTTPException(status_code=400, detail=...)`**.

### 2. The Code to Add
```python
from fastapi import FastAPI, HTTPException, status

# ... (Item model and db_items stay here)

# Create a new item (POST)
@app.post("/items/", status_code=status.HTTP_201_CREATED, response_model=Item)
def create_item(item: Item):
    # Check if item with the same id already exists
    for existing_item in db_items:
        if existing_item.id == item.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item with id {item.id} already exists"
            )
    
    # Save the item to our in-memory list
    db_items.append(item)
    return item
```

### 3. Key Concepts:
- `@app.post("/items/", ...)`: Maps HTTP POST requests at `/items/` to this function.
- `item: Item`: FastAPI reads the incoming JSON request body, validates it against `Item`, and injects it as `item`.
- `status_code=status.HTTP_201_CREATED`: Sets the response status code to 201 when creation succeeds.
- `raise HTTPException(...)`: Returns an error response with a proper HTTP code and JSON message (`{"detail": "..."}`).

---

## 📖 Step 5: "R" in CRUD — Read Items (Dynamic URL / Path Parameters)

### 1. The Concepts
We need two ways to read data:
1. **Get All Items**: `GET /items/` $\rightarrow$ returns the entire list.
2. **Get Single Item by Dynamic URL (Path Parameter)**: `GET /items/{item_id}` $\rightarrow$ dynamic parameter in the URL.
   - If found: return the item.
   - If not found: return **`404 Not Found`** using `HTTPException`.

---

### 2. The Code to Add

#### A. Read All Items
```python
# Read all items (GET)
@app.get("/items/", response_model=list[Item])
def get_all_items():
    return db_items
```

#### B. Read a Single Item by Dynamic Path Parameter (`{item_id}`)
```python
# Read single item by dynamic URL / path parameter (GET)
@app.get("/items/{item_id}", response_model=Item)
def get_item_by_id(item_id: int):
    for item in db_items:
        if item.id == item_id:
            return item
    
    # If not found, raise 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )
```

---

### 3. Key Concepts:
- **Dynamic Path Parameter `{item_id}`**: The `{item_id}` in the path matches the function argument `item_id: int`.
- **Automatic Type Conversion & Validation**: If a user requests `/items/abc`, FastAPI automatically returns a `422 Unprocessable Entity` error because `"abc"` cannot be parsed as an integer (`int`).
- **`status.HTTP_404_NOT_FOUND`**: Standard HTTP error status code for missing resources.

---

## ✏️ Step 6: "U" in CRUD — Update an Item (`PUT`)

### 1. The Concept
- HTTP `PUT` replaces or updates an existing resource.
- Notice how this route combines **both** a dynamic URL path parameter (`item_id: int`) and a request body (`updated_item: Item`).
- FastAPI automatically knows:
  - `item_id` comes from the URL path (`/items/{item_id}`).
  - `updated_item` comes from the JSON request body.

---

### 2. The Code to Add
```python
# Update an existing item (PUT)
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db_items):
        if item.id == item_id:
            # Keep ID consistent and update
            updated_item.id = item_id
            db_items[index] = updated_item
            return updated_item
            
    # If not found, raise 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )
```

### 3. Key Concepts:
- `@app.put("/items/{item_id}", ...)`: Listens for `PUT` requests at `/items/{item_id}`.
- `enumerate(db_items)`: Gives us both the index and the item so we can replace `db_items[index]` directly.
- **Combined Parameters**: Having both a path variable and a Pydantic model in the function signature is a core superpower of FastAPI.

---

## 🗑️ Step 7: "D" in CRUD — Delete an Item (`DELETE`)

### 1. The Concept
- HTTP `DELETE` removes an existing resource from the server.
- Takes the dynamic path parameter `item_id: int` to know which item to remove.
- If found: removes it from our list using `db_items.pop(index)` and returns a success message.
- If not found: raises **`404 Not Found`**.

---

### 2. The Code to Add
```python
# Delete an item (DELETE)
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
```

### 3. Key Concepts:
- `@app.delete("/items/{item_id}")`: Maps HTTP `DELETE` requests to this function.
- `db_items.pop(index)`: Removes the element at `index` from the list and returns the removed item.

---

## 📋 Full Code Summary (`main.py`)

Here is the complete CRUD implementation for easy reference:

```python
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="FastAPI CRUD Tutorial")

# 1. Pydantic Model (Schema)
class Item(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# 2. In-Memory Database
db_items: list[Item] = []

# Root / Health Check
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI CRUD Tutorial!"}

# CREATE (POST)
@app.post("/items/", status_code=status.HTTP_201_CREATED, response_model=Item)
def create_item(item: Item):
    for existing_item in db_items:
        if existing_item.id == item.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item with id {item.id} already exists"
            )
    db_items.append(item)
    return item

# READ ALL (GET)
@app.get("/items/", response_model=list[Item])
def get_all_items():
    return db_items

# READ ONE BY ID (GET with Path Parameter)
@app.get("/items/{item_id}", response_model=Item)
def get_item_by_id(item_id: int):
    for item in db_items:
        if item.id == item_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

# UPDATE (PUT with Path Parameter + Body)
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db_items):
        if item.id == item_id:
            updated_item.id = item_id
            db_items[index] = updated_item
            return updated_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

# DELETE (DELETE with Path Parameter)
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(db_items):
        if item.id == item_id:
            deleted_item = db_items.pop(index)
            return {"message": f"Item '{deleted_item.title}' (id: {item_id}) deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )
```

---

## 🔍 Step 8: Query Parameters & Filtering (Pagination & Search)

### 1. What is a Query Parameter?
- **Path Parameter**: Defined in URL path (`/items/{item_id}`) $\rightarrow$ identifies a specific resource.
- **Query Parameter**: Key-value pairs after `?` in the URL (`/items/?limit=5&is_available=true&search=book`) $\rightarrow$ used for filtering, sorting, or pagination.
- In FastAPI, any function argument that is **NOT** defined in the path is automatically treated as a **Query Parameter**!

---

### 2. Updating `get_all_items` with Query Parameters
```python
# 4. Read items with optional Query Parameters (Filtering & Search)
@app.get("/items/", response_model=list[Item])
def get_all_items(
    search: Optional[str] = None,
    is_available: Optional[bool] = None,
    limit: int = 10
):
    results = db_items

    # Filter by search string in title
    if search:
        results = [item for item in results if search.lower() in item.title.lower()]

    # Filter by availability
    if is_available is not None:
        results = [item for item in results if item.is_available == is_available]

    # Limit total number of results
    return results[:limit]
```

### 3. Key Concepts:
- `search: Optional[str] = None`: Optional query param `/items/?search=fastapi`.
- `is_available: Optional[bool] = None`: Optional boolean query param `/items/?is_available=true`.
- `limit: int = 10`: Has a default value of `10`. If not supplied by user, defaults to 10.
- Automatic interactive documentation in `/docs` renders individual input boxes for every query parameter!

---

## 🛡️ Step 9: Advanced Validation with Pydantic `Field`

### 1. Why use `Field`?
While Python type hints (`int`, `str`, `float`) check data types, **`Field`** allows you to enforce business logic rules directly in your model:
- **Numbers**: `gt` (>), `ge` (>=), `lt` (<), `le` (<=)
- **Strings**: `min_length`, `max_length`, `pattern` (regex)
- **Metadata for Swagger**: `description`, `examples`

---

### 2. Upgrading the `Item` Model
```python
from typing import Optional
from pydantic import BaseModel, Field

class Item(BaseModel):
    id: int = Field(
        ..., 
        gt=0, 
        description="Unique ID of the item (must be positive)",
        examples=[1]
    )
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="Title of the item (3 to 100 characters)",
        examples=["FastAPI Handbook"]
    )
    description: Optional[str] = Field(
        None, 
        max_length=300, 
        description="Optional detailed description"
    )
    price: float = Field(
        ..., 
        gt=0, 
        description="Price in USD (must be greater than 0)",
        examples=[29.99]
    )
    is_available: bool = Field(
        default=True, 
        description="Whether the item is in stock"
    )
```

### 3. Explanation of Parameters:
- `...` (Ellipsis): Marks the field as **required**.
- `gt=0`: Greater Than 0 (`price` cannot be `0` or negative).
- `min_length=3`: Rejects empty or 1-2 character strings.
- `max_length=100`: Prevents excessively large strings.
- `description` & `examples`: Automatically enhances the Swagger UI `/docs` documentation.

### 4. Automatic `422 Unprocessable Entity`
If a user submits invalid data (e.g. `price: -5` or `title: "a"`), FastAPI automatically intercepts it and returns a detailed `422` error specifying exactly which field violated which rule!

---

*(Next Step: Connecting a Real Database with SQLAlchemy & SQLite)*








