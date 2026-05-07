# 🎓 DAY 8: FETCHING EXTERNAL API DATA & STORING IN DATABASE

## 📋 What You'll Learn

- **HTTP Requests** - Fetch data from external APIs using `requests` library
- **API Integration** - Connect to CoinGecko (cryptocurrency API) with no auth
- **Error Handling** - Deal with timeouts, connection errors, HTTP errors
- **Data Processing** - Parse API responses and transform data
- **Database Storage** - Save external data permanently
- **API Logs** - Track all API calls and results
- **History Tracking** - Compare data over time
- **Real-world patterns** - How production apps integrate 3rd-party APIs

---

## 🌐 The Data Source

### CoinGecko API

- **URL:** https://api.coingecko.com/api/v3
- **Auth:** No authentication required!
- **Rate Limit:** 10-50 calls/minute (free tier)
- **Data:** Cryptocurrency prices, market data, etc.

### Why CoinGecko?

✅ No API key needed  
✅ Public data  
✅ Reliable  
✅ Perfect for learning

---

## 📊 The Complete Flow

```
┌─────────────────┐
│  Postman        │
│ POST /fetch     │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  Flask Server (day8_external_api.py)│
│                                     │
│  fetch_crypto_prices()              │
│  requests.get(api_url)     ←─ Makes HTTP request
└─────────────┬───────────────────────┘
              │
              ↓
    ┌─────────────────────┐
    │  CoinGecko API      │
    │  https://api.../    │
    │  simple/price       │
    └────────┬────────────┘
             │ Returns JSON
             ↓
    {
      "bitcoin": {"usd": 50000, ...},
      "ethereum": {"usd": 3000, ...}
    }
             │
             ↓
    ┌──────────────────────────┐
    │  Parse Response          │
    │  Extract needed data     │
    │  Validate format         │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────┐
    │  Store in Database       │
    │  INSERT INTO crypto_...  │
    │  UPDATE timestamps       │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────┐
    │  SQLite Database         │
    │  api.db                  │
    │  crypto_prices table     │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────┐
    │  Return Response         │
    │  {success: true, ...}    │
    └──────────────────────────┘
```

---

## 🚀 Step 1: Install Required Library

```bash
# Inside virtual environment
source venv/bin/activate

# Install requests library
pip install requests
```

**Verify installation:**

```bash
python3 -c "import requests; print('✅ requests installed')"
```

---

## 🏃 Step 2: Run the Server

```bash
cd /Users/sudipphuyal/Developments/Learn/API
source venv/bin/activate
python3 day8_external_api.py
```

**You should see:**

```
✅ Database initialized with external API tables
✓ fetch_crypto_prices() - Fetch from CoinGecko API
...
🚀 STARTING FLASK SERVER - DAY 8
* Running on http://127.0.0.1:5000
```

---

## 🧪 Testing with Postman

### ⚠️ IMPORTANT: First Need Internet Connection!

All tests require internet to reach CoinGecko API.

---

### Test 1: Fetch Crypto Prices (First Time) 📡

```
Method: POST
URL: http://localhost:5000/api/fetch-crypto
Body: (empty)

Click Send
```

**Expected Response (200):**

```json
{
  "success": true,
  "message": "Fetched and stored 5 cryptocurrency prices",
  "records_count": 5
}
```

**What happened:**

1. Flask contacted CoinGecko API ✓
2. Fetched prices for Bitcoin, Ethereum, Cardano, Ripple, Polkadot ✓
3. Stored in database ✓

**In Terminal:**

```
📡 Fetching cryptocurrency prices...
  Requesting: https://api.coingecko.com/api/v3/simple/price
  Coins: bitcoin, ethereum, cardano, ripple, polkadot
  ✅ Got response: 200
  💾 Stored 5 records in database
```

---

### Test 2: Get All Stored Prices

```
Method: GET
URL: http://localhost:5000/crypto/prices

Click Send
```

**Response (200):**

```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 1,
      "symbol": "BITCOIN",
      "name": "bitcoin",
      "price_usd": 50234.56,
      "price_eur": 46123.45,
      "price_gbp": 39876.12,
      "market_cap_usd": 987654321098,
      "volume_24h": 123456789,
      "change_24h": 2.45,
      "fetched_at": "2026-05-07 12:30:45",
      "api_source": "coingecko"
    },
    {
      "id": 2,
      "symbol": "ETHEREUM",
      "name": "ethereum",
      "price_usd": 2987.34,
      ...
    }
  ]
}
```

**Data stored in database includes:**

- Current price in USD, EUR, GBP
- Market cap
- 24-hour volume
- 24-hour change percentage
- Timestamp when fetched

---

### Test 3: Get Specific Coin Price

```
Method: GET
URL: http://localhost:5000/crypto/prices/BITCOIN

Click Send
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "symbol": "BITCOIN",
    "name": "bitcoin",
    "price_usd": 50234.56,
    "price_eur": 46123.45,
    "price_gbp": 39876.12,
    "market_cap_usd": 987654321098,
    "volume_24h": 123456789,
    "change_24h": 2.45,
    "fetched_at": "2026-05-07 12:30:45",
    "api_source": "coingecko"
  }
}
```

