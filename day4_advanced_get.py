"""
DAY 4: MASTER GET REQUESTS - FILTERING, SORTING & SEARCH
========================================================
Learn to build powerful GET endpoints with parameters, filtering, and sorting.
These are the skills that make APIs truly useful!
"""

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

print("=" * 80)
print("DAY 4: MASTER GET REQUESTS - FILTERING, SORTING & SEARCH")
print("=" * 80)

# ==============================================================================
# EXTENDED SAMPLE DATABASE
# ==============================================================================
"""
Building a richer dataset with more information so we can practice filtering,
sorting, and searching.
"""

users_db = {
    1: {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 28,
        "city": "New York",
        "role": "admin",
        "active": True,
        "created_date": "2024-01-15"
    },
    2: {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob@example.com",
        "age": 35,
        "city": "Los Angeles",
        "role": "user",
        "active": True,
        "created_date": "2024-02-20"
    },
    3: {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "age": 22,
        "city": "Chicago",
        "role": "user",
        "active": False,
        "created_date": "2024-03-10"
    },
    4: {
        "id": 4,
        "name": "Diana Prince",
        "email": "diana@example.com",
        "age": 31,
        "city": "New York",
        "role": "moderator",
        "active": True,
        "created_date": "2024-01-05"
    },
    5: {
        "id": 5,
        "name": "Eve Wilson",
        "email": "eve@example.com",
        "age": 26,
        "city": "Boston",
        "role": "user",
        "active": True,
        "created_date": "2024-04-12"
    },
    6: {
        "id": 6,
        "name": "Frank Miller",
        "email": "frank@example.com",
        "age": 45,
        "city": "Seattle",
        "role": "admin",
        "active": True,
        "created_date": "2024-02-01"
    }
}


# ==============================================================================
# ENDPOINT 1: BASIC FILTERING - GET /users/filter?role=admin
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 1: Basic Filtering by Role")
print("=" * 80)


@app.route('/users/filter', methods=['GET'])
def filter_users():
    """
    Filter users by role using query parameter.
    Example: /users/filter?role=admin
    """
    role = request.args.get('role')

    if not role:
        return jsonify({
            "success": False,
            "message": "Please provide role parameter: /users/filter?role=admin"
        }), 400

    # Filter users by role
    filtered_users = [
        user for user in users_db.values()
        if user['role'].lower() == role.lower()
    ]

    if not filtered_users:
        return jsonify({
            "success": False,
            "message": f"No users found with role '{role}'",
            "available_roles": ["admin", "user", "moderator"]
        }), 404

    return jsonify({
        "success": True,
        "count": len(filtered_users),
        "role": role,
        "data": filtered_users
    }), 200


print("""
Test in Postman:
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
- ?role=invalid
""")


# ==============================================================================
# ENDPOINT 2: MULTIPLE FILTERS - GET /users/advanced-filter?role=admin&city=NewYork
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 2: Multiple Filters")
print("=" * 80)


@app.route('/users/advanced-filter', methods=['GET'])
def advanced_filter():
    """
    Filter by multiple criteria.
    Example: /users/advanced-filter?role=admin&city=New%20York&active=true
    """
    # Get all query parameters
    role = request.args.get('role')
    city = request.args.get('city')
    active = request.args.get('active')

    # Start with all users
    results = list(users_db.values())

    # Apply filters one by one
    if role:
        results = [u for u in results if u['role'].lower() == role.lower()]

    if city:
        results = [u for u in results if u['city'].lower() == city.lower()]

    if active:
        # Convert string 'true'/'false' to boolean
        active_bool = active.lower() == 'true'
        results = [u for u in results if u['active'] == active_bool]

    if not results:
        return jsonify({
            "success": False,
            "message": "No users match the filters",
            "filters_applied": {
                "role": role,
                "city": city,
                "active": active
            }
        }), 404

    return jsonify({
        "success": True,
        "count": len(results),
        "filters": {
            "role": role,
            "city": city,
            "active": active
        },
        "data": results
    }), 200


