# 🎓 DAY 5: MASTERING POST REQUESTS & DATA VALIDATION

## 📋 What You'll Learn

- **POST requests** - Receive JSON data from client
- **Data validation** - Check if data is valid before processing
- **Error handling** - Return proper error messages with status codes
- **PUT requests** - Update existing data
- **DELETE requests** - Remove data
- **Batch operations** - Process multiple items at once
- **Status codes** - Use 200, 201, 400, 404, 500 correctly

---

## 🎯 Key Concepts

### Request & Response in API Flow

```
CLIENT (Postman)          SERVER (Flask)
    │                         │
    │ POST /users             │
    │ JSON body               │
    ├────────────────────────>│
    │                         │ Validate data
    │                         │ Check rules
    │                         │ Store in database
    │                         │ Create response
    │<────────────────────────┤
    │ 201 Created             │
    │ Response JSON           │
    │                         │
```

---

## 📊 HTTP Methods & Status Codes

| Method | Purpose | Success Code | Error Code      |
| ------ | ------- | ------------ | --------------- |
| POST   | Create  | 201 Created  | 400 Bad Request |
| PUT    | Update  | 200 OK       | 400/404         |
| DELETE | Remove  | 200 OK       | 404 Not Found   |
| GET    | Read    | 200 OK       | 404 Not Found   |

---

## 🚀 Step 1: Run the Server

```bash
cd /Users/sudipphuyal/Developments/Learn/API
source venv/bin/activate
python3 day5_post_requests.py
```

You should see:

```
* Running on http://localhost:5000
* Debugger is active!
```

---

## 🧪 Testing with Postman

### Test 1: Create User (POST) ✅

```
Method: POST
URL: http://localhost:5000/users
Headers: Content-Type: application/json

Body (raw JSON):
{
  "name": "Diana",
  "email": "diana@example.com",
  "age": 26
}

Click Send
```

**Expected Response (201 Created):**

```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 4,
    "name": "Diana",
    "email": "diana@example.com",
    "age": 26
  }
}
```

Status: **201 Created** (green)

---

### Test 2: Validation Error - Missing Field ❌

```
Method: POST
URL: http://localhost:5000/users

Body (missing email):
{
  "name": "Eve",
  "age": 30
}

Click Send
```

**Expected Response (400 Bad Request):**

```json
{
  "success": false,
  "error": "Field 'email' is required",
  "status": 400
}
```

Status: **400 Bad Request** (red)

---

### Test 3: Validation Error - Invalid Email ❌

```
Method: POST
URL: http://localhost:5000/users

Body (email without @):
{
  "name": "Frank",
  "email": "notanemail",
  "age": 30
}

Click Send
```

**Expected Response (400):**

```json
{
  "success": false,
  "error": "Invalid email format (must contain @)",
  "status": 400
}
```

---

### Test 4: Validation Error - Duplicate Email ❌

```
Method: POST
URL: http://localhost:5000/users

Body (email already exists):
{
  "name": "Alice2",
  "email": "alice@example.com",
  "age": 30
}

Click Send
```

**Expected Response (400):**

```json
{
  "success": false,
  "error": "Email 'alice@example.com' already exists",
  "status": 400
}
```

---

### Test 5: See All Users (GET)

```
Method: GET
URL: http://localhost:5000/users

Click Send
```

**Response:**

```json
{
  "success": true,
  "count": 3,
  "data": [
    {"id": 1, "name": "Alice", ...},
    {"id": 2, "name": "Bob", ...},
    {"id": 3, "name": "Charlie", ...}
  ]
}
```

Notice: New user Diana is NOT here (validation failed, so not created)

---

### Test 6: Update User (PUT) 🔄

```
Method: PUT
URL: http://localhost:5000/users/1
Content-Type: application/json

Body (update only name):
{
  "name": "Alice Johnson"
}

Click Send
```

**Response (200 OK):**

```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 25
  }
}
```

---

### Test 7: Update Multiple Fields (PUT)

```
Method: PUT
URL: http://localhost:5000/users/2

Body (update name and age):
{
  "name": "Robert",
  "age": 31
}

Click Send
```

