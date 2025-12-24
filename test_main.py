import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os
import json

# Ensure we can import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import buy_crypto

class TestBuyCrypto(unittest.TestCase):
    @patch('main.API_SECRET', 'test_secret')
    @patch('main.API_KEY', 'test_key')
    @patch('main.BUY_AMOUNT', 100.0)
    @patch('main.requests.post')
    @patch('main.get_server_time')
    @patch('sys.stdout', new_callable=StringIO)
    def test_buy_crypto_success_logging(self, mock_stdout, mock_get_server_time, mock_post):
        # Setup environment variables - handled by patches
        os.environ['SYMBOL'] = 'BTC_THB'

        # Mock server time
        mock_get_server_time.return_value = 1234567890

        # Mock API response
        # Based on Bitkub API documentation for successful buy order
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Real log data from user
        mock_response.json.return_value = {
            "error": 0,
            "result": {
                "amt": 108,
                "ci": "",
                "cre": 0,
                "fee": 0,
                "id": "461929172",
                "rat": 0,
                "rec": 0,
                "ts": "1766600275",
                "typ": "market"
            }
        }
        # Explicitly set text to match the json for the new log
        mock_response.text = json.dumps(mock_response.json.return_value)
        
        mock_post.return_value = mock_response

        # Run function
        try:
            buy_crypto()
        except SystemExit:
            pass 

        # Check Output
        output = mock_stdout.getvalue()
        
        expected_response_json = json.dumps({
            "error": 0,
            "result": {
                "amt": 108,
                "ci": "",
                "cre": 0,
                "fee": 0,
                "id": "461929172",
                "rat": 0,
                "rec": 0,
                "ts": "1766600275",
                "typ": "market"
            }
        })

        expected_output = (
            "🕒 Time: 1234567890\n"
            "🚀 Buying 100.0 THB of BTC_THB...\n"
            "✅ SUCCESS!\n"
            "   Order ID: 461929172\n"
            "   Spend Amount: 108\n"
            f"   Full Response: {expected_response_json}\n"
        )
        
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
