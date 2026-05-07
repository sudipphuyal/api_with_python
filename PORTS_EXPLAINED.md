"""
PORTS EXPLAINED: How localhost:5000 works
=========================================
Understanding ports, how your computer uses them, and how to change them.
"""

print("=" _ 80)
print("UNDERSTANDING PORTS & LOCALHOST")
print("=" _ 80)

explanation = """
╔════════════════════════════════════════════════════════════════════════════╗
║ WHAT IS A PORT? ║
╚════════════════════════════════════════════════════════════════════════════╝

Think of a PORT like an apartment building:

- Your computer's IP address (127.0.0.1 or localhost) = Building address
- Port number (5000) = Apartment number in that building

Multiple Services on One Computer:
┌─────────────────────────────────────────┐
│ YOUR COMPUTER (127.0.0.1) │
├─────────────────────────────────────────┤
│ Port 80: Web Browser (HTTP) │
│ Port 443: Secure Web (HTTPS) │
│ Port 3000: Another app (Node.js) │
│ Port 5000: Your Flask API │ ← Currently here!
│ Port 8000: Another app (Django) │
│ Port 9000: Database server │
└─────────────────────────────────────────┘

When you access: http://localhost:5000/users

- "localhost" = Your computer's local address (127.0.0.1)
- "5000" = Which service to talk to (your Flask app)
- "/users" = Which endpoint

╔════════════════════════════════════════════════════════════════════════════╗
║ HOW POSTMAN CONNECTS ║
╚════════════════════════════════════════════════════════════════════════════╝

1. You type URL in Postman: http://localhost:5000/hello

2. Postman breaks it down:
   Protocol: http://
   Host: localhost (means your own computer)
   Port: 5000 (which service on your computer)
   Path: /hello (which endpoint)

3. Postman connects to port 5000 on your computer

4. Flask app listens on port 5000, receives request

5. Flask processes and sends response back to same port

6. Postman receives and displays response

Visual Flow:
┌──────────────┐ ┌──────────────┐
│ POSTMAN │ Connects to localhost:5000 │ FLASK APP │
│ │ ◄─────────────────────────► (listens) │
│ │ Sends request │ │
│ │ ◄─────────────────────────► Sends response
└──────────────┘ └──────────────┘

╔════════════════════════════════════════════════════════════════════════════╗
║ IMPORTANT TERMS ║
╚════════════════════════════════════════════════════════════════════════════╝

localhost = Your computer (127.0.0.1 internally)
127.0.0.1 = Loopback address (points to your machine)
Port = Entry point for a service
0.0.0.0 = Listen on all network interfaces
app.run(debug=True) = Start the Flask server listening on a port

╔════════════════════════════════════════════════════════════════════════════╗
║ HOW TO CHANGE THE PORT ║
╚════════════════════════════════════════════════════════════════════════════╝

Location in app.py:
"""

print(explanation)

