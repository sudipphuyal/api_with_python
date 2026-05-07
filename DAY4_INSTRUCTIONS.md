# 🎓 DAY 4: MASTER GET REQUESTS - FILTERING, SORTING & SEARCH

## 📋 What You'll Learn

- **Filtering** - Get specific data (by role, status, etc.)
- **Multiple Filters** - Combine multiple conditions
- **Sorting** - Order results (ascending/descending)
- **Pagination** - Split large results into pages
- **Range Filtering** - Min/max queries
- **Text Search** - Search across fields
- **Advanced Queries** - Combine filter + sort + paginate
- **Statistics** - Aggregate and analyze data
- **API Documentation** - Help endpoint

---

## 🚀 Step 1: Run Day 4 Server

**In a terminal:**

```bash
cd /Users/sudipphuyal/Developments/Learn/API
source venv/bin/activate
python3 day4_advanced_get.py
```

You should see:

```
* Running on http://127.0.0.1:5000
* Debugger is active!
```

---

## 🧪 Step 2: Test All Endpoints in Postman

### Endpoint 1: Filter by Role

```
GET http://localhost:5000/users/filter?role=admin

Response:
{
  "success": true,
  "count": 2,
  "role": "admin",
  "data": [
    {"id": 1, "name": "Alice Johnson", ...},
    {"id": 6, "name": "Frank Miller", ...}
  ]
}

Try:
- ?role=user
- ?role=moderator
- ?role=invalid (returns 404)
```

### Endpoint 2: Advanced Filtering (Multiple Criteria)

```
GET http://localhost:5000/users/advanced-filter?role=user&city=Chicago

Also try:
- ?active=true
- ?role=admin&city=New%20York
- ?active=false&role=user
- ?inactive=true&role=moderator

Response shows all filters that were applied
```

### Endpoint 3: Sorting

```
GET http://localhost:5000/users/sorted?sort_by=age&order=desc

Response: Users sorted by age (oldest first)

Try:
- ?sort_by=name&order=asc (A-Z)
- ?sort_by=created_date&order=asc
- ?sort_by=age&order=asc (youngest first)
- ?sort_by=id&order=desc

Valid sort fields: id, name, age, created_date
Valid orders: asc, desc
```

### Endpoint 4: Pagination

```
GET http://localhost:5000/users/paginated?page=1&limit=2

Response:
{
  "pagination": {
    "page": 1,
    "limit": 2,
    "total_users": 6,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  },
  "data": [user1, user2]
}

Try:
- ?page=1&limit=3
- ?page=2&limit=2
- ?page=3&limit=2
- ?page=2&limit=1 (1 user per page)
- ?page=999 (returns 404 - page doesn't exist)

Key info:
- has_next: true if more pages exist
- has_prev: true if previous pages exist
- Use this to build "Next" and "Previous" buttons in frontend
```

### Endpoint 5: Age Range Filter

```
GET http://localhost:5000/users/by-age?min=25&max=35

Response: Users aged 25-35

Try:
- ?min=30 (30 and above)
- ?max=30 (30 and below)
- ?min=20&max=25
- ?min=50 (no results, returns 404)
```

### Endpoint 6: Text Search

```
GET http://localhost:5000/users/search?q=alice

Searches in name and email fields

Try:
- ?q=john
- ?q=@example.com
- ?q=smith
- ?q=new
- ?q=xyz (no results, returns 404)

Searches are case-insensitive
```

### Endpoint 7: Advanced Query (Combine Everything)

```
GET http://localhost:5000/users/advanced?role=user&sort_by=age&order=desc&page=1&limit=2

Combines:
✅ Filtering (role=user)
✅ Sorting (by age, descending)
✅ Pagination (page 1, 2 results)

Response includes all information:
{
  "filters": {"role": "user"},
  "sorting": {"sort_by": "age", "order": "desc"},
  "pagination": {...},
  "data": [...]
}

Try:
- ?role=admin&sort_by=name&order=asc&page=1&limit=1
- ?sort_by=created_date&order=asc&page=1&limit=2
- ?role=user&sort_by=age&order=asc
```

