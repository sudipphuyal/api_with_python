# 🎓 DAY 3: SETTING UP FLASK & FIRST ENDPOINTS

## 📋 What You'll Learn

- **What is Flask?** - Python web framework
- **Create your first endpoint** - Handle GET requests
- **URL Parameters** - Extract data from URL
- **Query Parameters** - Extract data from URL query
- **POST Requests** - Receive JSON data
- **Status Codes** - Return appropriate HTTP codes
- **Error Handling** - Handle missing endpoints
- **Run local server** - Test everything locally
- **Use Postman** - Test your endpoints

---

## 🚀 Step 1: Install Flask

First time only, install Flask:

```bash
pip install flask
```

Or with Python 3 explicitly:

```bash
pip3 install flask
```

**Expected output:**

```
Successfully installed flask-X.X.X
```

---

## 🏃 Step 2: Run the Flask Server

```bash
python3 app.py
```

**You should see:**

```
* Running on http://127.0.0.1:5000
* Debugger is active!
* Restarting with reloader
```

**Important:** Keep this terminal window open while testing!

---

## 🧪 Step 3: Test with Postman

Open Postman in a separate window.

### Test 1: Check API Status

```
Method: GET
URL: http://localhost:5000/
Click Send

Response:
{
  "status": "API is running ✅",
  "version": "1.0",
  "endpoints": {...}
}
```

### Test 2: Simple Greeting

```
Method: GET
URL: http://localhost:5000/hello
Click Send

Response:
{
  "message": "Hello! This is your first Flask endpoint! 🎉",
  "method": "GET",
  "status": "success"
}
```

### Test 3: Get All Users

```
Method: GET
URL: http://localhost:5000/users
Click Send

Response:
{
  "success": true,
  "count": 3,
  "data": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
  ]
}
```

### Test 4: Get Specific User

```
Method: GET
URL: http://localhost:5000/users/2
Click Send

Response:
{
  "success": true,
  "data": {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  }
}
```

### Test 5: Get Non-existent User (404 Error)

```
Method: GET
URL: http://localhost:5000/users/999
Click Send

Response (404):
{
  "success": false,
  "message": "User 999 not found"
}
```

### Test 6: Search User by Name

```
Method: GET
URL: http://localhost:5000/search?name=Alice
Click Send

Response:
{
  "success": true,
  "count": 1,
  "data": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"}
  ]
}
```

**Try variations:**

- `/search?name=B` - Find all with "B"
- `/search?name=Charlie` - Find exact match
- `/search?name=XYZ` - No results (404)

### Test 7: Create New User (POST)

```
Method: POST
URL: http://localhost:5000/users
Headers: Content-Type: application/json
Body (raw JSON):
{
  "name": "Diana",
  "email": "diana@example.com"
}
Click Send

Response (201):
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 4,
    "name": "Diana",
    "email": "diana@example.com"
  }
}
```

### Test 8: Create User - Missing Field (400 Error)

```
Method: POST
URL: http://localhost:5000/users
Body:
{
  "name": "Eve"
}
(Missing email!)
Click Send

Response (400):
{
  "success": false,
  "message": "Missing required fields: name, email"
}
```

### Test 9: Create User - Duplicate Email (400 Error)

```
Method: POST
URL: http://localhost:5000/users
Body:
{
  "name": "Alice2",
  "email": "alice@example.com"
}
(Email already exists!)
Click Send

Response (400):
{
  "success": false,
  "message": "Email alice@example.com already exists"
}
```

### Test 10: Invalid Endpoint (404)

```
Method: GET
URL: http://localhost:5000/invalid
Click Send

Response (404):
{
  "success": false,
  "message": "Endpoint not found",
  "status": 404
}
```

---

## 📚 Understanding the Code

### Basic Endpoint Structure

```python
@app.route('/hello', methods=['GET'])
def hello():
    response = {"message": "Hello!"}
    return jsonify(response), 200
```

**Breakdown:**

- `@app.route()` - Decorator that tells Flask to listen on this URL
- `'/hello'` - The URL path
- `methods=['GET']` - Only accept GET requests
- `def hello():` - Function that handles this endpoint
- `return jsonify(response), 200` - Return JSON response with status 200

### URL Parameters (Dynamic URLs)

```python
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"id": user_id})
```

**How it works:**

- `<int:user_id>` - Capture number from URL
- Convert to integer
- Pass as parameter to function
- `GET /users/5` → `user_id = 5`

### Query Parameters (URL ?value=xyz)

```python
name = request.args.get('name', 'default')
```

**How it works:**

- `request.args.get()` - Get query parameter
- `'name'` - Parameter name
- `'default'` - Default value if not provided
- `GET /search?name=Alice` → `name = 'Alice'`

### POST Requests (Receive JSON)

```python
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    return jsonify({"created": name}), 201
```

**How it works:**

