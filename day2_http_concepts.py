"""
DAY 2: HTTP CONCEPTS & REQUEST/RESPONSE CYCLE
==============================================
Understanding how APIs communicate over the internet using HTTP protocol.
This is what happens when you send a request from Postman to a server!
"""

import json
from datetime import datetime

print("=" * 80)
print("DAY 2: HTTP CONCEPTS & REQUEST/RESPONSE CYCLE")
print("=" * 80)


# ==============================================================================
# 1. WHAT IS HTTP?
# ==============================================================================
print("\n" + "=" * 80)
print("1. WHAT IS HTTP? (HyperText Transfer Protocol)")
print("=" * 80)
print("""
HTTP is the language that web browsers and servers use to communicate.
Think of it as a standard way to ask for and send data over the internet.

KEY CONCEPT:
- Client (Postman) sends HTTP REQUEST
- Server receives and processes it
- Server sends HTTP RESPONSE back
- Postman displays the response

Flow: Client Request → Server → Server Response → Client
""")


# ==============================================================================
# 2. HTTP METHODS (Verbs - what action do you want?)
# ==============================================================================
print("\n" + "=" * 80)
print("2. HTTP METHODS - What action do you want?")
print("=" * 80)

http_methods = {
    "GET": {
        "description": "Retrieve data from server",
        "use_case": "Get all users, Get specific user by ID",
        "sends_body": False,
        "postman_default": True
    },
    "POST": {
        "description": "Send data to server to create new resource",
        "use_case": "Create new user, Create new todo",
        "sends_body": True,
        "idempotent": False
    },
    "PUT": {
        "description": "Replace existing data on server",
        "use_case": "Update user profile, Update todo status",
        "sends_body": True,
        "idempotent": True
    },
    "DELETE": {
        "description": "Delete data from server",
        "use_case": "Delete user, Delete todo",
        "sends_body": False,
        "idempotent": True
    }
}

for method, details in http_methods.items():
    print(f"\n{method}")
    print(f"  📝 Description: {details['description']}")
    print(f"  💡 Use Case: {details['use_case']}")
    print(f"  📦 Sends Body: {details.get('sends_body', 'N/A')}")


# ==============================================================================
# 3. ANATOMY OF HTTP REQUEST
# ==============================================================================
print("\n" + "=" * 80)
print("3. ANATOMY OF HTTP REQUEST (What Postman sends)")
print("=" * 80)

print("""
A complete HTTP Request has these parts:

┌────────────────────────────────────────┐
│       REQUEST LINE (Method + URL)      │
├────────────────────────────────────────┤
│         HEADERS (Metadata)             │
├────────────────────────────────────────┤
│            BODY (Data)                 │
│        (For POST, PUT only)            │
└────────────────────────────────────────┘
""")

# Example GET Request
print("EXAMPLE 1: GET REQUEST (No Body)")
print("-" * 80)
get_request = {
    "method": "GET",
    "url": "http://localhost:5000/users/1",
    "headers": {
        "Accept": "application/json",
        "User-Agent": "PostmanRuntime/7.32.3"
    },
    "body": None
}
print(f"Method: {get_request['method']}")
print(f"URL: {get_request['url']}")
print(f"Headers: {json.dumps(get_request['headers'], indent=2)}")
print(f"Body: {get_request['body']}")
print("""
In Postman:
- Method: GET
- URL: http://localhost:5000/users/1
- No body needed
- Click "Send"
""")

