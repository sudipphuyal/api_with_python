"""
DAY 8: FETCHING DATA FROM EXTERNAL APIs & STORING IN DATABASE
================================================================
Learn to fetch real data from external APIs and store it locally.
Example: Cryptocurrency prices from CoinGecko API (free, no auth needed)
"""

from flask import Flask, jsonify, request
import sqlite3
import os
import requests
from datetime import datetime, timedelta
import json

# Create Flask app
app = Flask(__name__)

# Database path
DB_PATH = 'api.db'

print("=" * 80)
print("DAY 8: FETCHING EXTERNAL API DATA & STORING IN DATABASE")
print("=" * 80)


# ==============================================================================
# 1. EXTERNAL API SETUP
# ==============================================================================
print("\n" + "=" * 80)
print("1. EXTERNAL API SETUP - CoinGecko Cryptocurrency API")
print("=" * 80)

# Free API - No authentication needed!
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

print("""
🌐 API: CoinGecko (Cryptocurrency Data)
   URL: https://api.coingecko.com/api/v3
   Auth: No authentication required!
   Rate Limit: 10-50 calls/minute (free tier)

Endpoints we'll use:
  - GET /simple/price → Get current prices
  - GET /coins/markets → Market data for coins

Alternative APIs to explore:
  ✓ Open-Meteo (Weather) - No auth
  ✓ RestCountries (Country info) - No auth
  ✓ JSONPlaceholder (Fake data) - No auth
  ✓ Finnhub (Stock prices) - Free tier with key
  ✓ OpenWeatherMap (Weather) - Free tier with key
""")


# ==============================================================================
# 2. DATABASE SETUP
# ==============================================================================
print("\n" + "=" * 80)
print("2. DATABASE SETUP - Create tables for external data")
print("=" * 80)


def init_database():
    """Create database tables"""
    db_exists = os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Existing tables from Day 6
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

    # NEW - Cryptocurrency prices from external API
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            price_usd REAL NOT NULL,
            price_eur REAL,
            price_gbp REAL,
            market_cap_usd REAL,
            volume_24h REAL,
            change_24h REAL,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            api_source TEXT DEFAULT 'coingecko'
        )
    ''')

    # NEW - Weather data from external API (optional)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity INTEGER,
            weather_condition TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # NEW - API fetch logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_name TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            status_code INTEGER,
            records_fetched INTEGER,
            records_stored INTEGER,
            error_message TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    if not db_exists:
        # Insert sample users if new database
        cursor.execute('''
            INSERT INTO users (name, email, age)
            VALUES ('Alice', 'alice@example.com', 25),
                   ('Bob', 'bob@example.com', 30)
        ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized with external API tables")


# Initialize on startup
init_database()


# ==============================================================================
# 3. API HELPER FUNCTIONS
# ==============================================================================
print("\n" + "=" * 80)
print("3. API HELPER FUNCTIONS - Fetch & store external data")
print("=" * 80)


def log_api_fetch(api_name, endpoint, status_code, records_fetched, records_stored, error=None):
    """Log API fetch attempt"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO api_logs (api_name, endpoint, status_code, records_fetched, records_stored, error_message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (api_name, endpoint, status_code, records_fetched, records_stored, error))

    conn.commit()
    conn.close()


def fetch_crypto_prices():
    """
    Fetch cryptocurrency prices from CoinGecko API.

    Returns: dict with status, data, and error info
    """
    print("\n📡 Fetching cryptocurrency prices...")

    try:
        # API endpoint
        url = f"{COINGECKO_API_URL}/simple/price"

        # Parameters
        params = {
            'ids': 'bitcoin,ethereum,cardano,ripple,polkadot',
            'vs_currencies': 'usd,eur,gbp',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true'
        }

        # Make request
        print(f"  Requesting: {url}")
        print(f"  Coins: bitcoin, ethereum, cardano, ripple, polkadot")

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise error if status is not 200

        data = response.json()
        print(f"  ✅ Got response: {response.status_code}")

        # Parse data
        parsed_data = {}
        for coin_id, prices in data.items():
            parsed_data[coin_id] = {
                'symbol': coin_id.upper(),
                'name': coin_id.capitalize(),
                'price_usd': prices.get('usd'),
                'price_eur': prices.get('eur'),
                'price_gbp': prices.get('gbp'),
                'market_cap_usd': prices.get('usd_market_cap'),
                'volume_24h': prices.get('usd_24h_vol'),
                'change_24h': prices.get('usd_24h_change')
            }

        return {
            'success': True,
            'status_code': response.status_code,
            'records': parsed_data,
            'error': None
        }

    except requests.exceptions.Timeout:
        error_msg = "Request timeout - API took too long to respond"
        print(f"  ❌ {error_msg}")
        return {
            'success': False,
            'status_code': None,
            'records': {},
            'error': error_msg
        }

    except requests.exceptions.ConnectionError:
        error_msg = "Connection error - Could not reach API"
        print(f"  ❌ {error_msg}")
        return {
            'success': False,
            'status_code': None,
            'records': {},
            'error': error_msg
        }

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {response.status_code}"
        print(f"  ❌ {error_msg}")
        return {
            'success': False,
            'status_code': response.status_code,
            'records': {},
            'error': error_msg
        }

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"  ❌ {error_msg}")
        return {
            'success': False,
            'status_code': None,
            'records': {},
            'error': error_msg
        }


def store_crypto_prices(data):
    """Store cryptocurrency prices in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    stored_count = 0

    for coin_id, prices in data.items():
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO crypto_prices 
                (symbol, name, price_usd, price_eur, price_gbp, market_cap_usd, volume_24h, change_24h)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prices['symbol'],
                prices['name'],
                prices['price_usd'],
                prices['price_eur'],
                prices['price_gbp'],
                prices['market_cap_usd'],
                prices['volume_24h'],
                prices['change_24h']
            ))
            stored_count += 1
        except sqlite3.Error as e:
            print(f"  ⚠️  Error storing {coin_id}: {str(e)}")

    conn.commit()
    conn.close()

    print(f"  💾 Stored {stored_count} records in database")
    return stored_count


