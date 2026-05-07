"""
DAY 6: DATABASE INTEGRATION WITH SQLITE
=======================================
Move from in-memory data to persistent database storage.
SQLite is a lightweight SQL database - perfect for learning!
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Database path
DB_PATH = 'api.db'

print("=" * 80)
print("DAY 6: DATABASE INTEGRATION WITH SQLITE")
print("=" * 80)


# ==============================================================================
# 1. DATABASE SETUP & INITIALIZATION
# ==============================================================================
print("\n" + "=" * 80)
print("1. DATABASE SETUP")
print("=" * 80)


def init_database():
    """
    Create database tables if they don't exist.
    Called once when app starts.
    """
    # Check if database already exists
    db_exists = os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create todos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Insert sample data if database is new
    if not db_exists:
        print("📦 Creating sample data...")
        cursor.execute('''
            INSERT INTO users (name, email, age)
            VALUES ('Alice', 'alice@example.com', 25),
                   ('Bob', 'bob@example.com', 30),
                   ('Charlie', 'charlie@example.com', 28)
        ''')

        cursor.execute('''
            INSERT INTO todos (title, description, completed, user_id)
            VALUES ('Learn Python', 'Complete Day 1-5', 1, 1),
                   ('Build API', 'Create Flask API', 0, 1),
                   ('Learn Database', 'Complete Day 6', 0, 2)
        ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized at:", DB_PATH)


print("""
SQLite Database created with two tables:

USERS table:
┌────┬─────────┬──────────────────┬─────┬───────────┬───────────┐
│ id │  name   │      email       │ age │ created_at│ updated_at│
├────┼─────────┼──────────────────┼─────┼───────────┼───────────┤
│ 1  │ Alice   │ alice@...        │ 25  │ timestamp │ timestamp │
│ 2  │ Bob     │ bob@...          │ 30  │ timestamp │ timestamp │
└────┴─────────┴──────────────────┴─────┴───────────┴───────────┘

TODOS table:
┌────┬──────────────┬──────────────┬───────────┬─────────┬───────────┐
│ id │    title     │ description  │ completed │ user_id │ created_at│
├────┼──────────────┼──────────────┼───────────┼─────────┼───────────┤
│ 1  │ Learn Python │ Complete ... │ 1 (True)  │ 1       │ timestamp │
│ 2  │ Build API    │ Create Flask │ 0 (False) │ 1       │ timestamp │
└────┴──────────────┴──────────────┴───────────┴─────────┴───────────┘
""")

# Initialize database when app starts
init_database()


# ==============================================================================
# 2. HELPER FUNCTIONS FOR DATABASE
# ==============================================================================
print("\n" + "=" * 80)
print("2. DATABASE HELPER FUNCTIONS")
print("=" * 80)


def get_db_connection():
    """Create and return database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    if row is None:
        return None
    return dict(row)


def validate_email(email):
    """Check if email format is valid"""
    return email and '@' in email


def email_exists(email, exclude_user_id=None):
    """Check if email already exists in database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if exclude_user_id:
        cursor.execute('SELECT id FROM users WHERE email = ? AND id != ?',
                       (email, exclude_user_id))
    else:
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))

    result = cursor.fetchone() is not None
    conn.close()
    return result


print("""
Helper functions:
✓ get_db_connection() - Connect to database
✓ dict_from_row(row) - Convert database row to dictionary
✓ validate_email(email) - Check email format
✓ email_exists(email) - Check for duplicates
""")


# ==============================================================================
# 3. GET ENDPOINTS - Read from database
# ==============================================================================
print("\n" + "=" * 80)
print("3. GET ENDPOINTS - Query database")
print("=" * 80)


@app.route('/', methods=['GET'])
def home():
    """API status"""
    return jsonify({
        "status": "API Running ✅",
        "version": "6.0 - Database Edition",
        "database": "SQLite",
        "endpoints": {
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID",
            "POST /users": "Create user",
            "PUT /users/<id>": "Update user",
            "DELETE /users/<id>": "Delete user",
            "GET /todos": "Get all todos",
            "POST /todos": "Create todo",
            "PUT /todos/<id>": "Update todo",
            "DELETE /todos/<id>": "Delete todo"
        }
    }), 200


@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users from database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users ORDER BY id')
    rows = cursor.fetchall()
    users = [dict_from_row(row) for row in rows]

    conn.close()

    return jsonify({
        "success": True,
        "count": len(users),
        "data": users
    }), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({
            "success": False,
            "error": f"User {user_id} not found"
        }), 404

    return jsonify({
        "success": True,
        "data": dict_from_row(row)
    }), 200


@app.route('/todos', methods=['GET'])
def get_all_todos():
    """Get all todos from database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM todos ORDER BY id')
    rows = cursor.fetchall()
    todos = [dict_from_row(row) for row in rows]

    conn.close()

    return jsonify({
        "success": True,
        "count": len(todos),
        "data": todos
    }), 200


