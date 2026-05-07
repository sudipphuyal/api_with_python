# 🎓 DAY 6: DATABASE INTEGRATION WITH SQLITE

## 📋 What You'll Learn

- **What is SQLite?** - Lightweight SQL database
- **Create database tables** - Schema design
- **CRUD with database** - Create, Read, Update, Delete operations
- **Data persistence** - Data survives server restarts
- **Foreign keys** - Relationships between tables
- **Database queries** - SELECT, INSERT, UPDATE, DELETE
- **Connection handling** - Safe database access
- **Validation** - Prevent duplicate emails, etc.

---

## 🎯 Key Difference from Day 5

| Aspect      | Day 5 (In-Memory) | Day 6 (Database)     |
| ----------- | ----------------- | -------------------- |
| Storage     | Python dictionary | SQLite database file |
| Persistence | Lost on restart   | Saved permanently    |
| Scaling     | Limited           | Can handle thousands |
| Sharing     | Single instance   | Multiple clients     |
| Real-world  | Learning          | Production-like      |

---

## 🚀 Step 1: Understand SQLite

### What is SQLite?

- **SQL Database** - Uses SQL queries (SELECT, INSERT, UPDATE, DELETE)
- **Lightweight** - Stored as single file (api.db)
- **No setup** - Built into Python, no server needed
- **Perfect for learning** - Easy to understand and debug

### Database vs Dictionary

**Dictionary (Day 5):**

```python
users = {
    1: {"name": "Alice"},
    2: {"name": "Bob"}
}
# Lost when program exits!
```

**Database (Day 6):**

```
api.db (file on disk)
   ↓
   USERS table
   ┌────┬───────┐
   │ id │ name  │
   ├────┼───────┤
   │ 1  │ Alice │
   │ 2  │ Bob   │
   └────┴───────┘
# Permanent, survives restart!
```

---

## 🗂️ Step 2: Database Structure

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing ID
    name TEXT NOT NULL,                    -- Required text
    email TEXT NOT NULL UNIQUE,            -- Required, no duplicates
    age INTEGER NOT NULL,                  -- Required integer
    created_at TIMESTAMP DEFAULT ...,      -- Auto-set timestamp
    updated_at TIMESTAMP DEFAULT ...       -- Auto-set timestamp
)
```

### Todos Table

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT 0,
    user_id INTEGER,                       -- Links to users
    created_at TIMESTAMP DEFAULT ...,
    updated_at TIMESTAMP DEFAULT ...,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### Relationship

```
One User → Many Todos
┌────────┬──────┐
│ users  │ id   │──────┐
│ id=1   │ name │      │
│ Alice  │ ...  │      │
└────────┴──────┘      │
                       │ Foreign Key
                       ↓
            ┌──────────────────┐
            │ todos            │
            │ id=1, user_id=1  │
            │ id=2, user_id=1  │
            │ id=3, user_id=2  │
            └──────────────────┘
```

---

## 🏃 Step 3: Run the Server

```bash
cd /Users/sudipphuyal/Developments/Learn/API
source venv/bin/activate
python3 day6_database_sqlite.py
```

**You'll see:**

```
✅ Database initialized at: api.db
📦 Creating sample data...