# Example POST Request
print("\n\nEXAMPLE 2: POST REQUEST (Has Body)")
print("-" * 80)
post_request = {
    "method": "POST",
    "url": "http://localhost:5000/users",
    "headers": {
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    "body": {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25
    }
}
print(f"Method: {post_request['method']}")
print(f"URL: {post_request['url']}")
print(f"Headers: {json.dumps(post_request['headers'], indent=2)}")
print(f"Body: {json.dumps(post_request['body'], indent=2)}")
print("""
In Postman:
- Method: POST
- URL: http://localhost:5000/users
- Headers: Content-Type: application/json
- Body (raw JSON):
  {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
  }
- Click "Send"
""")


# ==============================================================================
# 4. ANATOMY OF HTTP RESPONSE
# ==============================================================================
print("\n" + "=" * 80)
print("4. ANATOMY OF HTTP RESPONSE (What server sends back)")
print("=" * 80)

print("""
A complete HTTP Response has these parts:

┌────────────────────────────────────────┐
│     STATUS LINE (Status Code)          │
│    (e.g., 200 OK, 404 Not Found)       │
├────────────────────────────────────────┤
│         HEADERS (Metadata)             │
├────────────────────────────────────────┤
│            BODY (Data)                 │
│       (Usually JSON for APIs)          │
└────────────────────────────────────────┘
""")

# Example successful response
print("EXAMPLE 1: SUCCESSFUL RESPONSE (200 OK)")
print("-" * 80)
success_response = {
    "status_code": 200,
    "status_text": "OK",
    "headers": {
        "Content-Type": "application/json",
        "Content-Length": "123"
    },
    "body": {
        "success": True,
        "message": "User retrieved successfully",
        "data": {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com"
        }
    }
}
print(
    f"Status Code: {success_response['status_code']} {success_response['status_text']}")
print(f"Headers: {json.dumps(success_response['headers'], indent=2)}")
print(f"Body: {json.dumps(success_response['body'], indent=2)}")
print("""
In Postman:
- You see "200 OK" in green
- Body tab shows:
  {
    "success": true,
    "message": "User retrieved successfully",
    "data": {...}
  }
""")

# Example error response
print("\n\nEXAMPLE 2: ERROR RESPONSE (404 Not Found)")
print("-" * 80)
error_response = {
    "status_code": 404,
    "status_text": "Not Found",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": {
        "success": False,
        "message": "User not found",
        "data": None
    }
}
print(
    f"Status Code: {error_response['status_code']} {error_response['status_text']}")
print(f"Headers: {json.dumps(error_response['headers'], indent=2)}")
print(f"Body: {json.dumps(error_response['body'], indent=2)}")
print("""
In Postman:
- You see "404 Not Found" in red
- Body tab shows error message
""")


# ==============================================================================
# 5. HTTP STATUS CODES (Server's response code)
# ==============================================================================
print("\n" + "=" * 80)
print("5. HTTP STATUS CODES - Understanding server responses")
print("=" * 80)

status_codes = {
    "2xx - SUCCESS": {
        200: {"name": "OK", "meaning": "Request succeeded, data returned"},
        201: {"name": "Created", "meaning": "Resource created successfully"},
        204: {"name": "No Content", "meaning": "Success but no data to return"}
    },
    "3xx - REDIRECT": {
        301: {"name": "Moved Permanently", "meaning": "Resource moved to new URL"},
        302: {"name": "Found", "meaning": "Resource temporarily at different URL"}
    },
    "4xx - CLIENT ERROR": {
        400: {"name": "Bad Request", "meaning": "Invalid request (malformed JSON)"},
        401: {"name": "Unauthorized", "meaning": "Authentication required"},
        403: {"name": "Forbidden", "meaning": "Access denied"},
        404: {"name": "Not Found", "meaning": "Resource doesn't exist"},
        422: {"name": "Invalid Data", "meaning": "Request has invalid data"}
    },
    "5xx - SERVER ERROR": {
        500: {"name": "Internal Server Error", "meaning": "Server crashed/error"},
        503: {"name": "Service Unavailable", "meaning": "Server is down"}
    }
}

for category, codes in status_codes.items():
    print(f"\n{category}")
    for code, info in codes.items():
        print(f"  {code} {info['name']}: {info['meaning']}")


# ==============================================================================
# 6. REQUEST/RESPONSE FLOW (Complete cycle)
# ==============================================================================
print("\n" + "=" * 80)
print("6. COMPLETE REQUEST/RESPONSE FLOW")
print("=" * 80)