print("""
Helper functions:
✓ fetch_crypto_prices() - Fetch from CoinGecko API
✓ store_crypto_prices() - Save to database
✓ log_api_fetch() - Log all API calls
""")


# ==============================================================================
# 4. ENDPOINTS - Fetch external data
# ==============================================================================
print("\n" + "=" * 80)
print("4. ENDPOINTS - Fetch & refresh external data")
print("=" * 80)


@app.route('/api/fetch-crypto', methods=['POST'])
def fetch_crypto_endpoint():
    """
    Fetch cryptocurrency prices and store in database.
    Manual trigger endpoint.
    """
    # Fetch from API
    result = fetch_crypto_prices()

    if not result['success']:
        # Log failed attempt
        log_api_fetch(
            'coingecko',
            '/simple/price',
            result['status_code'],
            0,
            0,
            result['error']
        )

        return jsonify({
            "success": False,
            "error": result['error']
        }), 400

    # Store in database
    stored_count = store_crypto_prices(result['records'])

    # Log successful fetch
    log_api_fetch(
        'coingecko',
        '/simple/price',
        result['status_code'],
        len(result['records']),
        stored_count
    )

    return jsonify({
        "success": True,
        "message": f"Fetched and stored {stored_count} cryptocurrency prices",
        "records_count": stored_count
    }), 200


@app.route('/crypto/prices', methods=['GET'])
def get_crypto_prices():
    """Get all stored cryptocurrency prices"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM crypto_prices ORDER BY fetched_at DESC
    ''')

    rows = cursor.fetchall()
    prices = [dict(row) for row in rows]
    conn.close()

    return jsonify({
        "success": True,
        "count": len(prices),
        "data": prices
    }), 200


@app.route('/crypto/prices/<symbol>', methods=['GET'])
def get_crypto_price(symbol):
    """Get specific cryptocurrency price"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM crypto_prices WHERE symbol = ? ORDER BY fetched_at DESC LIMIT 1
    ''', (symbol.upper(),))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({
            "success": False,
            "error": f"No price data found for {symbol}"
        }), 404

    return jsonify({
        "success": True,
        "data": dict(row)
    }), 200


@app.route('/api/logs', methods=['GET'])
def get_api_logs():
    """View all API fetch logs"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get last 20 logs
    cursor.execute('''
        SELECT * FROM api_logs ORDER BY fetched_at DESC LIMIT 20
    ''')

    rows = cursor.fetchall()
    logs = [dict(row) for row in rows]
    conn.close()

    return jsonify({
        "success": True,
        "count": len(logs),
        "data": logs
    }), 200


print("""
New endpoints:
✓ POST /api/fetch-crypto → Fetch crypto prices and store
✓ GET /crypto/prices → Get all stored prices
✓ GET /crypto/prices/<symbol> → Get specific coin price
✓ GET /api/logs → View API fetch logs
""")


# ==============================================================================
# 5. API COMPARISON ENDPOINT
# ==============================================================================
print("\n" + "=" * 80)
print("5. ADVANCED - Track price changes over time")
print("=" * 80)


@app.route('/crypto/prices/<symbol>/history', methods=['GET'])
def get_crypto_history(symbol):
    """Get price history for specific cryptocurrency"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT symbol, name, price_usd, price_eur, fetched_at 
        FROM crypto_prices 
        WHERE symbol = ? 
        ORDER BY fetched_at
    ''', (symbol.upper(),))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({
            "success": False,
            "error": f"No price history found for {symbol}"
        }), 404

    history = [dict(row) for row in rows]

    # Calculate statistics
    prices = [row['price_usd'] for row in history]
    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices) / len(prices)
    latest_price = prices[-1] if prices else 0

    return jsonify({
        "success": True,
        "symbol": symbol.upper(),
        "record_count": len(history),
        "statistics": {
            "current_price": latest_price,
            "highest_price": max_price,
            "lowest_price": min_price,
            "average_price": round(avg_price, 2)
        },
        "history": history
    }), 200