**Response (200 OK):** User updated with both fields

---

### Test 8: Update Non-existent User (PUT)

```
Method: PUT
URL: http://localhost:5000/users/999

Body:
{
  "name": "Test"
}

Click Send
```

**Response (404 Not Found):**

```json
{
  "success": false,
  "error": "User 999 not found",
  "status": 404
}
```

---

### Test 9: Delete User (DELETE) 🗑️

```
Method: DELETE
URL: http://localhost:5000/users/3
(No body needed)

Click Send
```

**Response (200 OK):**

```json
{
  "success": true,
  "message": "User deleted successfully",
  "data": {
    "id": 3,
    "name": "Charlie",
    "email": "charlie@example.com",
    "age": 28
  }
}
```

---

### Test 10: Delete Non-existent User (DELETE)

```
Method: DELETE
URL: http://localhost:5000/users/999

Click Send
```

**Response (404):**

```json
{
  "success": false,
  "error": "User 999 not found",
  "status": 404
}
```

---

### Test 11: Create Multiple Users (Batch) 📦

```
Method: POST
URL: http://localhost:5000/users/batch
Content-Type: application/json

Body:
{
  "users": [
    {"name": "User1", "email": "user1@example.com", "age": 25},
    {"name": "User2", "email": "user2@example.com", "age": 30},
    {"name": "User3", "email": "user3@example.com", "age": 28}
  ]
}

Click Send
```

**Response (201 - All successful):**

```json
{
  "success": true,
  "created_count": 3,
  "error_count": 0,
  "created_users": [...],
  "errors": []
}
```

---

### Test 12: Batch with Some Errors 📦

```
Method: POST
URL: http://localhost:5000/users/batch

Body (one invalid):
{
  "users": [
    {"name": "Valid1", "email": "valid1@example.com", "age": 25},
    {"name": "BadEmail", "email": "notanemail", "age": 30},
    {"name": "Valid2", "email": "valid2@example.com", "age": 28}
  ]
}

Click Send
```

**Response (207 - Partial success):**

```json
{
  "success": false,
  "created_count": 2,
  "error_count": 1,
  "created_users": [valid users...],
  "errors": [
    {
      "index": 1,
      "error": "Invalid email format (must contain @)",
      "data": {...}
    }
  ]
}
```

---

### Test 13: Create Todo (POST)

```
Method: POST
URL: http://localhost:5000/todos
Content-Type: application/json

Body:
{
  "title": "Master POST requests",
  "description": "Learn validation and error handling"
}

Click Send
```

**Response (201):**

```json
{
  "success": true,
  "message": "Todo created",
  "data": {
    "id": 3,
    "title": "Master POST requests",
    "description": "Learn validation and error handling",
    "completed": false
  }
}
```

---

## 📚 Understanding Validation

### Validation checks:

```python
✓ Required fields present
✓ Data types correct (string, integer, etc.)
✓ Values in valid range (age 1-150)
✓ String length requirements (name ≥2 chars)
✓ Format requirements (email must have @)
✓ Uniqueness checks (no duplicate emails)
```

### Validation flow:

```
POST request received
       ↓
Extract JSON data
       ↓
Check required fields
       ↓
Check data types
       ↓
Check value ranges
       ↓
Check format (email)
       ↓
Check uniqueness
       ↓
If any fails → Return 400 error
If all pass  → Create and return 201
```

---

## 📋 Complete Testing Checklist

- [ ] POST /users (valid data) → 201 Created
- [ ] POST /users (missing field) → 400 Bad Request
- [ ] POST /users (invalid email) → 400 Bad Request
- [ ] POST /users (age out of range) → 400 Bad Request
- [ ] POST /users (duplicate email) → 400 Bad Request
- [ ] GET /users (see all users)
- [ ] PUT /users/1 (update one field) → 200 OK
- [ ] PUT /users/1 (update multiple fields) → 200 OK
- [ ] PUT /users/999 (non-existent) → 404 Not Found
- [ ] DELETE /users/3 → 200 OK
- [ ] DELETE /users/999 → 404 Not Found
- [ ] POST /users/batch (all valid) → 201 Created
- [ ] POST /users/batch (some invalid) → 207 Multi-status
- [ ] POST /todos (valid) → 201 Created
- [ ] POST /todos (title too short) → 400 Bad Request