* Running on http://127.0.0.1:5000
```

---

## 🧪 Step 4: Testing with Postman

### Test 1: Get All Users (from database) ✅

```
Method: GET
URL: http://localhost:5000/users
```

**Response (200):**

```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com",
      "age": 25,
      "created_at": "2026-05-07 10:30:45...",
      "updated_at": "2026-05-07 10:30:45..."
    },
    {"id": 2, "name": "Bob", ...},
    {"id": 3, "name": "Charlie", ...}
  ]
}
```

**Notice:**

- ✅ created_at & updated_at timestamps
- ✅ Data from database, not hardcoded

---

### Test 2: Get Specific User

```
Method: GET
URL: http://localhost:5000/users/1
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "created_at": "...",
    "updated_at": "..."
  }
}
```

---

### Test 3: Create User (Stored in Database) 📝

```
Method: POST
URL: http://localhost:5000/users
Body (raw JSON):
{
  "name": "Diana",
  "email": "diana@example.com",
  "age": 26
}
```

**Response (201 Created):**

```json
{
  "success": true,
  "data": {
    "id": 4,
    "name": "Diana",
    "email": "diana@example.com",
    "age": 26,
    "created_at": "2026-05-07 11:15:22",
    "updated_at": "2026-05-07 11:15:22"
  }
}
```

**Important:** Diana now exists in api.db!

---

### Test 4: Update User in Database 🔄

```
Method: PUT
URL: http://localhost:5000/users/1
Body:
{
  "name": "Alice Smith",
  "age": 26
}
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "age": 26,
    "created_at": "2026-05-07 10:30:45",
    "updated_at": "2026-05-07 11:20:15"  ← Updated timestamp!
  }
}
```

---

### Test 5: Delete User from Database 🗑️

```
Method: DELETE
URL: http://localhost:5000/users/3
```

**Response (200):**

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

**Verify:** GET /users now shows only 2 users!

---

### Test 6: Duplicate Email Validation

```
Method: POST
URL: http://localhost:5000/users
Body:
{
  "name": "Alice2",
  "email": "alice@example.com",  ← Already exists!
  "age": 30
}
```

**Response (400):**

```json
{
  "success": false,
  "error": "Email 'alice@example.com' already exists"
}
```

**Database prevents duplicates!**

---

### Test 7: Create Todo

```
Method: POST
URL: http://localhost:5000/todos
Body:
{
  "title": "Master SQLite",
  "description": "Learn database operations",
  "completed": false,
  "user_id": 1
}
```

**Response (201):**

```json
{
  "success": true,
  "data": {
    "id": 4,
    "title": "Master SQLite",
    "description": "Learn database operations",
    "completed": 0,
    "user_id": 1,
    "created_at": "...",
    "updated_at": "..."
  }
}
```

**Note:** user_id links this todo to Alice (user_id=1)

---

### Test 8: Get All Todos

```
Method: GET
URL: http://localhost:5000/todos
```

**Response:**

```json
{
  "success": true,
  "count": 4,
  "data": [
    {"id": 1, "title": "Learn Python", "user_id": 1, ...},
    {"id": 2, "title": "Build API", "user_id": 1, ...},
    {"id": 3, "title": "Learn Database", "user_id": 2, ...},
    {"id": 4, "title": "Master SQLite", "user_id": 1, ...}
  ]
}
```

---

## 📚 Understanding the Code

### Database Connection

```python
def get_db_connection():
    conn = sqlite3.connect('api.db')
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    return conn
```

### SELECT Query (Read)

```python
cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
row = cursor.fetchone()  # Get one row
# or
rows = cursor.fetchall()  # Get all rows
```

### INSERT Query (Create)

```python
cursor.execute('''
    INSERT INTO users (name, email, age)
    VALUES (?, ?, ?)
''', (name, email, age))

user_id = cursor.lastrowid  # Get auto-generated ID
conn.commit()  # Save to database
```

### UPDATE Query (Update)

```python
cursor.execute('''
    UPDATE users SET name = ?, age = ?
    WHERE id = ?
''', (name, age, user_id))

conn.commit()  # Save changes
```

### DELETE Query (Delete)

```python
cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
conn.commit()  # Permanent deletion
```

---

## 🔄 The SQL Query Pattern

```
┌─────────────────────────────────────────┐
│  SQL Query Construction                 │
├─────────────────────────────────────────┤
│                                         │
│  1. cursor.execute("SQL", (params,))   │
│  2. conn.commit()  (for changes)       │
│  3. cursor.fetchone() / fetchall()     │
│  4. conn.close()                       │
│                                         │
└─────────────────────────────────────────┘
```

---

## 💾 Data Persistence Example

### Before Restart

```bash
$ python3 day6_database_sqlite.py
GET /users → Returns Alice, Bob, Charlie
POST /users → Creates Diana
GET /users → Returns Alice, Bob, Charlie, Diana
CTRL+C (stop server)
```

### After Restart

```bash
$ python3 day6_database_sqlite.py
GET /users → Still returns Alice, Bob, Charlie, Diana ✅
✓ Diana PERSISTS! (stored in api.db)
✓ Database file survives restart
```

**This is the HUGE difference from Day 5!**

---

## 📊 SQL Commands Reference

| Command  | Purpose       | Example                                  |
| -------- | ------------- | ---------------------------------------- |
| SELECT   | Read data     | `SELECT * FROM users WHERE age > 25`     |
| INSERT   | Create data   | `INSERT INTO users VALUES (...)`         |
| UPDATE   | Modify data   | `UPDATE users SET age = 26 WHERE id = 1` |
| DELETE   | Remove data   | `DELETE FROM users WHERE id = 1`         |
| WHERE    | Filter        | `WHERE email = 'alice@example.com'`      |
| ORDER BY | Sort          | `ORDER BY id DESC`                       |
| LIMIT    | Limit results | `LIMIT 10`                               |

---

## 🎯 Complete Testing Checklist

- [ ] GET /users → See sample data from database
- [ ] GET /users/1 → See timestamps
- [ ] POST /users → Create new user (checks email duplicate)
- [ ] GET /users → New user appears in list
- [ ] PUT /users/1 → Update user
- [ ] GET /users/1 → See updated_at changed
- [ ] DELETE /users/3 → Delete from database
- [ ] GET /users → Verify user is gone
- [ ] POST /todos → Create todo with user_id
- [ ] GET /todos → See all todos
- [ ] CTRL+C to stop server
- [ ] python3 day6_database_sqlite.py (restart)
- [ ] GET /users → Data still there! ✅
- [ ] GET /todos → Todos still there! ✅

---

## 🗄️ SQLite Basics

### Open Database in Terminal

```bash
# Open SQLite command line
sqlite3 api.db