### Endpoint 8: Statistics

```
GET http://localhost:5000/users/stats

Response:
{
  "stats": {
    "total_users": 6,
    "active_users": 5,
    "inactive_users": 1,
    "average_age": 31.17,
    "users_by_role": {
      "admin": 2,
      "user": 3,
      "moderator": 1
    },
    "users_by_city": {
      "New York": 2,
      "Los Angeles": 1,
      ...
    },
    "age_range": {
      "min": 22,
      "max": 45
    }
  }
}

Great for dashboards and analytics!
```

### Endpoint 9: Help/Documentation

```
GET http://localhost:5000/users/help

Shows:
- All available endpoints
- Available filter options
- Example queries
- Valid values

Perfect for API users to discover features!
```

---

## 📚 Key Concepts

### 1️⃣ Query Parameters

```python
# URL: /users/filter?role=admin&city=NewYork
role = request.args.get('role')      # "admin"
city = request.args.get('city')      # "NewYork"
```

### 2️⃣ Filtering (Select specific data)

```python
# Keep only users with role="admin"
results = [u for u in users if u['role'] == 'admin']
```

### 3️⃣ Sorting (Order data)

```python
# Sort by age, descending
results = sorted(users, key=lambda x: x['age'], reverse=True)
```

### 4️⃣ Pagination (Split into pages)

```python
# Show 3 items per page
page = 1
limit = 3
start = (page - 1) * limit               # 0
end = start + limit                      # 3
page_data = all_results[start:end]       # Items 0-2
```

### 5️⃣ Range Filtering (Min/Max)

```python
min_age = 25
max_age = 35
results = [u for u in users if min_age <= u['age'] <= max_age]
```

### 6️⃣ Text Search (Find matching text)

```python
query = 'alice'
results = [u for u in users if query in u['name'].lower()]
```

---

## 🔄 Real-World Use Cases

### E-Commerce Product Filtering

```
/products/filter?category=electronics&price_min=100&price_max=500&sort_by=popularity
- Filter by category
- Filter by price range
- Sort by popularity
```

### Job Search Website

```
/jobs/search?q=python&location=New%20York&sort_by=date&order=desc&page=1
- Search for keyword
- Filter by location
- Sort by newest first
- Paginate results
```

### Social Media Feed

```
/posts/feed?user_id=123&type=photo&sort_by=date&order=desc&page=1&limit=20
- Filter by user
- Filter by post type
- Sort by newest
- 20 posts per page
```

### Banking Dashboard

```
/transactions/search?status=completed&date_from=2024-01-01&amount_min=100&sort_by=date&order=desc
- Filter by status
- Filter by date range
- Filter by amount range
- Sort by date
```

---

## 📊 Full Sample Dataset

Your API has 6 users with data:

| ID  | Name          | Email       | Age | City        | Role      | Active |
| --- | ------------- | ----------- | --- | ----------- | --------- | ------ |
| 1   | Alice Johnson | alice@...   | 28  | New York    | admin     | ✓      |
| 2   | Bob Smith     | bob@...     | 35  | Los Angeles | user      | ✓      |
| 3   | Charlie Brown | charlie@... | 22  | Chicago     | user      | ✗      |
| 4   | Diana Prince  | diana@...   | 31  | New York    | moderator | ✓      |
| 5   | Eve Wilson    | eve@...     | 26  | Boston      | user      | ✓      |
| 6   | Frank Miller  | frank@...   | 45  | Seattle     | admin     | ✓      |

---

## 🎯 Testing Checklist

### Filtering

- [ ] `GET /users/filter?role=admin` → 2 results
- [ ] `GET /users/filter?role=user` → 3 results
- [ ] `GET /users/filter?role=invalid` → 404 error

### Advanced Filtering

