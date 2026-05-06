"""
DAY 1: PYTHON BASICS FOR API DEVELOPMENT
=========================================
This file teaches you Python fundamentals needed for building APIs.
Everything here will be used when we build our API server!
"""

# ==============================================================================
# 1. VARIABLES & DATA TYPES
# ==============================================================================
print("=" * 70)
print("1. VARIABLES & DATA TYPES")
print("=" * 70)

# Strings - text data
name = "Alice"
print(f"Name: {name}")  # f-string is a modern way to format text

# Integers - whole numbers
age = 25
print(f"Age: {age}")

# Floats - decimal numbers
height = 5.7
print(f"Height: {height}")

# Booleans - True or False (used for conditions)
is_active = True
print(f"Is Active: {is_active}")

# None - represents "no value"
phone = None
print(f"Phone: {phone}")


# ==============================================================================
# 2. LISTS - Collections of data
# ==============================================================================
print("\n" + "=" * 70)
print("2. LISTS - Store multiple items")
print("=" * 70)

# Create a list
fruits = ["apple", "banana", "orange"]
print(f"Fruits: {fruits}")

# Access items by index (starts at 0)
print(f"First fruit: {fruits[0]}")
print(f"Last fruit: {fruits[-1]}")

# Add items to list
fruits.append("mango")
print(f"After adding mango: {fruits}")

# Remove items
fruits.remove("banana")
print(f"After removing banana: {fruits}")

# List length
print(f"Number of fruits: {len(fruits)}")

# Loop through list
print("All fruits:")
for fruit in fruits:
    print(f"  - {fruit}")


# ==============================================================================
# 3. DICTIONARIES - Key-value pairs (THIS IS IMPORTANT FOR APIs!)
# ==============================================================================
print("\n" + "=" * 70)
print("3. DICTIONARIES - Key-value pairs (JSON-like structure)")
print("=" * 70)

# Create a dictionary - represents a User object
user = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "is_active": True
}
print(f"User: {user}")

# Access dictionary values
print(f"User name: {user['name']}")
print(f"User email: {user['email']}")

# Add new key-value pair
user["phone"] = "555-1234"
print(f"After adding phone: {user}")

# Loop through dictionary
print("User details:")
for key, value in user.items():
    print(f"  {key}: {value}")

# Get value with default if key doesn't exist
city = user.get("city", "Not provided")
print(f"City: {city}")


# ==============================================================================
# 4. FUNCTIONS - Reusable code blocks
# ==============================================================================
print("\n" + "=" * 70)
print("4. FUNCTIONS - Reusable code blocks")
print("=" * 70)

# Simple function


def greet(name):
    """Function that greets a person"""
    return f"Hello, {name}!"


print(greet("Bob"))

# Function with default parameter


def create_user(name, email, age=18):
    """Create a user dictionary"""
    return {
        "name": name,
        "email": email,
        "age": age
    }


new_user = create_user("Charlie", "charlie@example.com")
print(f"New user: {new_user}")

new_user_with_age = create_user("Diana", "diana@example.com", 30)
print(f"New user with age: {new_user_with_age}")

# Function returning multiple values


def get_coordinates():
    """Return x and y coordinates"""
    return 10, 20


x, y = get_coordinates()
print(f"Coordinates: x={x}, y={y}")


# ==============================================================================
# 5. CONDITIONALS - Making decisions
# ==============================================================================
print("\n" + "=" * 70)
print("5. CONDITIONALS - Making decisions")
print("=" * 70)

age = 20

if age >= 18:
    print(f"Age {age}: You are an adult")
else:
    print(f"Age {age}: You are a minor")

# Multiple conditions
score = 75
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Score {score}: Grade {grade}")


# ==============================================================================
# 6. LOOPS - Repeating actions
# ==============================================================================
print("\n" + "=" * 70)
print("6. LOOPS - Repeating actions")
print("=" * 70)

# For loop
print("Counting 1 to 5:")
for i in range(1, 6):
    print(f"  {i}")

# While loop
print("Countdown:")
count = 3
while count > 0:
    print(f"  {count}")
    count -= 1
print("  Blast off!")


# ==============================================================================
# 7. LISTS OF DICTIONARIES - List of objects (Very important for APIs!)
# ==============================================================================
print("\n" + "=" * 70)
print("7. LISTS OF DICTIONARIES - Collections of objects")
print("=" * 70)

# Database-like structure (this is what APIs return!)
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

print(f"All users: {users}")

# Access specific user
print(f"First user: {users[0]}")
print(f"First user's name: {users[0]['name']}")

# Find a user
target_id = 2
for user in users:
    if user["id"] == target_id:
        print(f"Found user: {user['name']}")
        break


# ==============================================================================
# 8. PRACTICAL EXERCISE - API-like response
# ==============================================================================
print("\n" + "=" * 70)
print("8. PRACTICAL EXERCISE - Creating API response")
print("=" * 70)


def create_api_response(success, message, data=None):
    """Create a standard API response"""
    response = {
        "success": success,
        "message": message,
        "data": data
    }
    return response


# Successful response
api_response_1 = create_api_response(
    success=True,
    message="User created successfully",
    data={"id": 1, "name": "Alice", "email": "alice@example.com"}
)
print(f"Success response: {api_response_1}")

# Error response
api_response_2 = create_api_response(
    success=False,
    message="Invalid email format"
)
print(f"Error response: {api_response_2}")


print("\n" + "=" * 70)
print("✅ DAY 1 COMPLETE! You understand Python basics!")
print("=" * 70)