print("""
In app.py, at the very bottom:

┌─────────────────────────────────────────────────┐
│ if **name** == '**main**': │
│ app.run( │
│ host='127.0.0.1', # Localhost only│
│ port=5000, # ← CHANGE THIS │
│ debug=True │
│ ) │
└─────────────────────────────────────────────────┘

CURRENT: port=5000

You can change to:
port=3000 # Different port
port=8000 # Another common port
port=9000 # Yet another option
port=5001 # If 5000 is busy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY CHANGE THE PORT?

Reason 1: Another app already using port 5000
┌──────────────────────────────┐
│ Port 5000 already in use by: │
│ - Another Flask app │
│ - Node.js app │
│ - Other service │
│ → Change to port 3000 │
└──────────────────────────────┘

Reason 2: You want multiple servers running
Port 5000: Flask API 1
Port 5001: Flask API 2
Port 3000: Node.js app
→ Each runs on different port

Reason 3: Development preference
Some developers prefer port 3000 or 8000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW TO CHANGE PORT:

Step 1: Edit app.py
Change: port=5000
To: port=3000

Step 2: Save file

Step 3: Flask auto-reloads (you'll see "Restarting...")

Step 4: In Postman, use new URL
OLD: http://localhost:5000/users
NEW: http://localhost:3000/users

That's it! Your server now runs on the new port.

╔════════════════════════════════════════════════════════════════════════════╗
║ COMMON PORTS EXPLAINED ║
╚════════════════════════════════════════════════════════════════════════════╝

PORT SERVICE TYPE TYPICAL USE
────────────────────────────────────────────────────────────
80 HTTP Web servers (www.example.com)
443 HTTPS Secure web servers (https://)
3000 Node.js Common for Node development
3306 MySQL Database servers
5000 Flask Flask development (our choice!)
5432 PostgreSQL PostgreSQL database
8000 Django Django development
8080 General purpose Alternate web server
9000 Generic service Various services
27017 MongoDB NoSQL database

╔════════════════════════════════════════════════════════════════════════════╗
║ CHANGING HOST (Advanced) ║
╚════════════════════════════════════════════════════════════════════════════╝

Current: host='127.0.0.1' (localhost only - local machine only)

You could change to:
host='0.0.0.0' (listen on all interfaces - local network)
host='192.168.1.100' (specific network address)

⚠️ IMPORTANT:

- 127.0.0.1 = Only your machine can connect
- 0.0.0.0 = Others on your network can connect
- For learning: keep 127.0.0.1 (safer)

╔════════════════════════════════════════════════════════════════════════════╗
║ TROUBLESHOOTING PORT ISSUES ║
╚════════════════════════════════════════════════════════════════════════════╝

PROBLEM: "Address already in use"
────────────────────────────────
Cause: Another process is using port 5000
Solution 1: Change port to 5001 in app.py
Solution 2: Kill the process using port 5000
macOS/Linux:
lsof -i :5000 (find what's using port 5000)
kill -9 <PID> (kill process)
Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

PROBLEM: "Connection refused"
─────────────────────────────
Cause: Flask server not running or wrong port
Solution: Make sure Flask server is running
python3 app.py

PROBLEM: "Port 5000 not responding"
────────────────────────────────────
Cause: Server might be crashed or stuck
Solution:
Press CTRL+C to stop
Wait 5 seconds
python3 app.py to restart

╔════════════════════════════════════════════════════════════════════════════╗
║ QUICK REFERENCE ║
╚════════════════════════════════════════════════════════════════════════════╝

Current Configuration:
URL in Postman: http://localhost:5000/endpoint
Server address: 127.0.0.1 (your computer only)
Port: 5000

To change port to 3000:
Edit app.py last lines from: port=5000
To: port=3000

Postman URL becomes: http://localhost:3000/endpoint

To allow network connections (advanced):
Edit app.py from: host='127.0.0.1'
To: host='0.0.0.0'
⚠️ Only do this when you want others to access!

╔════════════════════════════════════════════════════════════════════════════╗
║ REAL WORLD EXAMPLE ║
╚════════════════════════════════════════════════════════════════════════════╝

Your computer has multiple apps running:

┌──────────────────────────────────┐
│ Your Computer (localhost) │
├──────────────────────────────────┤
│ Port 3000: React frontend │
│ http://localhost:3000
│ │
│ Port 5000: Flask API │
│ http://localhost:5000
│ │
│ Port 27017: MongoDB database │
│ (no web interface) │
│ │
│ Port 8000: Django admin panel │
│ http://localhost:8000
└──────────────────────────────────┘

Each service has its own port so they don't interfere!

╔════════════════════════════════════════════════════════════════════════════╗
║ SUMMARY ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ PORT 5000 is just a number - a "channel" for your Flask app
✅ localhost:5000 = "Talk to port 5000 on my computer"
✅ You can change it anytime (just update the number)
✅ Most ports are just conventions (you choose what you want)
✅ Make sure no other app is using the same port
✅ Your computer can run multiple services on different ports

Think of it like TV channels:
Channel 5000 = Flask API (your server)
Channel 3000 = React app (frontend)
Channel 8000 = Something else

Postman just tunes to the right channel (port) to talk to your server!
"""
)

print("\n" + "=" _ 80)
print("✅ Now you understand ports!")
print("=" _ 80)