- [ ] `GET /users/advanced-filter?active=true` → 5 results
- [ ] `GET /users/advanced-filter?role=user&city=Chicago` → 1 result
- [ ] `GET /users/advanced-filter?role=admin&city=New%20York` → 1 result

### Sorting

- [ ] `GET /users/sorted?sort_by=age&order=desc` → Oldest first
- [ ] `GET /users/sorted?sort_by=name&order=asc` → A-Z
- [ ] `GET /users/sorted?sort_by=created_date&order=asc` → Oldest first

### Pagination

- [ ] `GET /users/paginated?page=1&limit=2` → 2 users, has_next=true
- [ ] `GET /users/paginated?page=2&limit=2` → 2 users, has_prev=true
- [ ] `GET /users/paginated?page=3&limit=2` → 2 users, has_next=false
- [ ] `GET /users/paginated?page=999&limit=2` → 404 error

### Range Filtering

- [ ] `GET /users/by-age?min=25&max=35` → 4 results
- [ ] `GET /users/by-age?min=30` → 3 results (30+)
- [ ] `GET /users/by-age?max=25` → 1 result (Charlie, age 22)

### Text Search

- [ ] `GET /users/search?q=alice` → 1 result
- [ ] `GET /users/search?q=john` → 1 result (Alice Johnson)
- [ ] `GET /users/search?q=@example.com` → 6 results
- [ ] `GET /users/search?q=xyz` → 404 error

### Advanced Combined

- [ ] `GET /users/advanced?role=user&sort_by=age&order=desc` → Users sorted
- [ ] With pagination: `...&page=1&limit=2` → Limited results + pagination info

### Statistics

- [ ] `GET /users/stats` → Shows aggregated data

### Help

- [ ] `GET /users/help` → Shows all endpoints

---

## 💡 Common Query Patterns

### "Get active admins"

```
GET /users/advanced-filter?role=admin&active=true
```

### "Get users aged 25-35, sorted by name"

```
GET /users/advanced?sort_by=name&order=asc
(Then filter manually or create new endpoint)
```

### "Search for user and paginate results"

```
GET /users/search?q=alice&page=1&limit=10
```

### "Get users from a city, sorted by age"

```
GET /users/advanced-filter?city=New%20York
(Then sort by creating advanced query)
```

---

## 🎓 Practice Assignments

### Task 1: Combine Stats with Filters

Modify `/users/stats` to accept `?role=admin` parameter and show stats only for that role.

### Task 2: Add Email Domain Search

Add endpoint: `/users/by-domain?domain=example.com` to find all users with that email domain.

### Task 3: Add City Filter

Create endpoint: `/users/by-city?city=NewYork` to filter by city.

### Task 4: Combine All Features

Create: `/users/super-advanced?role=user&city=Chicago&sort_by=age&order=asc&min_age=20&max_age=40&page=1&limit=2`

---

## 📌 Files Created

- [day4_advanced_get.py](day4_advanced_get.py) - Advanced GET endpoint examples
- [DAY4_INSTRUCTIONS.md](DAY4_INSTRUCTIONS.md) - This guide

---

## 🎉 What You've Learned

Day 4 skills:
✅ Filtering data by criteria
✅ Multiple filter combinations
✅ Sorting in ascending/descending order
✅ Pagination (splitting results into pages)
✅ Range queries (min/max)
✅ Text search
✅ Combining all features
✅ Data aggregation/statistics
✅ Self-documenting APIs with help endpoints

These are **professional-grade API features** used in real applications!

---

## 🚀 Ready for Day 5?

Next we'll learn:

- **POST requests deep dive** - Create data
- **Input validation** - Check data is correct
- **Database integration** - Save data forever
- **Error handling** - Proper error responses

**When ready, let me know! 🚀**

---

**Key Takeaway:** Modern APIs are not just about getting data - they're about getting _the right data_ in _the right order_ with _the right amount_. Filtering, sorting, and pagination are essential!
