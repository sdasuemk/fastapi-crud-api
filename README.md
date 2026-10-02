# 🚀 FastAPI CRUD REST API

A clean, beginner-to-intermediate, production-structured RESTful CRUD API built with **FastAPI**, **Pydantic v2**, and **Uvicorn**.

Includes a comprehensive, self-paced learning tutorial in [`FASTAPI_CRUD_GUIDE.md`](./FASTAPI_CRUD_GUIDE.md).

---

## ⚡ Features

- ⚡ **Lightning Fast**: Built on Starlette and Pydantic with asynchronous Python.
- 📦 **Pydantic Validation**: Strict request/response validation and serialization.
- 🛣️ **Full CRUD Operations**:
  - **Create (`POST`)**: Resource creation with duplicate ID validation & `201 Created`.
  - **Read (`GET`)**: Fetch all items with query parameters (`search`, `is_available`, `limit`) + Dynamic path lookup (`/items/{id}`).
  - **Update (`PUT`)**: Full item updates with path + body integration.
  - **Delete (`DELETE`)**: Resource removal with proper status code and error handling.
- 📖 **Interactive API Docs**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).
- 🛡️ **Robust Error Handling**: Standardized HTTP 400, 404, and 422 responses.

---

## 📋 API Endpoints Reference

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `GET` | `/` | Health check & welcome message | `200 OK` |
| `POST` | `/items/` | Create a new item | `201 Created` / `400 Bad Request` |
| `GET` | `/items/` | List all items (with `search`, `is_available`, `limit`) | `200 OK` |
| `GET` | `/items/{item_id}` | Fetch a single item by dynamic ID | `200 OK` / `404 Not Found` |
| `PUT` | `/items/{item_id}` | Update an existing item | `200 OK` / `404 Not Found` |
| `DELETE`| `/items/{item_id}` | Delete an item | `200 OK` / `404 Not Found` |

---

## 🛠️ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/sdasuemk/fastapi-crud-api.git
cd fastapi-crud-api
```

### 2. Set up virtual environment
```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run development server
```bash
uvicorn main:app --reload
```

Server runs on: **`http://127.0.0.1:8000`**

---

## 📖 Interactive Documentation
Once the server is running, explore and test the endpoints interactively:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📂 Project Structure
```text
curd-fastAPI/
├── main.py                  # FastAPI application and route endpoints
├── FASTAPI_CRUD_GUIDE.md    # Step-by-step learning guide & notes
├── requirements.txt         # Project dependencies
├── .gitignore               # Ignored files (venv, pycache, etc.)
└── README.md                # Project documentation
```

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
