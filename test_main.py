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
    @patch('main.requests.post')
    @patch('main.get_server_time')
    @patch('sys.stdout', new_callable=StringIO)
    def test_buy_crypto_success_logging(self, mock_stdout, mock_get_server_time, mock_post):
        # Setup environment variables - handled by patches
        os.environ['BUY_AMOUNT'] = '100'
        os.environ['SYMBOL'] = 'BTC_THB'

        # Mock server time
        mock_get_server_time.return_value = 1234567890

        # Mock API response
        # Based on Bitkub API documentation for successful buy order
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": 0,
            "result": {
                "id": "1",
                "typ": "limit",
                "amt": 1000,
                "rat": 15000,
                "fee": 99.9, # Different from cre to ensure we pick cre
                "cre": 2.5,
                "rec": 0.06666666,
                "ts": "1707220636",
                "ci": "input_client_id"
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
        
        # Strict assertions for the fix (values from doc)
        self.assertIn("Price: 15000", output)
        self.assertIn("Amount: 0.06666666", output)
        self.assertIn("Fee: 2.5", output) 
        self.assertIn("Order ID: 1", output)
        self.assertIn("Full Response:", output) # Check that we print the response label
        self.assertIn('"id": "1"', output) # Check that actual JSON content is there
        
        # We expect these to BE currently failing or incorrect based on the bug
        # But we want to verify the FIX produces these.
        
        self.assertIn("✅ SUCCESS!", output)

if __name__ == '__main__':
    unittest.main()