---

## 🎯 Key Learning Points

### 1. POST Requests

**Purpose:** Create new data  
**Status Code:** 201 Created (success) or 400 Bad Request (error)

### 2. Validation

**Check:** Data is complete, correct type, valid values  
**Return:** Error message explaining what's wrong

### 3. PUT Requests

**Purpose:** Update existing data  
**Partial updates:** Update only provided fields

### 4. DELETE Requests

**Purpose:** Remove data  
**Status Code:** 200 OK (success) or 404 Not Found

### 5. Error Responses

**Always include:**

- `success: false`
- `error: "detailed message"`
- `status: error_code`

### 6. Batch Operations

**Handle:** Multiple items with individual validation  
**Return:** Created count, error count, and detailed errors

---

## 💡 Pro Tips

### Tip 1: Always Validate Input

```python
if not email or '@' not in email:
    return 400 error
```

### Tip 2: Provide Helpful Error Messages

```
❌ Bad:  "Invalid"
✅ Good: "Invalid email format (must contain @)"
```

### Tip 3: Use Correct Status Codes

```
201 → Resource created
200 → Update successful
400 → Client error (bad data)
404 → Resource not found
500 → Server error
```

### Tip 4: Validate After Each Step

```
1. Check field exists
2. Check correct type
3. Check valid value
4. Check uniqueness
```

### Tip 5: Return Created/Updated Data

Always send back the object that was created/updated so client sees result

---

## 🎓 Practice Assignments

### Task 1: Add Email Uniqueness in PUT

Ensure when updating email, no other user has it

### Task 2: Add Validation for Update

Check field values in PUT request before updating

### Task 3: Add Todo Update Endpoint

```
PUT /todos/<id>
Update title, description, or completed status
```

### Task 4: Add Todo Delete Endpoint

```
DELETE /todos/<id>
Delete a todo item
```

### Task 5: Add Name Length Check

Ensure names don't exceed 50 characters

---

## 🔄 Request Method Reference

```
GET    /users           → Retrieve all users
GET    /users/1         → Retrieve user 1
POST   /users           → Create new user
PUT    /users/1         → Update user 1
DELETE /users/1         → Delete user 1
```

**In Postman:** Select method from dropdown, type URL, fill body for POST/PUT

---

## 🚨 Common Mistakes

### ❌ Mistake 1: No Validation

```python
# BAD
user = data['name']  # What if 'name' missing?

# GOOD
if 'name' not in data:
    return error 400
```

### ❌ Mistake 2: Wrong Status Code

```python
# BAD
return response, 200  # Created user but returned 200

# GOOD
return response, 201  # Use 201 for creation
```

### ❌ Mistake 3: Unclear Error Messages

```python
# BAD
"Invalid input"

# GOOD
"Field 'email' must contain @ symbol"
```

### ❌ Mistake 4: No Error Details

```python
# BAD
if error:
    return 400

# GOOD
if error:
    return jsonify({
        "success": False,
        "error": "Specific error message",
        "status": 400
    }), 400
```

---

## 🎉 Success Indicators

You've mastered Day 5 when:

- ✅ POST creates new users with 201 status
- ✅ Validation prevents invalid data (400 errors)
- ✅ PUT updates users correctly
- ✅ DELETE removes users
- ✅ All error messages are clear
- ✅ Batch operations work
- ✅ All validation rules work
- ✅ Status codes are correct

---

## 📌 Files

- [day5_post_requests.py](day5_post_requests.py) - Complete Flask app with POST/PUT/DELETE

---

## 🚀 What's Next?

**Day 6:** Database Integration

- Connect to real database (SQLite)
- Replace in-memory data with persistent storage
- Learn CRUD operations with database

**Keep building! 🌟**