- `methods=['POST']` - Accept POST requests
- `request.get_json()` - Parse JSON from body
- `data['name']` - Extract field from JSON
- Return 201 (Created) status

### Return Responses

```python
return jsonify({"message": "success"}), 200
```

**Parts:**

- `jsonify()` - Convert Python dict to JSON
- `200` - HTTP status code
- Common codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found)

---

## 📊 All Endpoints Summary

| Method | URL            | Purpose        | Returns           |
| ------ | -------------- | -------------- | ----------------- |
| GET    | /              | API status     | Status info       |
| GET    | /hello         | Greeting       | Welcome message   |
| GET    | /users         | All users      | User list         |
| GET    | /users/{id}    | Specific user  | User data or 404  |
| GET    | /search?name=x | Search by name | Matching users    |
| POST   | /users         | Create user    | Created user, 201 |

---

## 🔄 Development Workflow

### While developing:

1. **Edit code** in app.py
2. **Save file** (Ctrl+S)
3. **Flask auto-reloads** - You'll see "Restarting with reloader"
4. **Test in Postman** - No need to restart server!

### Example:

```
Edit endpoint → Save file → Flask reloads → Test in Postman
```

**To stop server:**
Press `CTRL+C` in the terminal

---

## 🎯 Common Testing Scenarios

### Scenario 1: Wrong Method

```
Try: POST /hello
Result: Method not allowed (405)
Reason: /hello only accepts GET
```

### Scenario 2: Missing Required Data

```
POST /users with body: {"name": "Bob"}
Result: 400 Bad Request
Reason: Email field missing
```

### Scenario 3: Resource Not Found

```
GET /users/999
Result: 404 Not Found
Reason: User with ID 999 doesn't exist
```

### Scenario 4: Duplicate Data

```
POST /users with email that already exists
Result: 400 Bad Request
Reason: Email must be unique
```

---

## 📋 Postman Quick Checklist

- [ ] Install Postman
- [ ] Run Flask server: `python3 app.py`
- [ ] Test GET / endpoint
- [ ] Test GET /hello endpoint
- [ ] Test GET /users endpoint
- [ ] Test GET /users/1 endpoint
- [ ] Test GET /search?name=Alice
- [ ] Test POST /users with valid data (201)
- [ ] Test POST /users with missing field (400)
- [ ] Test invalid endpoint (404)
- [ ] Try modifying users and see POST responses

---

## 💡 Key Concepts

### Flask Decorator

```python
@app.route('/path', methods=['GET', 'POST'])
```

Tells Flask which URL and HTTP method to listen for

### jsonify()

```python
jsonify({"key": "value"})
```

Converts Python dict to JSON response

### request Object

```python
request.get_json()      # Get JSON body
request.args.get('param')  # Get query parameter
```

Access data from the HTTP request

### Status Codes

```python
return response, 200  # OK
return response, 201  # Created
return response, 400  # Bad Request
return response, 404  # Not Found
```

Tell client what happened

---

## 🎓 Practice Assignments

### Task 1: Add New Endpoint

Create an endpoint:

```
GET /users/count
Returns: Total number of users
```

### Task 2: Add Validation

In POST /users, add validation:

- Email must contain '@'
- Name must be at least 2 characters

### Task 3: Add PUT Endpoint

```
PUT /users/<id>
Updates existing user
```

### Task 4: Add DELETE Endpoint

```
DELETE /users/<id>
Deletes user
Returns: Success message
```

---

## 🚨 Troubleshooting

### "Port 5000 already in use"

Another process is using port 5000

```bash
# Find process on port 5000
lsof -i :5000

# Kill process (Mac/Linux)
kill -9 <PID>
```

### "ModuleNotFoundError: No module named 'flask'"

Flask not installed

```bash
pip install flask
```

### Changes not showing up

Flask might not be in debug mode. Restart:

```bash
CTRL+C (stop server)
python3 app.py (restart)
```

### "Address already in use"

Wait 20 seconds or use different port:

```bash
# Change in app.py: port=5001
```

---

## 🎉 Success Indicators

You know Day 3 is complete when:

- ✅ Flask server runs without errors
- ✅ Postman receives response from /hello
- ✅ GET /users returns list of users
- ✅ POST /users creates new user with 201 status
- ✅ GET /users/999 returns 404 error
- ✅ POST with missing data returns 400 error
- ✅ All responses are valid JSON

---

## 📌 Files Created

- [app.py](app.py) - Your first Flask API server

---

## 🚀 Ready for Day 4?

Next we'll:

- Master GET requests with parameters
- Learn filtering and sorting
- Practice more complex queries
- Build search functionality

**When ready, just let me know! 🎉**

---

**Key Takeaway:** You've built your first real API server! It runs locally, accepts requests, and returns JSON responses. Postman tests it. This is how real APIs work! 🚀
