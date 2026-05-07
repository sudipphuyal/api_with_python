"""
DAY 3: SETTING UP FLASK & FIRST ENDPOINTS
==========================================
Build your first web server with Flask!
Flask is a Python framework that makes building APIs easy.
"""

from flask import Flask, jsonify, request
import json

# ==============================================================================
# 1. WHAT IS FLASK?
# ==============================================================================
"""
FLASK is a lightweight Python web framework for building web APIs.

Why Flask?
✅ Simple and beginner-friendly
✅ Perfect for REST APIs
✅ Handles HTTP requests/responses automatically
✅ Large community and lots of tutorials
✅ Easy to test with Postman

How it works:
1. You define endpoints (functions) for each URL
2. User sends request to URL in Postman
3. Flask routes to correct function
4. Function processes and returns response
5. Postman receives response
"""

# Create Flask app
app = Flask(__name__)

print("=" * 80)
print("DAY 3: SETTING UP FLASK & FIRST ENDPOINTS")
print("=" * 80)


# ==============================================================================
# 2. YOUR FIRST ENDPOINT - GET /hello
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 1: GET /hello - Simple greeting")
print("=" * 80)


@app.route('/hello', methods=['GET'])
def hello():
    """
    Simple GET endpoint that returns a greeting.

    How it works:
    1. @app.route() decorator tells Flask to listen on /hello
    2. methods=['GET'] means only GET requests accepted
    3. When request comes, this function runs
    4. Return value becomes HTTP response
    """
    response = {
        "message": "Hello! This is your first Flask endpoint! 🎉",
        "method": "GET",
        "status": "success"
    }
    return jsonify(response)


print("""
In Postman:
- Method: GET
- URL: http://localhost:5000/hello
- Click Send

Response:
{
  "message": "Hello! This is your first Flask endpoint! 🎉",
  "method": "GET",
  "status": "success"
}
""")


# ==============================================================================
# 3. ENDPOINT WITH URL PARAMETERS - GET /users/<id>
# ==============================================================================
print("=" * 80)
print("ENDPOINT 2: GET /users/<id> - Get user by ID")
print("=" * 80)

# Fake database
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
}


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    GET endpoint that accepts a parameter (user ID).

    <int:user_id> means:
    - Take the number from URL
    - Convert to integer
    - Pass as parameter 'user_id'
    """
    if user_id in users_db:
        return jsonify({
            "success": True,
            "data": users_db[user_id]
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"User {user_id} not found"
        }), 404


print("""
In Postman:
- Method: GET
- URL: http://localhost:5000/users/1
- Click Send

Response (Success):
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
}

Try: http://localhost:5000/users/999
Response (Not Found):
{
  "success": false,
  "message": "User 999 not found"
}
""")


# ==============================================================================
# 4. GET ALL ITEMS - GET /users
# ==============================================================================
print("=" * 80)
print("ENDPOINT 3: GET /users - Get all users")
print("=" * 80)


@app.route('/users', methods=['GET'])
def get_all_users():
    """
    GET endpoint that returns all items from database.
    """
    users_list = list(users_db.values())
    return jsonify({
        "success": True,
        "count": len(users_list),
        "data": users_list
    }), 200


print("""
In Postman:
- Method: GET
- URL: http://localhost:5000/users
- Click Send

Response:
{
  "success": true,
  "count": 3,
  "data": [
    {"id": 1, "name": "Alice", ...},
    {"id": 2, "name": "Bob", ...},
    {"id": 3, "name": "Charlie", ...}
  ]
}
""")


# ==============================================================================
# 5. POST REQUEST - CREATE NEW USER
# ==============================================================================
print("=" * 80)
print("ENDPOINT 4: POST /users - Create new user")
print("=" * 80)


@app.route('/users', methods=['POST'])
def create_user():
    """
    POST endpoint that receives data and creates new user.

    How it works:
    1. Client sends JSON data in request body
    2. request.get_json() extracts that data
    3. Validate the data
    4. Add to database
    5. Return success response with 201 status
    """
    data = request.get_json()

    # Validation: Check if required fields present
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: name, email"
        }), 400

    # Check if email already exists
    for user in users_db.values():
        if user['email'] == data['email']:
            return jsonify({
                "success": False,
                "message": f"Email {data['email']} already exists"
            }), 400

    # Create new user
    new_id = max(users_db.keys()) + 1
    new_user = {
        "id": new_id,
        "name": data['name'],
        "email": data['email']
    }
    users_db[new_id] = new_user

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": new_user
    }), 201


print("""
In Postman:
- Method: POST
- URL: http://localhost:5000/users
- Headers: Content-Type: application/json
- Body (raw JSON):
  {
    "name": "Diana",
    "email": "diana@example.com"
  }
- Click Send

Response:
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 4,
    "name": "Diana",
    "email": "diana@example.com"
  }
}

Error Response (Missing field):
- Body:
  {
    "name": "Eve"
  }

Returns 400:
{
  "success": false,
  "message": "Missing required fields: name, email"
}
""")


# ==============================================================================
# 6. ERROR HANDLING - 404 NOT FOUND
# ==============================================================================
print("=" * 80)
print("ENDPOINT 5: Error handling - 404")
print("=" * 80)


@app.errorhandler(404)
def not_found(error):
    """
    Handle requests to endpoints that don't exist.
    """
    return jsonify({
        "success": False,
        "message": "Endpoint not found",
        "status": 404
    }), 404


print("""
Try non-existent endpoint:
- URL: http://localhost:5000/nonexistent

