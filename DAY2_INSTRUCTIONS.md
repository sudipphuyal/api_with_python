# 🎓 DAY 2: HTTP CONCEPTS & REQUEST/RESPONSE CYCLE

## 📋 What You'll Learn

- **HTTP Protocol** - How web communication works
- **HTTP Methods** - GET, POST, PUT, DELETE (what each does)
- **Request Anatomy** - What you send to a server
- **Response Anatomy** - What server sends back
- **Status Codes** - Understanding server responses (200, 404, 500, etc.)
- **Headers** - Metadata about requests/responses
- **JSON Format** - Standard data format for APIs
- **Request/Response Flow** - Complete cycle explained
- **Practical Handlers** - Write code that processes requests

---

## 🚀 Step 1: Run the Script

```bash
python3 day2_http_concepts.py
```

This will show you:

- Detailed explanations with output
- Real examples of requests and responses
- Simulated server processing
- Practical code you can modify

---

## 📚 Key Concepts Explained

### 1️⃣ HTTP Methods (What action?)

| Method     | Purpose              | Example                    | Status         |
| ---------- | -------------------- | -------------------------- | -------------- |
| **GET**    | Retrieve data        | `GET /users/1`             | 200 OK         |
| **POST**   | Create new data      | `POST /users` + JSON body  | 201 Created    |
| **PUT**    | Update existing data | `PUT /users/1` + JSON body | 200 OK         |
| **DELETE** | Remove data          | `DELETE /users/1`          | 204 No Content |

**In Postman:**

- Select the method from dropdown
- Type the URL
- Click Send

### 2️⃣ Request Structure

```
GET /users/1
Host: localhost:5000
Content-Type: application/json
Accept: application/json

(no body for GET)
```

### 3️⃣ Response Structure

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 256

