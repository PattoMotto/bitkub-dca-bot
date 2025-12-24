import hashlib
import hmac
import json
import os
import time
import requests
import sys

# ==========================================
# CONFIGURATION
# ==========================================
# Load secrets from GitHub Environment
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
# Default to 108 THB if not set
BUY_AMOUNT = float(os.environ.get("BUY_AMOUNT", "108"))
# Default to 'BTC_THB' if not set
SYMBOL = os.environ.get("SYMBOL", "BTC_THB")


def get_server_time():
    """Get Bitkub server time to avoid 'Invalid Timestamp' errors"""
    try:
        response = requests.get("https://api.bitkub.com/api/v3/servertime")
        return int(response.text)
    except:
        # Fallback to local time if server time fetch fails
        return int(time.time() * 1000)


def buy_crypto():
    if not API_KEY or not API_SECRET:
        print("❌ CRITICAL: API_KEY or API_SECRET is missing from environment variables.")
        sys.exit(1)

    host = "https://api.bitkub.com"
    path = "/api/v3/market/place-bid"
    method = "POST"

    # 1. Sync Time
    timestamp = str(get_server_time())

    # 2. Prepare Body
    # 'rat': 0 is required for market orders
    body = {
        "sym": SYMBOL,
        "amt": BUY_AMOUNT,
        "rat": 0,
        "typ": "market"
    }

    # 3. Compact JSON (Crucial for Signature)
    # separators removes spaces: {"sym":"btc_thb",...} instead of {"sym": "btc_thb", ...}
    body_string = json.dumps(body, separators=(',', ':'))

    # 4. Generate Signature (V3 Standard)
    # Formula: timestamp + method + path + body
    sig_payload = f"{timestamp}{method}{path}{body_string}"

    signature = hmac.new(
        key=API_SECRET.encode('utf-8'),
        msg=sig_payload.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    # 5. Prepare Headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-BTK-APIKEY": API_KEY,
        "X-BTK-TIMESTAMP": timestamp,
        "X-BTK-SIGN": signature
    }

    # 6. Execute Request
    print(f"🕒 Time: {timestamp}")
    print(f"🚀 Buying {BUY_AMOUNT} THB of {SYMBOL}...")

    try:
        response = requests.post(
            f"{host}{path}", headers=headers, data=body_string)
        response_json = response.json()

        # 7. Validate Response
        if response.status_code == 200 and response_json.get('error') == 0:
            result = response_json.get('result', {})
            print("✅ SUCCESS!")
            print(f"   Order ID: {result.get('id')}")
            print(f"   Price: {result.get('rat', 'N/A')}")
            print(f"   Amount: {result.get('rec', 'N/A')}")
            print(f"   Fee: {result.get('cre', 'N/A')}")
            print(f"   Full Response: {response.text}")
        else:
            print("❌ FAILED")
            print(f"   Status Code: {response.status_code}")
            print(f"   Error Code: {response_json.get('error')}")
            print(f"   Full Response: {response.text}")

            # Help debug common errors
            if response_json.get('error') == 11:
                print(
                    "   💡 HINT: Error 11 means 'Invalid Symbol'. Try changing SYMBOL to 'THB_BTC' or 'BTC_THB' (uppercase).")
            if response_json.get('error') == 7:
                print(
                    "   💡 HINT: Error 7 means 'Signature Mismatch'. Check your API Secret.")

            sys.exit(1)  # Fail the action

    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        sys.exit(1)


if __name__ == "__main__":
    buy_crypto()