# See all tables
.tables

# View users table
SELECT * FROM users;

# View todos table
SELECT * FROM todos;

# Exit
.exit
```

### Example Queries

```sql
-- Count users
SELECT COUNT(*) FROM users;

-- Find users by age
SELECT * FROM users WHERE age > 25;

-- Get todos for user 1
SELECT * FROM todos WHERE user_id = 1;

-- Sort by created_at
SELECT * FROM todos ORDER BY created_at DESC;

-- Join tables (advanced)
SELECT u.name, t.title
FROM users u
JOIN todos t ON u.id = t.user_id;
```

---

## 🔑 Key Concepts

### 1. Tables

Structured data with rows and columns

### 2. Primary Key

Unique ID for each row (id field)

### 3. Foreign Key

Links to row in another table (user_id)

### 4. Constraints

- NOT NULL: Field required
- UNIQUE: No duplicates
- DEFAULT: Default value

### 5. CRUD Operations

- Create: INSERT
- Read: SELECT
- Update: UPDATE
- Delete: DELETE

### 6. Timestamps

- created_at: When record created
- updated_at: When record last updated

---

## 📝 Common Operations

### Get all users

```python
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()
```

### Find user by email

```python
cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
user = cursor.fetchone()
```

### Create user

```python
cursor.execute(
    'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
    (name, email, age)
)
user_id = cursor.lastrowid
```

### Update user

```python
cursor.execute(
    'UPDATE users SET name = ?, age = ? WHERE id = ?',
    (name, age, user_id)
)
```

### Delete user

```python
cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
```

---

## 💡 Pro Tips

### Tip 1: Always Use Parameterized Queries

```python
# ✅ SAFE - Prevents SQL injection
cursor.execute('SELECT * FROM users WHERE email = ?', (email,))

# ❌ UNSAFE - Never do this!
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### Tip 2: Always Commit Changes

```python
cursor.execute(...)
conn.commit()  # Don't forget!
```

### Tip 3: Close Connections

```python
conn.close()  # Free up resources
```

### Tip 4: Handle Errors

```python
try:
    cursor.execute(...)
    conn.commit()
except sqlite3.Error as e:
    return error_response
```

### Tip 5: Use Foreign Keys

```python
# Link todos to users
user_id = data.get('user_id')
cursor.execute(
    'INSERT INTO todos (..., user_id) VALUES (..., ?)',
    (..., user_id)
)
```

---

## 🎓 Practice Assignments

### Task 1: Add Search by Name

```python
@app.route('/users/search/<name>')
def search_users(name):
    # Find users by name containing search term
    # SELECT * FROM users WHERE name LIKE '%name%'
```

### Task 2: Get User's Todos

```python
@app.route('/users/<int:user_id>/todos')
def get_user_todos(user_id):
    # GET all todos for specific user
    # SELECT * FROM todos WHERE user_id = ?
```

### Task 3: Mark Todo Complete

```python
# PUT /todos/<id>
# Update completed = 1
```

### Task 4: Delete All User's Todos

```python
# DELETE from todos where user_id = ?
```

### Task 5: Statistics Endpoint

```python
@app.route('/stats')
# Return: total users, total todos, completed todos, etc.
```

---

## 🚨 Troubleshooting

### Error: "database is locked"

```
Cause: Another process accessing database
Solution: Close other terminals, restart server
```

### Error: "no such table"

```
Cause: Table never created
Solution: Delete api.db and restart (creates fresh database)
```

### Error: "UNIQUE constraint failed"

```
Cause: Trying to insert duplicate email
Solution: Validation works! Check error response
```

### Data won't persist

```
Cause: Forgot conn.commit()
Solution: Always commit after INSERT/UPDATE/DELETE
```

---

## 🎉 Success Indicators

You've mastered Day 6 when:

- ✅ SQLite database file (api.db) exists
- ✅ Sample data loads on startup
- ✅ GET endpoints query from database
- ✅ POST creates records in database
- ✅ PUT updates database records
- ✅ DELETE removes from database
- ✅ Email uniqueness works
- ✅ Data persists after restart
- ✅ Timestamps auto-update
- ✅ Foreign keys work (user_id in todos)

---

## 📌 Files

- [day6_database_sqlite.py](day6_database_sqlite.py) - Flask app with SQLite
- api.db - Your database file (created automatically)

---

## 🚀 What's Next?

**Day 7-8:** Advanced Database Features

- Relationships and joins
- Filtering and sorting
- Pagination
- Search functionality
- Authentication

**Keep building! You're learning real-world API development! 🌟**