**Try other coins:**

- `/crypto/prices/ETHEREUM`
- `/crypto/prices/CARDANO`
- `/crypto/prices/RIPPLE`
- `/crypto/prices/POLKADOT`

---

### Test 4: View API Fetch Logs

```
Method: GET
URL: http://localhost:5000/api/logs

Click Send
```

**Response (200):**

```json
{
  "success": true,
  "count": 1,
  "data": [
    {
      "id": 1,
      "api_name": "coingecko",
      "endpoint": "/simple/price",
      "status_code": 200,
      "records_fetched": 5,
      "records_stored": 5,
      "error_message": null,
      "fetched_at": "2026-05-07 12:30:45"
    }
  ]
}
```

**Tracks:**

- When API was called
- Which endpoint
- Success/failure status
- How many records fetched vs stored
- Any error messages

---

### Test 5: Price History & Statistics

```
Method: GET
URL: http://localhost:5000/crypto/prices/BITCOIN/history

Click Send (first time)
```

**Response (200):**

```json
{
  "success": true,
  "symbol": "BITCOIN",
  "record_count": 1,
  "statistics": {
    "current_price": 50234.56,
    "highest_price": 50234.56,
    "lowest_price": 50234.56,
    "average_price": 50234.56
  },
  "history": [
    {
      "symbol": "BITCOIN",
      "name": "bitcoin",
      "price_usd": 50234.56,
      "price_eur": 46123.45,
      "fetched_at": "2026-05-07 12:30:45"
    }
  ]
}
```

**Try again later (24 hours later):**

```
Method: GET
URL: http://localhost:5000/crypto/prices/BITCOIN/history

Response now shows:
"record_count": 2 (or more)
"highest_price": X
"lowest_price": Y
"average_price": Z
history: [ old record, new record ]
```

---

### Test 6: Fetch Again (Overwrite)

```
Method: POST
URL: http://localhost:5000/api/fetch-crypto

Click Send
```

**Response (200):**

```json
{
  "success": true,
  "message": "Fetched and stored 5 cryptocurrency prices",
  "records_count": 5
}
```

**What happens:**

1. Latest prices fetched from CoinGecko ✓
2. Database records REPLACED with new data ✓
3. `fetched_at` timestamp updated ✓
4. Old records overwritten (only latest stored) ✓

**Check logs:**

```
GET /api/logs
```

Shows two fetch attempts now!

---

## 📚 Understanding the Code

### Fetching from External API

```python
import requests

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum,cardano',
        'vs_currencies': 'usd,eur,gbp'
    }

    # Make HTTP request
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # Raise error if failed

    # Parse JSON response
    data = response.json()
    return data
```

### Error Handling

```python
try:
    response = requests.get(url, timeout=10)
except requests.exceptions.Timeout:
    # Handle timeout
except requests.exceptions.ConnectionError:
    # Handle connection failed
except requests.exceptions.HTTPError:
    # Handle HTTP error (4xx, 5xx)
except Exception as e:
    # Handle other errors
```

### Storing in Database

```python
def store_crypto_prices(data):
    conn = sqlite3.connect('api.db')
    cursor = conn.cursor()

    for coin, prices in data.items():
        cursor.execute('''
            INSERT OR REPLACE INTO crypto_prices
            (symbol, name, price_usd, price_eur, ...)
            VALUES (?, ?, ?, ?, ...)
        ''', (symbol, name, price_usd, ...))

    conn.commit()
    conn.close()
```

---

## 🗄️ Database Tables Created

### crypto_prices Table

```
id (PRIMARY KEY)
symbol (e.g., "BITCOIN")
name (e.g., "bitcoin")
price_usd (e.g., 50000)
price_eur
price_gbp
market_cap_usd
volume_24h
change_24h
fetched_at (TIMESTAMP)
api_source (e.g., "coingecko")
```

### api_logs Table

```
id (PRIMARY KEY)
api_name (e.g., "coingecko")
endpoint (e.g., "/simple/price")
status_code (200, 404, 500, etc)
records_fetched (how many from API)
records_stored (how many in DB)
error_message (if failed)
fetched_at (TIMESTAMP)
```

### weather_history Table

```
(Created for future use - not used in this example)
location
temperature
humidity
weather_condition
fetched_at
```

---

## 📊 Real Data Example

### What we fetch from CoinGecko:

```json
{
  "bitcoin": {
    "usd": 50234.56,
    "eur": 46123.45,
    "gbp": 39876.12,
    "usd_market_cap": 987654321098,
    "usd_24h_vol": 123456789,
    "usd_24h_change": 2.45
  },
  "ethereum": {
    "usd": 2987.34,
    ...
  }
}
```

### What we store in database:

```
BITCOIN, bitcoin, 50234.56, 46123.45, 39876.12, 987654321098, 123456789, 2.45
ETHEREUM, ethereum, 2987.34, ..., ..., ..., ..., ...
```

