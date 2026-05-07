"""
DAY 5: MASTERING POST REQUESTS & DATA VALIDATION
================================================
Learn how to receive data from Postman, validate it, and handle errors.
POST is where real data creation happens!
"""

from flask import Flask, jsonify, request
import json
from datetime import datetime

# Create Flask app
app = Flask(__name__)

print("=" * 80)
print("DAY 5: MASTERING POST REQUESTS & DATA VALIDATION")
print("=" * 80)


# ==============================================================================
# DATABASE (Fake database for learning)
# ==============================================================================

users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 30},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 28}
}

todos_db = {
    1: {"id": 1, "title": "Learn Python", "description": "Complete Day 1-5", "completed": True},
    2: {"id": 2, "title": "Build API", "description": "Create Flask API", "completed": False}
}


# ==============================================================================
# 1. VALIDATION FUNCTIONS
# ==============================================================================
print("\n" + "=" * 80)
print("1. VALIDATION FUNCTIONS - Check if data is valid")
print("=" * 80)


def validate_email(email):
    """Check if email has @ symbol (basic validation)"""
    if not email or '@' not in email:
        return False
    return True


def validate_user_data(data):
    """
    Validate user creation data.
    Returns: (is_valid: bool, error_message: str)
    """
    if not data:
        return False, "Request body cannot be empty"

    # Check required fields
    if 'name' not in data:
        return False, "Field 'name' is required"

    if 'email' not in data:
        return False, "Field 'email' is required"

    if 'age' not in data:
        return False, "Field 'age' is required"

    # Validate data types
    if not isinstance(data['name'], str):
        return False, "Field 'name' must be a string"

    if not isinstance(data['email'], str):
        return False, "Field 'email' must be a string"

    if not isinstance(data['age'], int):
        return False, "Field 'age' must be an integer"

    # Validate field values
    if len(data['name'].strip()) < 2:
        return False, "Name must be at least 2 characters"

    if not validate_email(data['email']):
        return False, "Invalid email format (must contain @)"

    if data['age'] < 1 or data['age'] > 150:
        return False, "Age must be between 1 and 150"

    # Check if email already exists
    for user in users_db.values():
        if user['email'] == data['email']:
            return False, f"Email '{data['email']}' already exists"

    return True, None


def validate_todo_data(data):
    """Validate todo creation data"""
    if not data:
        return False, "Request body cannot be empty"

    if 'title' not in data:
        return False, "Field 'title' is required"

    if not isinstance(data['title'], str):
        return False, "Field 'title' must be a string"

    if len(data['title'].strip()) < 3:
        return False, "Title must be at least 3 characters"

    return True, None


print("""
Validation functions check:
✓ Required fields present
✓ Data types correct
✓ Values in valid range
✓ No duplicates
✓ Format correct (email, etc.)

These functions return (is_valid, error_message)
""")


# ==============================================================================
# 2. BASIC POST ENDPOINT - Create user
# ==============================================================================
print("\n" + "=" * 80)
print("2. BASIC POST - Create new user with validation")
print("=" * 80)