flow = [
    ("USER", "Opens Postman"),
    ("POSTMAN", "Prepares request (URL, method, headers, body)"),
    ("NETWORK", "Sends HTTP request to server"),
    ("SERVER", "Receives request on port 5000"),
    ("SERVER", "Routes to correct endpoint/function"),
    ("SERVER", "Processes request (database query, calculation)"),
    ("SERVER", "Creates response (status code, headers, body)"),
    ("NETWORK", "Sends HTTP response back to client"),
    ("POSTMAN", "Receives response"),
    ("USER", "Sees response in Postman")
]

for i, (actor, action) in enumerate(flow, 1):
    print(f"{i:2d}. [{actor:8s}] {action}")


# ==============================================================================
# 7. HEADERS - Metadata about the request/response
# ==============================================================================
print("\n" + "=" * 80)
print("7. HTTP HEADERS - Information about the request/response")
print("=" * 80)

common_headers = {
    "REQUEST HEADERS": {
        "Content-Type": "application/json",
        "user_says": "Client sends JSON data",
        "example": "Content-Type: application/json"
    },
    "REQUEST HEADERS 2": {
        "Accept": "application/json",
        "user_says": "Client wants JSON in response",
        "example": "Accept: application/json"
    },
    "REQUEST HEADERS 3": {
        "Authorization": "Bearer token123",
        "user_says": "Client sends auth token",
        "example": "Authorization: Bearer eyJhbGc..."
    },
    "RESPONSE HEADERS": {
        "Content-Type": "application/json",
        "server_says": "Server sends JSON data",
        "example": "Content-Type: application/json"
    },
    "RESPONSE HEADERS 2": {
        "Content-Length": "256",
        "server_says": "Response body size in bytes",
        "example": "Content-Length: 256"
    }
}

for header_type, details in common_headers.items():
    header_name = list(details.keys())[0]
    value = details[header_name]
    if "user_says" in details:
        print(f"\n{header_name}: {value}")
        print(f"  → {details['user_says']}")
        print(f"  → Example: {details['example']}")


# ==============================================================================
# 8. SIMULATING A REQUEST/RESPONSE IN CODE
# ==============================================================================
print("\n" + "=" * 80)
print("8. SIMULATING REQUEST/RESPONSE IN PYTHON CODE")
print("=" * 80)


def handle_get_request(user_id):
    """
    Simulate what server does when GET /users/1 is received
    """
    print(f"[SERVER] Received: GET /users/{user_id}")

    # Simulate database lookup
    users_db = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
    }

    # Check if user exists
    if user_id in users_db:
        response = {
            "status_code": 200,
            "status_text": "OK",
            "body": {
                "success": True,
                "data": users_db[user_id]
            }
        }
    else:
        response = {
            "status_code": 404,
            "status_text": "Not Found",
            "body": {
                "success": False,
                "message": "User not found"
            }
        }

    return response


def handle_post_request(request_body):
    """
    Simulate what server does when POST /users is received with user data
    """
    print(f"[SERVER] Received: POST /users")
    print(f"[SERVER] Body: {request_body}")

    # Simulate validation
    if "name" not in request_body or "email" not in request_body:
        response = {
            "status_code": 400,
            "status_text": "Bad Request",
            "body": {
                "success": False,
                "message": "Missing name or email"
            }
        }
    else:
        # Simulate database insert
        response = {
            "status_code": 201,
            "status_text": "Created",
            "body": {
                "success": True,
                "message": "User created",
                "data": {
                    "id": 3,
                    "name": request_body["name"],
                    "email": request_body["email"]
                }
            }
        }

    return response


# Test GET Request
print("\nSCENARIO 1: GET Request (User exists)")
print("-" * 80)
get_response = handle_get_request(1)
print(
    f"[RESPONSE] Status: {get_response['status_code']} {get_response['status_text']}")
print(f"[RESPONSE] Body: {json.dumps(get_response['body'], indent=2)}")

print("\n\nSCENARIO 2: GET Request (User doesn't exist)")
print("-" * 80)
get_response = handle_get_request(999)
print(
    f"[RESPONSE] Status: {get_response['status_code']} {get_response['status_text']}")
print(f"[RESPONSE] Body: {json.dumps(get_response['body'], indent=2)}")