print("""
Advanced endpoint:
✓ GET /crypto/prices/<symbol>/history → Price history with statistics
""")


# ==============================================================================
# 6. LEGACY ENDPOINTS FROM DAY 7
# ==============================================================================

@app.route('/', methods=['GET'])
def home():
    """API status"""
    return jsonify({
        "status": "API Running ✅",
        "version": "8.0 - External API Integration",
        "database": "SQLite with external data",
        "endpoints": {
            "POST /api/fetch-crypto": "Fetch crypto prices from CoinGecko",
            "GET /crypto/prices": "Get all stored prices",
            "GET /crypto/prices/<symbol>": "Get specific coin",
            "GET /crypto/prices/<symbol>/history": "Price history & stats",
            "GET /api/logs": "View API fetch attempts",
            "GET /users": "Get all users",
            "POST /users": "Create user",
            "GET /todos": "Get all todos"
        },
        "sample_symbols": ["BITCOIN", "ETHEREUM", "CARDANO", "RIPPLE", "POLKADOT"]
    }), 200


@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users ORDER BY id')
    rows = cursor.fetchall()
    users = [dict(row) for row in rows]
    conn.close()

    return jsonify({
        "success": True,
        "count": len(users),
        "data": users
    }), 200


@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM todos ORDER BY id')
    rows = cursor.fetchall()
    todos = [dict(row) for row in rows]
    conn.close()

    return jsonify({
        "success": True,
        "count": len(todos),
        "data": todos
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("SUMMARY - DAY 8: EXTERNAL API INTEGRATION")
print("=" * 80)

summary = """
╔════════════════════════════════════════════════════════════════════════╗
║              EXTERNAL API DATA INTEGRATION FLOW                        ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  1. CLIENT (Postman)                                                  ║
║     POST /api/fetch-crypto                                            ║
║                ↓                                                       ║
║  2. FLASK SERVER                                                      ║
║     Receives request                                                  ║
║                ↓                                                       ║
║  3. EXTERNAL API (CoinGecko)                                          ║
║     fetch_crypto_prices()                                             ║
║     requests.get(coingecko_url)                                       ║
║                ↓                                                       ║
║  4. API RESPONSE                                                      ║
║     Bitcoin: $50,000                                                  ║
║     Ethereum: $3,000                                                  ║
║     ...                                                               ║
║                ↓                                                       ║
║  5. PROCESS & STORE                                                   ║
║     store_crypto_prices()                                             ║
║     INSERT INTO crypto_prices                                         ║
║                ↓                                                       ║
║  6. DATABASE (SQLite)                                                 ║
║     crypto_prices table updated                                       ║
║                ↓                                                       ║
║  7. RESPONSE TO CLIENT                                                ║
║     {success: true, stored: 5 records}                               ║
║                                                                        ║
║  PATTERN:                                                              ║
║     External API → Validate → Process → Store in DB → Return         ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
"""
print(summary)


# ==============================================================================
# RUN SERVER
# ==============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 STARTING FLASK SERVER - DAY 8 (External API Integration)")
    print("=" * 80)
    print("""
THIS IS IMPORTANT - First time running Day 8:

⚠️  INSTALL REQUESTS LIBRARY:
    pip install requests

Then run:
    python3 day8_external_api.py

🧪 Test in Postman (requires internet):

1. POST http://localhost:5000/api/fetch-crypto
   → Fetches crypto prices from CoinGecko API
   → Stores in database
   → Returns success/failure

2. GET http://localhost:5000/crypto/prices
   → See all stored crypto prices

3. GET http://localhost:5000/crypto/prices/BITCOIN
   → See specific coin price

4. GET http://localhost:5000/api/logs
   → See API fetch history

5. GET http://localhost:5000/
   → See all endpoints

📝 Notes:
   • CoinGecko API requires internet connection
   • No authentication needed
   • Free tier: 10-50 calls/minute
   • Data is stored and persists!

💾 Database files:
   api.db → Main database with all tables
""")

    # Check if requests is installed
    try:
        import requests
        print("✅ requests library found")
    except ImportError:
        print("❌ ERROR: requests library not installed")
        print("   Run: pip install requests")
        print("   Then restart the server")

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