@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user with full validation.

    Expected JSON:
    {
        "name": "Diana",
        "email": "diana@example.com",
        "age": 26
    }
    """
    # Get JSON from request
    data = request.get_json()

    # Validate using function
    is_valid, error_message = validate_user_data(data)

    if not is_valid:
        return jsonify({
            "success": False,
            "error": error_message,
            "status": 400
        }), 400

    # Create new user
    new_id = max(users_db.keys()) + 1 if users_db else 1
    new_user = {
        "id": new_id,
        "name": data['name'].strip(),
        "email": data['email'].strip(),
        "age": data['age']
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

SUCCESS CASE:
{
  "name": "Diana",
  "email": "diana@example.com",
  "age": 26
}
Response (201 Created):
{
  "success": true,
  "message": "User created successfully",
  "data": {"id": 4, "name": "Diana", "email": "diana@example.com", "age": 26}
}

ERROR CASE - Missing field:
{
  "name": "Eve"
}
Response (400):
{
  "success": false,
  "error": "Field 'email' is required",
  "status": 400
}

ERROR CASE - Invalid email:
{
  "name": "Frank",
  "email": "notanemail",
  "age": 30
}
Response (400):
{
  "success": false,
  "error": "Invalid email format (must contain @)",
  "status": 400
}

ERROR CASE - Age out of range:
{
  "name": "Grace",
  "email": "grace@example.com",
  "age": 200
}
Response (400):
{
  "success": false,
  "error": "Age must be between 1 and 150",
  "status": 400
}

ERROR CASE - Duplicate email:
{
  "name": "Alice2",
  "email": "alice@example.com",
  "age": 30
}
Response (400):
{
  "success": false,
  "error": "Email 'alice@example.com' already exists",
  "status": 400
}
""")


# ==============================================================================
# 3. PUT ENDPOINT - Update user
# ==============================================================================
print("\n" + "=" * 80)
print("3. PUT ENDPOINT - Update existing user")
print("=" * 80)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user.
    Can update: name, email, age
    """
    # Check if user exists
    if user_id not in users_db:
        return jsonify({
            "success": False,
            "error": f"User {user_id} not found",
            "status": 404
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body cannot be empty",
            "status": 400
        }), 400

    user = users_db[user_id]

    # Update only provided fields
    if 'name' in data:
        if not isinstance(data['name'], str) or len(data['name'].strip()) < 2:
            return jsonify({
                "success": False,
                "error": "Name must be a string with at least 2 characters",
                "status": 400
            }), 400
        user['name'] = data['name'].strip()

    if 'email' in data:
        if not isinstance(data['email'], str) or not validate_email(data['email']):
            return jsonify({
                "success": False,
                "error": "Invalid email format",
                "status": 400
            }), 400

        # Check if email exists for another user
        for uid, u in users_db.items():
            if uid != user_id and u['email'] == data['email']:
                return jsonify({
                    "success": False,
                    "error": "Email already exists",
                    "status": 400
                }), 400

        user['email'] = data['email'].strip()

    if 'age' in data:
        if not isinstance(data['age'], int) or data['age'] < 1 or data['age'] > 150:
            return jsonify({
                "success": False,
                "error": "Age must be an integer between 1 and 150",
                "status": 400
            }), 400
        user['age'] = data['age']

    return jsonify({
        "success": True,
        "message": "User updated successfully",
        "data": user
    }), 200


print("""
In Postman:
- Method: PUT
- URL: http://localhost:5000/users/1
- Headers: Content-Type: application/json
- Body (raw JSON):

EXAMPLE 1 - Update name only:
{
  "name": "Alice Smith"
}
Response (200):
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "age": 25
  }
}

EXAMPLE 2 - Update multiple fields:
{
  "name": "Alice J",
  "age": 26
}
Response (200): User with updated fields

EXAMPLE 3 - Update non-existent user:
- URL: http://localhost:5000/users/999
Response (404):
{
  "success": false,
  "error": "User 999 not found",
  "status": 404
}
""")


# ==============================================================================
# 4. DELETE ENDPOINT - Remove user
# ==============================================================================
print("\n" + "=" * 80)
print("4. DELETE ENDPOINT - Remove user")
print("=" * 80)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID"""
    if user_id not in users_db:
        return jsonify({
            "success": False,
            "error": f"User {user_id} not found",
            "status": 404
        }), 404

    deleted_user = users_db.pop(user_id)

    return jsonify({
        "success": True,
        "message": "User deleted successfully",
        "data": deleted_user
    }), 200


print("""
In Postman:
- Method: DELETE
- URL: http://localhost:5000/users/3
- No body needed

SUCCESS - User found and deleted:
Response (200):
{
  "success": true,
  "message": "User deleted successfully",
  "data": {"id": 3, "name": "Charlie", ...}
}

ERROR - User not found:
- URL: http://localhost:5000/users/999
Response (404):
{
  "success": false,
  "error": "User 999 not found",
  "status": 404
}
""")