print("""
Test in Postman:
GET http://localhost:5000/users/advanced-filter?role=user&city=Chicago

Also try:
GET http://localhost:5000/users/advanced-filter?active=true
GET http://localhost:5000/users/advanced-filter?role=admin&city=New%20York
GET http://localhost:5000/users/advanced-filter?active=false&role=user
""")


# ==============================================================================
# ENDPOINT 3: SORTING - GET /users/sorted?sort_by=age&order=desc
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 3: Sorting Data")
print("=" * 80)


@app.route('/users/sorted', methods=['GET'])
def sorted_users():
    """
    Get users sorted by a specific field.
    Example: /users/sorted?sort_by=age&order=desc
    """
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    # Valid sort fields
    valid_fields = ['id', 'name', 'age', 'created_date']

    if sort_by not in valid_fields:
        return jsonify({
            "success": False,
            "message": f"Invalid sort field '{sort_by}'",
            "valid_fields": valid_fields
        }), 400

    if order.lower() not in ['asc', 'desc']:
        return jsonify({
            "success": False,
            "message": "Order must be 'asc' or 'desc'"
        }), 400

    # Sort users
    sorted_list = sorted(
        users_db.values(),
        key=lambda x: x[sort_by],
        reverse=(order.lower() == 'desc')
    )

    return jsonify({
        "success": True,
        "sort_by": sort_by,
        "order": order,
        "count": len(sorted_list),
        "data": sorted_list
    }), 200


print("""
Test in Postman:

GET http://localhost:5000/users/sorted?sort_by=age&order=desc
→ Shows users by age (oldest first)

GET http://localhost:5000/users/sorted?sort_by=name&order=asc
→ Shows users alphabetically (A to Z)

Also try:
- ?sort_by=created_date&order=asc
- ?sort_by=age&order=asc
- ?sort_by=id&order=desc
""")


# ==============================================================================
# ENDPOINT 4: PAGINATION - GET /users/paginated?page=1&limit=2
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 4: Pagination (Split results into pages)")
print("=" * 80)


@app.route('/users/paginated', methods=['GET'])
def paginated_users():
    """
    Get users with pagination.
    Example: /users/paginated?page=1&limit=2

    Pagination is useful when you have thousands of users.
    Instead of returning all at once, split into pages.
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 3))
    except ValueError:
        return jsonify({
            "success": False,
            "message": "page and limit must be numbers"
        }), 400

    if page < 1 or limit < 1:
        return jsonify({
            "success": False,
            "message": "page and limit must be >= 1"
        }), 400

    # Get all users
    all_users = list(users_db.values())
    total_users = len(all_users)

    # Calculate pagination
    total_pages = (total_users + limit - 1) // limit  # Ceiling division
    start_index = (page - 1) * limit
    end_index = start_index + limit

    # Check if page exists
    if page > total_pages:
        return jsonify({
            "success": False,
            "message": f"Page {page} doesn't exist (total pages: {total_pages})"
        }), 404

    # Get page data
    page_data = all_users[start_index:end_index]

    return jsonify({
        "success": True,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_users": total_users,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        },
        "count": len(page_data),
        "data": page_data
    }), 200


print("""
Test in Postman:

GET http://localhost:5000/users/paginated?page=1&limit=2
→ First 2 users

GET http://localhost:5000/users/paginated?page=2&limit=2
→ Next 2 users

GET http://localhost:5000/users/paginated?page=3&limit=2
→ Last 2 users