print("\n\nSCENARIO 3: POST Request (Success)")
print("-" * 80)
post_body = {"name": "Charlie", "email": "charlie@example.com"}
post_response = handle_post_request(post_body)
print(
    f"[RESPONSE] Status: {post_response['status_code']} {post_response['status_text']}")
print(f"[RESPONSE] Body: {json.dumps(post_response['body'], indent=2)}")

print("\n\nSCENARIO 4: POST Request (Validation Error)")
print("-" * 80)
post_body = {"name": "Diana"}  # Missing email!
post_response = handle_post_request(post_body)
print(
    f"[RESPONSE] Status: {post_response['status_code']} {post_response['status_text']}")
print(f"[RESPONSE] Body: {json.dumps(post_response['body'], indent=2)}")


# ==============================================================================
# 9. JSON FORMAT (Data format for APIs)
# ==============================================================================
print("\n" + "=" * 80)
print("9. JSON FORMAT - How data is structured in APIs")
print("=" * 80)

print("""
JSON (JavaScript Object Notation) is the standard format for API data.
It's just a Python dictionary represented as text!

JSON Types:
- string: "hello" (quoted text)
- number: 42, 3.14 (no quotes)
- boolean: true, false (lowercase, no quotes)
- null: null (no value)
- array: [...] (list)
- object: {...} (dictionary)
""")

# Python dictionary
python_dict = {
    "user": {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25,
        "is_active": True,
        "phone": None,
        "tags": ["python", "api", "developer"]
    }
}

# Convert to JSON string
json_string = json.dumps(python_dict, indent=2)

print("\nPython Dictionary:")
print(python_dict)

print("\n\nSame data as JSON (text):")
print(json_string)

print("\n\nConvert JSON back to Python:")
parsed_back = json.loads(json_string)
print(parsed_back)
print(f"Name: {parsed_back['user']['name']}")


# ==============================================================================
# 10. PRACTICAL EXERCISE
# ==============================================================================
print("\n" + "=" * 80)
print("10. PRACTICAL EXERCISE - Build a simple API response handler")
print("=" * 80)


def create_todo_api_handler(method, todo_id=None, request_body=None):
    """
    Simulate a Todo API endpoint handler
    """
    todos_db = {
        1: {"id": 1, "title": "Learn Python", "completed": True},
        2: {"id": 2, "title": "Build API", "completed": False}
    }

    if method == "GET" and todo_id is None:
        # GET /todos - Get all todos
        return {
            "status": 200,
            "body": {"success": True, "data": list(todos_db.values())}
        }

    elif method == "GET" and todo_id is not None:
        # GET /todos/1 - Get specific todo
        if todo_id in todos_db:
            return {
                "status": 200,
                "body": {"success": True, "data": todos_db[todo_id]}
            }
        else:
            return {
                "status": 404,
                "body": {"success": False, "message": "Todo not found"}
            }

    elif method == "POST" and request_body:
        # POST /todos - Create new todo
        if "title" not in request_body:
            return {
                "status": 400,
                "body": {"success": False, "message": "Title required"}
            }

        new_todo = {
            "id": 3,
            "title": request_body["title"],
            "completed": False
        }
        return {
            "status": 201,
            "body": {"success": True, "message": "Todo created", "data": new_todo}
        }


# Test the handler
print("\n✅ GET /todos (all todos)")
response = create_todo_api_handler("GET")
print(f"Status: {response['status']}")
print(f"Response: {json.dumps(response['body'], indent=2)}")

print("\n✅ GET /todos/1 (specific todo)")
response = create_todo_api_handler("GET", todo_id=1)
print(f"Status: {response['status']}")
print(f"Response: {json.dumps(response['body'], indent=2)}")

print("\n✅ POST /todos (create todo)")
response = create_todo_api_handler(
    "POST", request_body={"title": "Learn Flask"})
print(f"Status: {response['status']}")
print(f"Response: {json.dumps(response['body'], indent=2)}")


print("\n" + "=" * 80)
print("✅ DAY 2 COMPLETE! You understand HTTP concepts!")
print("=" * 80)