# ==============================================================================
# 5. BATCH OPERATIONS - Process multiple items
# ==============================================================================
print("\n" + "=" * 80)
print("5. BATCH OPERATIONS - Create multiple items")
print("=" * 80)


@app.route('/users/batch', methods=['POST'])
def create_users_batch():
    """
    Create multiple users in one request.

    Expected JSON:
    {
        "users": [
            {"name": "User1", "email": "user1@example.com", "age": 25},
            {"name": "User2", "email": "user2@example.com", "age": 30}
        ]
    }
    """
    data = request.get_json()

    if not data or 'users' not in data:
        return jsonify({
            "success": False,
            "error": "Expected 'users' array in body",
            "status": 400
        }), 400

    if not isinstance(data['users'], list):
        return jsonify({
            "success": False,
            "error": "Field 'users' must be an array",
            "status": 400
        }), 400

    created_users = []
    errors = []

    # Process each user
    for idx, user_data in enumerate(data['users']):
        is_valid, error_msg = validate_user_data(user_data)

        if not is_valid:
            errors.append({
                "index": idx,
                "error": error_msg,
                "data": user_data
            })
            continue

        # Create user
        new_id = max(users_db.keys()) + 1 if users_db else 1
        new_user = {
            "id": new_id,
            "name": user_data['name'].strip(),
            "email": user_data['email'].strip(),
            "age": user_data['age']
        }
        users_db[new_id] = new_user
        created_users.append(new_user)

    return jsonify({
        "success": len(errors) == 0,
        "created_count": len(created_users),
        "error_count": len(errors),
        "created_users": created_users,
        "errors": errors
    }), 201 if len(errors) == 0 else 207


print("""
In Postman:
- Method: POST
- URL: http://localhost:5000/users/batch
- Body (raw JSON):

{
  "users": [
    {"name": "User1", "email": "user1@example.com", "age": 25},
    {"name": "User2", "email": "user2@example.com", "age": 30}
  ]
}

Response (201 - all successful):
{
  "success": true,
  "created_count": 2,
  "error_count": 0,
  "created_users": [...],
  "errors": []
}

Response (207 - partial success):
{
  "success": false,
  "created_count": 1,
  "error_count": 1,
  "created_users": [valid users...],
  "errors": [
    {
      "index": 1,
      "error": "Invalid email format",
      "data": {...}
    }
  ]
}
""")


# ==============================================================================
# 6. TODOS ENDPOINT - POST
# ==============================================================================
print("\n" + "=" * 80)
print("6. CREATE TODO - Another POST example")
print("=" * 80)


@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo item"""
    data = request.get_json()

    is_valid, error_msg = validate_todo_data(data)
    if not is_valid:
        return jsonify({
            "success": False,
            "error": error_msg,
            "status": 400
        }), 400

    new_id = max(todos_db.keys()) + 1 if todos_db else 1
    new_todo = {
        "id": new_id,
        "title": data['title'].strip(),
        "description": data.get('description', '').strip(),
        "completed": False
    }
    todos_db[new_id] = new_todo

    return jsonify({
        "success": True,
        "message": "Todo created",
        "data": new_todo
    }), 201


print("""
In Postman:
- Method: POST
- URL: http://localhost:5000/todos
- Body:

{
  "title": "Learn Flask",
  "description": "Master POST requests"
}