@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get specific todo by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({
            "success": False,
            "error": f"Todo {todo_id} not found"
        }), 404

    return jsonify({
        "success": True,
        "data": dict_from_row(row)
    }), 200


print("""
GET Endpoints:
✓ GET /users → All users from database
✓ GET /users/<id> → Specific user
✓ GET /todos → All todos from database
✓ GET /todos/<id> → Specific todo
""")


# ==============================================================================
# 4. POST ENDPOINTS - Create in database
# ==============================================================================
print("\n" + "=" * 80)
print("4. POST ENDPOINTS - Create new records")
print("=" * 80)


@app.route('/users', methods=['POST'])
def create_user():
    """Create new user in database"""
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({
            "success": False,
            "error": "Request body cannot be empty"
        }), 400

    # Check required fields
    if 'name' not in data or 'email' not in data or 'age' not in data:
        return jsonify({
            "success": False,
            "error": "Required fields: name, email, age"
        }), 400

    # Validate email
    if not validate_email(data['email']):
        return jsonify({
            "success": False,
            "error": "Invalid email format"
        }), 400

    # Check email not already exists
    if email_exists(data['email']):
        return jsonify({
            "success": False,
            "error": f"Email '{data['email']}' already exists"
        }), 400

    # Validate age
    if not isinstance(data['age'], int) or data['age'] < 1 or data['age'] > 150:
        return jsonify({
            "success": False,
            "error": "Age must be integer between 1 and 150"
        }), 400

    # Insert into database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (name, email, age)
            VALUES (?, ?, ?)
        ''', (data['name'].strip(), data['email'].strip(), data['age']))

        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        # Get created user
        return get_user(user_id)

    except sqlite3.IntegrityError as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 400


@app.route('/todos', methods=['POST'])
def create_todo():
    """Create new todo in database"""
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({
            "success": False,
            "error": "Field 'title' is required"
        }), 400

    if len(data['title'].strip()) < 3:
        return jsonify({
            "success": False,
            "error": "Title must be at least 3 characters"
        }), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        description = data.get('description', '').strip()
        completed = data.get('completed', False)
        user_id = data.get('user_id', None)

        cursor.execute('''
            INSERT INTO todos (title, description, completed, user_id)
            VALUES (?, ?, ?, ?)
        ''', (data['title'].strip(), description, completed, user_id))

        conn.commit()
        todo_id = cursor.lastrowid
        conn.close()

        return get_todo(todo_id)

    except sqlite3.Error as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 400


print("""
POST Endpoints:
✓ POST /users → Create user in database (auto-assigned ID)
✓ POST /todos → Create todo in database (auto-assigned ID)

Database features:
✓ Auto-incrementing IDs
✓ Timestamps (created_at, updated_at)
✓ Foreign keys (todos linked to users)
""")


# ==============================================================================
# 5. PUT ENDPOINTS - Update in database
# ==============================================================================
print("\n" + "=" * 80)
print("5. PUT ENDPOINTS - Update records")
print("=" * 80)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user in database"""
    # Check if user exists
    if not get_user(user_id)[0].json['data'] if get_user(user_id)[1] == 200 else False:
        # Let's do it simpler
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        if cursor.fetchone() is None:
            conn.close()
            return jsonify({
                "success": False,
                "error": f"User {user_id} not found"
            }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body cannot be empty"
        }), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build dynamic UPDATE query
        updates = []
        params = []

        if 'name' in data:
            updates.append('name = ?')
            params.append(data['name'].strip())

        if 'email' in data:
            if not validate_email(data['email']):
                conn.close()
                return jsonify({
                    "success": False,
                    "error": "Invalid email format"
                }), 400

            if email_exists(data['email'], exclude_user_id=user_id):
                conn.close()
                return jsonify({
                    "success": False,
                    "error": "Email already exists"
                }), 400

            updates.append('email = ?')
            params.append(data['email'].strip())

        if 'age' in data:
            if not isinstance(data['age'], int) or data['age'] < 1 or data['age'] > 150:
                conn.close()
                return jsonify({
                    "success": False,
                    "error": "Age must be integer between 1 and 150"
                }), 400

            updates.append('age = ?')
            params.append(data['age'])

        if updates:
            updates.append('updated_at = CURRENT_TIMESTAMP')
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            params.append(user_id)

            cursor.execute(query, params)
            conn.commit()

        conn.close()

        return get_user(user_id)

    except sqlite3.Error as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 400


@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update todo in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM todos WHERE id = ?', (todo_id,))

    if cursor.fetchone() is None:
        conn.close()
        return jsonify({
            "success": False,
            "error": f"Todo {todo_id} not found"
        }), 404

    data = request.get_json()

    if not data:
        conn.close()
        return jsonify({
            "success": False,
            "error": "Request body cannot be empty"
        }), 400

    try:
        updates = []
        params = []

        if 'title' in data:
            if len(data['title'].strip()) < 3:
                conn.close()
                return jsonify({
                    "success": False,
                    "error": "Title must be at least 3 characters"
                }), 400

            updates.append('title = ?')
            params.append(data['title'].strip())

        if 'description' in data:
            updates.append('description = ?')
            params.append(data['description'].strip())

        if 'completed' in data:
            updates.append('completed = ?')
            params.append(data['completed'])

        if updates:
            updates.append('updated_at = CURRENT_TIMESTAMP')
            query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
            params.append(todo_id)

            cursor.execute(query, params)
            conn.commit()

        conn.close()

        return get_todo(todo_id)

    except sqlite3.Error as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 400


print("""
PUT Endpoints:
✓ PUT /users/<id> → Update user fields
✓ PUT /todos/<id> → Update todo fields
✓ Partial updates (only update provided fields)
""")


# ==============================================================================
# 6. DELETE ENDPOINTS - Remove from database
# ==============================================================================
print("\n" + "=" * 80)
print("6. DELETE ENDPOINTS - Remove records")
print("=" * 80)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user from database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user before deletion
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return jsonify({
            "success": False,
            "error": f"User {user_id} not found"
        }), 404

    user_data = dict_from_row(row)

    try:
        # Delete user
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "User deleted successfully",
            "data": user_data
        }), 200

    except sqlite3.Error as e:
        conn.close()
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 400


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete todo from database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get todo before deletion
    cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return jsonify({
            "success": False,
            "error": f"Todo {todo_id} not found"
        }), 404

    todo_data = dict_from_row(row)

    try:
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Todo deleted successfully",
            "data": todo_data
        }), 200

    except sqlite3.Error as e:
        conn.close()
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 400


print("""
DELETE Endpoints:
✓ DELETE /users/<id> → Delete user permanently
✓ DELETE /todos/<id> → Delete todo permanently
✓ Returns deleted record before removal
""")


# ==============================================================================
# 7. ERROR HANDLERS
# ==============================================================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ==============================================================================
# 8. SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("SUMMARY OF DAY 6")
print("=" * 80)

summary = """
╔════════════════════════════════════════════════════════════════════════╗
║              DATABASE ARCHITECTURE & OPERATIONS                        ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  DATABASE: SQLite (api.db)                                            ║
║                                                                        ║
║  TABLES:                                                              ║
║    • users (id, name, email, age, created_at, updated_at)           ║
║    • todos (id, title, description, completed, user_id, ...)        ║
║                                                                        ║
║  RELATIONSHIPS:                                                       ║
║    • todos.user_id → users.id (Foreign Key)                          ║
║    • One user can have many todos                                    ║
║                                                                        ║
║  COMPLETE CRUD OPERATIONS:                                           ║
║    ✓ CREATE   (POST)   → Insert into database                        ║
║    ✓ READ     (GET)    → Query from database                         ║
║    ✓ UPDATE   (PUT)    → Modify in database                          ║
║    ✓ DELETE   (DELETE) → Remove from database                        ║
║                                                                        ║
║  KEY FEATURES:                                                       ║
║    ✓ Auto-incrementing IDs                                           ║
║    ✓ Timestamps (created_at, updated_at)                             ║
║    ✓ Unique constraints (email)                                      ║
║    ✓ Foreign keys (todos <-> users)                                  ║
║    ✓ Data persistence (survives server restart)                      ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
"""
print(summary)


# ==============================================================================
# RUN SERVER
# ==============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 STARTING FLASK SERVER - DAY 6 (Database Edition)")
    print("=" * 80)
    print(f"""
Database location: {DB_PATH}

📖 Sample Data Loaded:
   Users: Alice, Bob, Charlie
   Todos: Learn Python, Build API, Learn Database

🧪 Test with Postman:
   1. GET /users → See all users (from database!)
   2. POST /users → Create user (stored in database)
   3. GET /users/1 → User persists after restart
   4. PUT /users/1 → Update user in database
   5. DELETE /users/3 → Remove from database

⏹️  Press CTRL+C to stop
📚 File: day6_database_sqlite.py
""")

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
