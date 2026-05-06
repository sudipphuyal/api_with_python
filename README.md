# 🚀 API Development Learning Journey

**Goal:** Learn to build a local server that handles GET and POST requests using Python and test with Postman

**Level:** Beginner Python Developer

---

## 📅 Project Timeline

| Phase         | Duration | Focus                                                     |
| ------------- | -------- | --------------------------------------------------------- |
| **Day 1**     | 1-2 hrs  | Python Basics (Variables, Lists, Dictionaries, Functions) |
| **Day 2-3**   | 2-3 hrs  | HTTP Concepts & Request/Response Cycle                    |
| **Day 4-5**   | 2-3 hrs  | Setup Flask & Create First Endpoint                       |
| **Day 6-7**   | 2-3 hrs  | Master GET Requests                                       |
| **Day 8-10**  | 3-4 hrs  | Master POST Requests                                      |
| **Day 11-13** | 3-4 hrs  | Connect with Database (SQLite)                            |
| **Day 14-20** | 5-6 hrs  | Build Complete CRUD API                                   |
| **Day 21-25** | 3-4 hrs  | Best Practices & Error Handling                           |

---

## 📂 Project Structure

```
API/
├── day1_python_basics.py        # Current: Python fundamentals
├── DAY1_INSTRUCTIONS.md         # Current: Day 1 guide
├── day2_http_concepts.py        # Coming: HTTP methods
├── day3_setup_flask.py          # Coming: Flask app setup
├── app.py                       # Final: Main API server
├── models.py                    # Final: Database models
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

---

## 🎯 What You'll Build

### By Day 1: ✅ Understanding Python

- Variables, lists, dictionaries
- Functions and loops
- Data structures for APIs

### By Day 5: Server Framework

- A running Flask server on localhost:5000
- First GET endpoint working

### By Day 10: Handling Requests

- Process GET requests with parameters
- Handle POST requests from Postman
- Return JSON responses

### By Day 20: Full API

**Todo App API** with full CRUD operations:

- `GET /todos` - Get all todos
- `GET /todos/<id>` - Get specific todo
- `POST /todos` - Create new todo
- `PUT /todos/<id>` - Update todo
- `DELETE /todos/<id>` - Delete todo

---

## 🚀 Getting Started

### Currently: Day 1

1. Read [DAY1_INSTRUCTIONS.md](DAY1_INSTRUCTIONS.md)
2. Run: `python3 day1_python_basics.py`
3. Understand each concept
4. Try the practice exercises

---

## 📚 Key Technologies

- **Python 3.8+** - Backend language
- **Flask** - Web framework for creating API server
- **SQLite** - Simple database for data persistence
- **Postman** - Tool for testing API requests
- **JSON** - Data format for API communication

---

## 💻 Hardware Requirements

- Any laptop (Windows, Mac, or Linux)
- Terminal/Command Prompt access
- Postman (free app)
- Python installed

---

## 🔗 Testing Your API

Once you build your API, you'll test it with **Postman**:

1. **GET Request** - Send to `http://localhost:5000/todos`
2. **POST Request** - Send JSON data to `http://localhost:5000/todos`
3. **See Responses** - Your server responds with data

Example in Postman:

```
POST http://localhost:5000/todos
Body (JSON):
{
    "title": "Learn Python",
    "description": "Complete Day 1 exercises",
    "completed": false
}

Response:
{
    "success": true,
    "message": "Todo created",
    "data": {"id": 1, "title": "Learn Python", ...}
}
```

---

## ❓ Common Questions

**Q: Do I need to know Python first?**
A: This course assumes you're a beginner. We start from scratch!

**Q: What's the difference between GET and POST?**
A: GET retrieves data, POST sends data. You'll understand this in Day 2.

**Q: Can I use this knowledge for real projects?**
A: Yes! These concepts are used in professional APIs worldwide.

**Q: How long will this take?**
A: 25 days with 2-3 hours of work per day. You can go faster or slower.

---

## 📌 Next Steps

✅ You are here: **Day 1 - Python Basics**

→ Next: **Day 2 - HTTP Concepts**

---

**Let's build your first API! 🎉**