{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

### 4️⃣ Status Codes (First digit tells the story)

- **2xx** (200, 201) = ✅ Success
- **3xx** (301, 302) = 🔄 Redirect
- **4xx** (400, 404, 422) = ⚠️ Your mistake
- **5xx** (500, 503) = ❌ Server error

**Common codes:**

- `200` - Request worked
- `201` - Resource created
- `400` - Bad request (invalid data)
- `404` - Not found
- `500` - Server error

### 5️⃣ JSON Format

**Python Dictionary:**

```python
user = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "tags": ["python", "api"]
}
```

**Same as JSON (sent in HTTP):**

```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "tags": ["python", "api"]
}
```

---

## 🔄 The Complete Flow (What happens when you click "Send" in Postman)

```
1. [POSTMAN] You click "Send" button
                ↓
2. [POSTMAN] Prepares HTTP request with:
   - Method (GET, POST, etc.)
   - URL (http://localhost:5000/users)
   - Headers (Content-Type, Accept, etc.)
   - Body (data to send, if any)
                ↓
3. [NETWORK] Request travels over the internet
                ↓
4. [SERVER] Receives request on port 5000
                ↓
5. [SERVER] Router says "Oh, this is for /users endpoint"
                ↓
6. [SERVER] Function runs (check database, validate data, etc.)
                ↓
7. [SERVER] Creates response with:
   - Status code (200, 404, 500, etc.)
   - Headers (Content-Type, etc.)
   - Body (JSON data to return)
                ↓
8. [NETWORK] Response travels back to Postman
                ↓
9. [POSTMAN] Receives response
                ↓
10. [YOU] See status, headers, and body in Postman
```

---

## 💡 Real Examples (From the script)

### GET Request Example

**In Postman:**

```
Method: GET
URL: http://localhost:5000/users/1
```

**Server processes:**

```
Look up user with ID=1
Found it!
Return JSON response
```

**Postman shows:**

```
Status: 200 OK
Body:
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

### POST Request Example

**In Postman:**

```
Method: POST
URL: http://localhost:5000/users
Body:
{
  "name": "Charlie",
  "email": "charlie@example.com"
}
```

**Server processes:**

```
Check if name and email provided ✓
Add to database
Return success with new user ID
```

**Postman shows:**

```
Status: 201 Created
Body:
{
  "success": true,
  "message": "User created",
  "data": {
    "id": 3,
    "name": "Charlie",
    "email": "charlie@example.com"
  }
}
```

---

## 🎯 Headers Explained

### Request Headers (Client sends to Server)

| Header          | Meaning                         | Example             |
| --------------- | ------------------------------- | ------------------- |
| `Content-Type`  | Format of body data             | `application/json`  |
| `Accept`        | Format client wants response in | `application/json`  |
| `Authorization` | Authentication token            | `Bearer eyJhbGc...` |

### Response Headers (Server sends to Client)

| Header           | Meaning                   | Example            |
| ---------------- | ------------------------- | ------------------ |
| `Content-Type`   | Format of response body   | `application/json` |
| `Content-Length` | Size of response in bytes | `256`              |

**In Postman:** You can see headers by clicking the "Headers" tab

---

## 🎓 HTTP Methods in Our Todo App

Let's say we're building a Todo API:

```
GET /todos                  → Get all todos
POST /todos                 → Create new todo
GET /todos/1                → Get specific todo
PUT /todos/1                → Update todo
DELETE /todos/1             → Delete todo
```

**In Postman, test each:**

1. `GET http://localhost:5000/todos` → See all todos
2. `POST http://localhost:5000/todos` with JSON body → Create todo
3. `GET http://localhost:5000/todos/1` → See specific todo
4. `PUT http://localhost:5000/todos/1` → Update it
5. `DELETE http://localhost:5000/todos/1` → Delete it

---

## 🎓 Practice Assignments

### Task 1: Understand Status Codes

Look at the script output and match:

- ✅ When would you get `200 OK`?
- ✅ When would you get `404 Not Found`?
- ✅ When would you get `400 Bad Request`?
- ✅ When would you get `201 Created`?

### Task 2: Modify the Handler

Edit the `create_todo_api_handler()` function to:

- Add support for PUT method (update todo)
- Add support for DELETE method (delete todo)
- Add proper validation

### Task 3: Create a Response

Write a Python function that creates this response:

```json
{
  "success": true,
  "message": "Data processed",
  "data": [1, 2, 3, 4, 5]
}
```

### Task 4: Parse JSON

Convert this JSON string to Python dictionary:

```python
json_string = '{"user": "Alice", "age": 25, "active": true}'
```

---

## 📊 Visual Summary

```
┌─────────────────────────────────────────┐
│         CLIENT (Postman)                │
│  ┌─────────────────────────────────┐   │
│  │   User clicks "Send"            │   │
│  └────────────────┬────────────────┘   │
│                   │                     │
│               REQUEST                  │
│         (GET /users, POST data)        │
│                   │                     │
└─────────────────────────────────────────┘
          ↓        ↓        ↓
    ┌────────────────────────┐
    │      NETWORK           │
    │ (Internet/Localhost)   │
    └────────────────────────┘
          ↓        ↓        ↓
┌─────────────────────────────────────────┐
│         SERVER (Flask app)              │
│  ┌─────────────────────────────────┐   │
│  │   Receives request              │   │
│  │   Processes (database, etc)     │   │
│  │   Creates response (JSON)       │   │
│  └────────────────┬────────────────┘   │
│                   │                     │
│              RESPONSE                  │
│     (200 OK, JSON body)                │
│                   │                     │
└─────────────────────────────────────────┘
          ↑        ↑        ↑
    ┌────────────────────────┐
    │      NETWORK           │
    │ (Internet/Localhost)   │
    └────────────────────────┘
          ↑        ↑        ↑
┌─────────────────────────────────────────┐
│         CLIENT (Postman)                │
│  ┌─────────────────────────────────┐   │
│  │   Receives response             │   │
│  │   Shows status, headers, body   │   │
│  └─────────────────────────────────┘   │
│                                         │
│   You see: 200 OK                       │
│   Body tab shows JSON response          │
└─────────────────────────────────────────┘
```

---

## 📝 Key Takeaway

When you use Postman:

1. You're a **Client** making HTTP requests
2. Your code will be a **Server** receiving those requests
3. You respond with appropriate status codes and JSON data
4. Postman shows what you send and what you get back

**Next:** We'll build an actual Flask server that handles these requests!

---

## 🎯 Ready for Day 3?

When you're comfortable with HTTP concepts, let us know!

We'll move to:

- **Setting up Flask** (Python web framework)
- **Creating your first endpoint**
- **Running your local server**
- **Testing with Postman**

**Keep learning! 🚀**