---

## 🔄 Complete API Integration Pattern

```
1. USER REQUEST
   POST /api/fetch-crypto

2. FLASK ENDPOINT
   fetch_crypto_endpoint()

3. FETCH FROM API
   fetch_crypto_prices()
   requests.get(coingecko_url)

4. ERROR CHECK
   if response.status != 200:
       return error

5. PARSE DATA
   data = response.json()

6. STORE IN DB
   store_crypto_prices(data)

7. LOG ATTEMPT
   log_api_fetch(...)

8. RETURN RESPONSE
   jsonify({success: true, ...})
```

---

## 💡 Key Concepts

### 1. External API

- Service outside your app that provides data
- You send HTTP request, get JSON response
- CoinGecko, OpenWeatherMap, Finnhub, etc.

### 2. requests Library

```python
import requests
response = requests.get(url)
data = response.json()
```

### 3. Error Handling

- Timeout: `requests.exceptions.Timeout`
- Connection: `requests.exceptions.ConnectionError`
- HTTP Error: `requests.exceptions.HTTPError`

### 4. Database Integration

- Fetch from API → Parse → Validate → Store
- Create audit log of all API calls
- Track success/failure

### 5. Data Persistence

- Store external data locally
- Reduces API calls (if data cached)
- Historical data for comparison

---

## 🎯 Complete Testing Checklist

- [ ] Install: `pip install requests`
- [ ] Run: `python3 day8_external_api.py`
- [ ] POST /api/fetch-crypto → Fetch prices
- [ ] GET /crypto/prices → See all prices
- [ ] GET /crypto/prices/BITCOIN → See Bitcoin
- [ ] GET /crypto/prices/ETHEREUM → See Ethereum
- [ ] GET /api/logs → See fetch logs
- [ ] GET /crypto/prices/BITCOIN/history → See history
- [ ] POST /api/fetch-crypto again → Fetch again
- [ ] GET /api/logs → See two entries
- [ ] Check database file exists (api.db)

---

## 🔍 Advanced: Inspect the Database

```bash
sqlite3 api.db

.tables
# Shows: api_logs, crypto_prices, todos, users, weather_history

SELECT * FROM crypto_prices;
# See all stored prices

SELECT * FROM api_logs;
# See all API calls

SELECT * FROM crypto_prices WHERE symbol = 'BITCOIN';
# Get only Bitcoin prices

.exit
```

---

## 🚨 Troubleshooting

### Error: "No module named requests"

```
Solution: pip install requests
```

### Error: "Connection refused" / "Connection error"

```
Cause: No internet connection or API server down
Solution: Check internet, try again later
```

### Error: "Timeout"

```
Cause: API took too long to respond
Solution: Try again, increase timeout if needed
```

### No data returned

```
Cause: Possible rate limit exceeded
Solution: Wait a few minutes and try again
```

---

## 📚 Alternative APIs to Try

### No Authentication Needed:

- **Open-Meteo** - Weather data

  ```
  https://api.open-meteo.com/v1/forecast
  ```

- **RestCountries** - Country information

  ```
  https://restcountries.com/v3.1/all
  ```

- **JSONPlaceholder** - Fake data for testing
  ```
  https://jsonplaceholder.typicode.com/posts
  ```

### With Free Tier API Key:

- **Finnhub** - Stock prices

  ```
  https://finnhub.io/api/v1/quote
  ```

- **OpenWeatherMap** - Weather
  ```
  https://api.openweathermap.org/data/2.5/weather
  ```

---

## 💾 Architecture Summary

```
┌──────────────────────────────────────┐
│       Your Flask API (Day 8)         │
│  - Endpoints                         │
│  - Request handlers                  │
│  - Database connections              │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│     External APIs (CoinGecko, etc)   │
│  - Cryptocurrency data               │
│  - Weather data                      │
│  - Financial data                    │
│  - etc.                              │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│        SQLite Database (api.db)      │
│  - users                             │
│  - todos                             │
│  - crypto_prices ← NEW               │
│  - api_logs ← NEW                    │
│  - weather_history ← NEW             │
└──────────────────────────────────────┘
```

---

## 🎯 What You've Learned in Day 8

✅ **Fetch Data**: From external APIs using requests  
✅ **Parse JSON**: Extract data from API responses  
✅ **Error Handling**: Timeout, connection, HTTP errors  
✅ **Store External Data**: Save in local database  
✅ **Audit Logging**: Track all API calls  
✅ **Historical Data**: Compare data over time  
✅ **Real-world Patterns**: How production apps work

---

## 📌 Files

- [day8_external_api.py](day8_external_api.py) - Complete Flask app with API integration

---

## 🚀 What's Next?

**Day 9:** Advanced Features

- Scheduled data fetching (run every hour)
- Caching strategies
- Rate limiting
- Multiple API sources
- Data validation & transformation

**You're now building REAL production-like APIs!** 🌟

Keep going! 🎉
