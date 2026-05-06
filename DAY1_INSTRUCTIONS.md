# 🎓 DAY 1: PYTHON BASICS FOR API DEVELOPMENT

## 📋 What You'll Learn

- **Variables & Data Types** - How to store information
- **Lists** - Store multiple items
- **Dictionaries** - Key-value pairs (used in JSON/APIs)
- **Functions** - Reusable code blocks
- **Conditionals** - Make decisions in code
- **Loops** - Repeat actions
- **Practical Example** - Create API-like responses

---

## 🚀 Step 1: Set Up Your Environment

### Check Python Installation

Open Terminal and run:

```bash
python3 --version
```

You should see Python 3.8 or higher. If not, install it from [python.org](https://www.python.org)

### Navigate to Your Project Folder

```bash
cd /Users/sudipphuyal/Developments/Learn/API
```

---

## 🏃 Step 2: Run the Python Basics Script

```bash
python3 day1_python_basics.py
```

**What you'll see:**

- Various Python concepts with output
- Clear explanations of each concept
- Practical examples you'll use in APIs

---

## 📚 Understanding the Code

### 1️⃣ Variables & Data Types

```python
name = "Alice"           # String
age = 25                 # Integer
height = 5.7             # Float
is_active = True         # Boolean
phone = None             # No value
```

**Why?** APIs receive data in these types through JSON.

### 2️⃣ Lists

```python
fruits = ["apple", "banana", "orange"]
fruits.append("mango")          # Add item
fruits.remove("banana")         # Remove item
print(fruits[0])                # Access first item
```

**Why?** When API returns "all users", it's a list!

### 3️⃣ Dictionaries (Most Important!)

```python
user = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}
print(user["name"])             # Access value by key
user["phone"] = "555-1234"      # Add new key
```

**Why?** This is exactly how JSON works in APIs! When Postman sends data, it's a dictionary.

### 4️⃣ Functions

```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Bob")           # Call function
```

**Why?** Every API endpoint is a function that receives a request and returns a response.

### 5️⃣ Conditionals

```python
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

**Why?** Validate API requests and make decisions.

### 6️⃣ Loops

```python
for fruit in fruits:
    print(fruit)
```

**Why?** Process lists of data from databases or requests.

### 7️⃣ Lists of Dictionaries

```python
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]
```

**Why?** This is exactly what APIs return to Postman!

---

## 💡 Key Takeaways

| Concept              | API Example                                |
| -------------------- | ------------------------------------------ |
| Dictionary           | `{"id": 1, "name": "Alice"}` (single user) |
| List of Dictionaries | `[{...}, {...}]` (all users)               |
| Function             | Endpoint handler that processes requests   |
| String               | User name, email                           |
| Integer              | User ID                                    |
| Boolean              | is_active, is_admin                        |

---

## 🎯 Practice Exercise

Try these modifications to `day1_python_basics.py`:

1. **Add a new user to the users list**

   ```python
   users.append({"id": 4, "name": "Eve", "email": "eve@example.com"})
   ```

2. **Create a function that finds user by ID**

   ```python
   def find_user(user_id):
       for user in users:
           if user["id"] == user_id:
               return user
       return None
   ```

3. **Loop through users and print their emails**
   ```python
   for user in users:
       print(user["email"])
   ```

---

## ✅ You're Ready for Day 2!

**Next Steps:**

- Run the script multiple times
- Modify the code and see what happens
- Try to break it and fix it (learning!)
- When comfortable, we'll move to Day 2: HTTP Concepts

**Questions to think about:**

- How would you store a list of tasks?
- How would a user request look as a dictionary?
- How would you validate if an email is provided?

---

## 🎓 Resources (Optional Further Learning)

- [Python Official Documentation](https://docs.python.org/3/)
- [W3Schools Python Tutorial](https://www.w3schools.com/python/)
- [Real Python - Python Dictionaries](https://realpython.com/python-dicts/)

---

**Happy Learning! 🚀**