Response includes:
{
  "pagination": {
    "page": 1,
    "limit": 2,
    "total_users": 6,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  },
  "data": [...]
}
""")


# ==============================================================================
# ENDPOINT 5: RANGE FILTER - GET /users/by-age?min=25&max=35
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 5: Range Filtering (Min/Max)")
print("=" * 80)


@app.route('/users/by-age', methods=['GET'])
def filter_by_age():
    """
    Filter users by age range.
    Example: /users/by-age?min=25&max=35
    """
    try:
        min_age = int(request.args.get('min', 0))
        max_age = int(request.args.get('max', 150))
    except ValueError:
        return jsonify({
            "success": False,
            "message": "min and max must be numbers"
        }), 400

    # Filter by age range
    results = [
        user for user in users_db.values()
        if min_age <= user['age'] <= max_age
    ]

    if not results:
        return jsonify({
            "success": False,
            "message": f"No users found with age between {min_age} and {max_age}"
        }), 404

    return jsonify({
        "success": True,
        "age_range": {
            "min": min_age,
            "max": max_age
        },
        "count": len(results),
        "data": results
    }), 200


print("""
Test in Postman:

GET http://localhost:5000/users/by-age?min=25&max=35
→ Users aged 25-35

GET http://localhost:5000/users/by-age?min=30
→ Users aged 30 and above

Also try:
- ?max=30
- ?min=20&max=30
""")


# ==============================================================================
# ENDPOINT 6: SEARCH - GET /users/search?q=alice
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 6: Search (Text Search)")
print("=" * 80)


@app.route('/users/search', methods=['GET'])
def search_users():
    """
    Search users by name or email.
    Example: /users/search?q=alice
    Searches across multiple fields for more useful results.
    """
    query = request.args.get('q', '').strip().lower()

    if not query:
        return jsonify({
            "success": False,
            "message": "Please provide search query: /users/search?q=alice"
        }), 400

    # Search in name and email
    results = [
        user for user in users_db.values()
        if query in user['name'].lower() or query in user['email'].lower()
    ]

    if not results:
        return jsonify({
            "success": False,
            "message": f"No users found matching '{query}'"
        }), 404

    return jsonify({
        "success": True,
        "query": query,
        "count": len(results),
        "data": results
    }), 200


print("""
Test in Postman:

GET http://localhost:5000/users/search?q=alice
→ Finds "Alice Johnson"

GET http://localhost:5000/users/search?q=@example.com
→ Finds all with that email domain

Also try:
- ?q=new
- ?q=john
- ?q=smith
- ?q=example
""")


# ==============================================================================
# ENDPOINT 7: COMBINE FILTER + SORT - GET /users/advanced?role=user&sort_by=age&order=desc
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 7: Combine Filters + Sorting")
print("=" * 80)


@app.route('/users/advanced', methods=['GET'])
def advanced_query():
    """
    Advanced endpoint combining multiple features.
    - Filter by role
    - Sort by field
    - Paginate results

    Example: /users/advanced?role=user&sort_by=age&order=desc&page=1&limit=2
    """
    # Get filters
    role = request.args.get('role')
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 3))
    except ValueError:
        return jsonify({"success": False, "message": "Invalid page or limit"}), 400

    # Start with all users
    results = list(users_db.values())

    # Apply filter if provided
    if role:
        results = [u for u in results if u['role'].lower() == role.lower()]

    if not results:
        return jsonify({
            "success": False,
            "message": f"No users found with role '{role}'"
        }), 404

    # Sort
    valid_fields = ['id', 'name', 'age', 'created_date']
    if sort_by in valid_fields:
        results = sorted(
            results,
            key=lambda x: x[sort_by],
            reverse=(order.lower() == 'desc')
        )

    # Paginate
    total = len(results)
    total_pages = (total + limit - 1) // limit

    if page > total_pages or page < 1:
        return jsonify({
            "success": False,
            "message": f"Invalid page {page} (total pages: {total_pages})"
        }), 400

    start = (page - 1) * limit
    end = start + limit
    page_data = results[start:end]

    return jsonify({
        "success": True,
        "filters": {"role": role},
        "sorting": {"sort_by": sort_by, "order": order},
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        },
        "data": page_data
    }), 200


print("""
Test in Postman:

GET http://localhost:5000/users/advanced?role=user&sort_by=age&order=desc

GET http://localhost:5000/users/advanced?sort_by=name&order=asc&page=1&limit=2