Response (201):
{
  "success": true,
  "message": "Todo created",
  "data": {
    "id": 3,
    "title": "Learn Flask",
    "description": "Master POST requests",
    "completed": false
  }
}
""")


# ==============================================================================
# 7. GET ENDPOINTS (Supporting endpoints)
# ==============================================================================
print("\n" + "=" * 80)
print("7. GET ENDPOINTS - View created data")
print("=" * 80)


@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    return jsonify({
        "success": True,
        "count": len(users_db),
        "data": list(users_db.values())
    }), 200


@app.route('/todos', methods=['GET'])
def get_all_todos():
    """Get all todos"""
    return jsonify({
        "success": True,
        "count": len(todos_db),
        "data": list(todos_db.values())
    }), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user"""
    if user_id in users_db:
        return jsonify({
            "success": True,
            "data": users_db[user_id]
        }), 200
    return jsonify({
        "success": False,
        "error": f"User {user_id} not found"
    }), 404


@app.route('/', methods=['GET'])
def home():
    """API status and endpoints"""
    return jsonify({
        "status": "API Running ✅",
        "version": "5.0",
        "endpoints": {
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID",
            "POST /users": "Create user",
            "POST /users/batch": "Create multiple users",
            "PUT /users/<id>": "Update user",
            "DELETE /users/<id>": "Delete user",
            "GET /todos": "Get all todos",
            "POST /todos": "Create todo"
        }
    }), 200


# ==============================================================================
# 8. ERROR HANDLING
# ==============================================================================
print("\n" + "=" * 80)
print("8. COMPLETE ERROR HANDLING")
print("=" * 80)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "status": 404
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed"""
    return jsonify({
        "success": False,
        "error": "Method not allowed for this endpoint",
        "status": 405
    }), 405


@app.errorhandler(500)
def server_error(error):
    """Handle server errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "status": 500
    }), 500


print("""
Error responses examples:

404 - Endpoint doesn't exist:
{
  "success": false,
  "error": "Endpoint not found",
  "status": 404
}

405 - Wrong HTTP method:
{
  "success": false,
  "error": "Method not allowed for this endpoint",
  "status": 405
}

500 - Server error:
{
  "success": false,
  "error": "Internal server error",
  "status": 500
}
""")


# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("SUMMARY OF DAY 5")
print("=" * 80)

summary = """
╔════════════════════════════════════════════════════════════════════════╗
║                   API ENDPOINTS REFERENCE                             ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  GET /                                                                 ║
║    → API status & available endpoints                                 ║
║                                                                        ║
║  GET /users                                                            ║
║    → Get all users                                                     ║
║                                                                        ║
║  GET /users/<id>                                                       ║
║    → Get specific user (404 if not found)                             ║
║                                                                        ║
║  POST /users ⭐ NEW                                                    ║
║    → Create new user with validation                                  ║
║    → 201 Created on success                                           ║
║    → 400 Bad Request if validation fails                              ║
║                                                                        ║
║  POST /users/batch ⭐ NEW                                              ║
║    → Create multiple users at once                                    ║
║    → Returns created_count, error_count, errors                      ║
║                                                                        ║
║  PUT /users/<id> ⭐ NEW                                                ║
║    → Update existing user                                             ║
║    → Validates each field separately                                  ║
║    → 200 OK or 400/404 errors                                         ║
║                                                                        ║
║  DELETE /users/<id> ⭐ NEW                                             ║
║    → Delete user                                                       ║
║    → Returns deleted user data                                        ║
║                                                                        ║
║  GET /todos                                                            ║
║    → Get all todos                                                     ║
║                                                                        ║
║  POST /todos ⭐ NEW                                                    ║
║    → Create new todo                                                  ║
║    → Validates title (required, ≥3 chars)                            ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
"""
print(summary)


# ==============================================================================
# RUN SERVER
# ==============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 STARTING FLASK SERVER - DAY 5")
    print("=" * 80)
    print("""
The server is running on http://localhost:5000

📚 Test these in Postman:
  1. POST /users (create user)
  2. GET /users (see all users)
  3. PUT /users/1 (update user)
  4. DELETE /users/3 (delete user)
  5. POST /users/batch (multiple users)
  6. POST /todos (create todo)

⚠️  Keep terminal open - Press CTRL+C to stop
""")

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