Response (404):
{
  "success": false,
  "message": "Endpoint not found",
  "status": 404
}
""")


# ==============================================================================
# 7. STATUS SUMMARY ENDPOINT
# ==============================================================================
print("=" * 80)
print("ENDPOINT 6: GET / - API Status")
print("=" * 80)


@app.route('/', methods=['GET'])
def api_status():
    """
    Root endpoint showing API status and available endpoints.
    """
    return jsonify({
        "status": "API is running ✅",
        "version": "1.0",
        "endpoints": {
            "GET /": "This status page",
            "GET /hello": "Simple greeting",
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID",
            "POST /users": "Create new user"
        }
    }), 200


print("""
In Postman:
- Method: GET
- URL: http://localhost:5000/
- Click Send

Response:
{
  "status": "API is running ✅",
  "version": "1.0",
  "endpoints": {
    "GET /": "This status page",
    "GET /hello": "Simple greeting",
    ...
  }
}
""")


# ==============================================================================
# 8. QUERY PARAMETERS - GET /search?name=Alice
# ==============================================================================
print("=" * 80)
print("ENDPOINT 7: Query parameters - Search")
print("=" * 80)


@app.route('/search', methods=['GET'])
def search_user():
    """
    GET endpoint that uses query parameters.

    Query parameters are sent in URL after ?
    Example: /search?name=Alice
    Access via: request.args.get('name')
    """
    name = request.args.get('name', '').strip()

    if not name:
        return jsonify({
            "success": False,
            "message": "Please provide name parameter: /search?name=Alice"
        }), 400

    # Search in database
    results = []
    for user in users_db.values():
        if name.lower() in user['name'].lower():
            results.append(user)

    if results:
        return jsonify({
            "success": True,
            "count": len(results),
            "data": results
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"No users found with name containing '{name}'"
        }), 404


print("""
In Postman:
- Method: GET
- URL: http://localhost:5000/search?name=Alice
- Click Send

Response:
{
  "success": true,
  "count": 1,
  "data": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"}
  ]
}

Try: /search?name=B
Returns all users with 'B' in name
""")


# ==============================================================================
# 9. ENDPOINT SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("SUMMARY OF ENDPOINTS")
print("=" * 80)

endpoints_summary = """
╔════════════════════════════════════════════════════════════════════╗
║                    YOUR FIRST API ENDPOINTS                        ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  1. GET /                                                          ║
║     Purpose: Check API status & list all endpoints                ║
║     Response: Status, version, available endpoints                ║
║                                                                    ║
║  2. GET /hello                                                     ║
║     Purpose: Simple greeting endpoint                             ║
║     Response: Welcome message                                     ║
║                                                                    ║
║  3. GET /users                                                     ║
║     Purpose: Get all users                                        ║
║     Response: List of all users with count                        ║
║                                                                    ║
║  4. GET /users/<id>                                                ║
║     Purpose: Get specific user by ID                              ║
║     Param: id (number)                                            ║
║     Response: User data or 404 error                              ║
║                                                                    ║
║  5. GET /search?name=<search_term>                                 ║
║     Purpose: Search users by name                                 ║
║     Param: name (query parameter)                                 ║
║     Response: Matching users or 404                               ║
║                                                                    ║
║  6. POST /users                                                    ║
║     Purpose: Create new user                                      ║
║     Body: {"name": "...", "email": "..."}                         ║
║     Response: Created user with 201 status                        ║
║                                                                    ║
║  7. Error Handler (404)                                           ║
║     Purpose: Handle undefined endpoints                           ║
║     Response: 404 error message                                   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""
print(endpoints_summary)


# ==============================================================================
# 10. RUNNING THE SERVER
# ==============================================================================
print("\n" + "=" * 80)
print("HOW TO RUN THE SERVER")
print("=" * 80)

run_instructions = """
STEP 1: Install Flask (first time only)
  $ pip install flask

STEP 2: Run this script
  $ python3 app.py

STEP 3: You should see:
  * Running on http://127.0.0.1:5000
  * press CTRL+C to quit
  * Restarting with reloader

STEP 4: Open Postman and start testing!
  - Paste URLs like: http://localhost:5000/hello
  - Try different methods: GET, POST
  - See responses appear in Postman

STEP 5: Try all endpoints
  GET http://localhost:5000/
  GET http://localhost:5000/hello
  GET http://localhost:5000/users
  GET http://localhost:5000/users/1
  GET http://localhost:5000/search?name=Alice
  POST http://localhost:5000/users (with JSON body)
"""
print(run_instructions)


# ==============================================================================
# 11. MAIN BLOCK - Run the server
# ==============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 STARTING FLASK SERVER")
    print("=" * 80)
    print("""
The server is now running on http://localhost:5000

📌 IMPORTANT:
1. Keep this terminal window open
2. Open a NEW terminal for Postman testing
3. Press CTRL+C to stop the server

🧪 TEST WITH POSTMAN:
- Open Postman
- Try: GET http://localhost:5000/
- Then try: GET http://localhost:5000/hello
- Then try: GET http://localhost:5000/users

📚 Check DAY3_INSTRUCTIONS.md for detailed testing guide
""")

    # Run the Flask app
    # debug=True means:
    # - Auto-reload when you change code
    # - Better error messages
    app.run(
        host='localhost',      # Localhost only
        port=5000,             # Port number
        debug=True             # Auto-reload on changes
    )