GET http://localhost:5000/users/advanced?role=admin&sort_by=created_date

This combines:
✅ Filtering
✅ Sorting
✅ Pagination
""")


# ==============================================================================
# ENDPOINT 8: STATS/ANALYTICS - GET /users/stats
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 8: Statistics/Analytics")
print("=" * 80)


@app.route('/users/stats', methods=['GET'])
def user_stats():
    """
    Return statistics about users.
    This shows how to aggregate data.
    """
    all_users = list(users_db.values())

    stats = {
        "total_users": len(all_users),
        "active_users": len([u for u in all_users if u['active']]),
        "inactive_users": len([u for u in all_users if not u['active']]),
        "average_age": round(sum(u['age'] for u in all_users) / len(all_users), 2),
        "users_by_role": {},
        "users_by_city": {},
        "age_range": {
            "min": min(u['age'] for u in all_users),
            "max": max(u['age'] for u in all_users)
        }
    }

    # Count by role
    for user in all_users:
        role = user['role']
        stats['users_by_role'][role] = stats['users_by_role'].get(role, 0) + 1

    # Count by city
    for user in all_users:
        city = user['city']
        stats['users_by_city'][city] = stats['users_by_city'].get(city, 0) + 1

    return jsonify({
        "success": True,
        "stats": stats
    }), 200


print("""
Test in Postman:
GET http://localhost:5000/users/stats

Response:
{
  "success": true,
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
""")


# ==============================================================================
# ENDPOINT 9: STATUS AND AVAILABLE FILTERS
# ==============================================================================
print("\n" + "=" * 80)
print("ENDPOINT 9: API Documentation Endpoint")
print("=" * 80)


@app.route('/users/help', methods=['GET'])
def users_help():
    """
    Show all available filters and query endpoints.
    """
    return jsonify({
        "success": True,
        "endpoints": {
            "GET /users": "Get all users",
            "GET /users/<id>": "Get specific user",
            "GET /users/filter?role=admin": "Filter by role",
            "GET /users/advanced-filter": "Filter by multiple criteria",
            "GET /users/sorted?sort_by=age&order=desc": "Sort users",
            "GET /users/paginated?page=1&limit=3": "Paginated results",
            "GET /users/by-age?min=25&max=35": "Filter by age range",
            "GET /users/search?q=alice": "Search by name or email",
            "GET /users/advanced": "Combine filter+sort+paginate",
            "GET /users/stats": "User statistics",
            "GET /users/help": "This help page"
        },
        "available_fields": {
            "sort_by": ["id", "name", "age", "created_date"],
            "filter_role": ["admin", "user", "moderator"],
            "order": ["asc", "desc"],
            "boolean": ["true", "false"]
        },
        "example_queries": [
            "/users/filter?role=admin",
            "/users/sorted?sort_by=age&order=desc",
            "/users/paginated?page=1&limit=2",
            "/users/by-age?min=25&max=35",
            "/users/search?q=alice",
            "/users/advanced?role=user&sort_by=age&order=desc&page=1"
        ]
    }), 200


print("""
Test in Postman:
GET http://localhost:5000/users/help

Shows all available endpoints and how to use them!
""")


# ==============================================================================
# RUN SERVER
# ==============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 DAY 4 SERVER STARTING")
    print("=" * 80)
    print("""
Server running on http://localhost:5000

📚 TRY THESE ENDPOINTS:
1. GET /users/help                          (See all endpoints)
2. GET /users/filter?role=admin             (Filter by role)
3. GET /users/sorted?sort_by=age&order=desc (Sort by age)
4. GET /users/paginated?page=1&limit=2      (Pagination)
5. GET /users/by-age?min=25&max=35          (Age range)
6. GET /users/search?q=alice                (Text search)
7. GET /users/advanced?role=user&sort_by=age&order=desc (Combine all)
8. GET /users/stats                         (Statistics)

Check DAY4_INSTRUCTIONS.md for detailed testing guide!
""")

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
