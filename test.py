import requests
import unittest

class AppTest(unittest.TestCase):
    #test client for response 200
    def test_status(self):
        base = 'http://127.0.0.1:5000/' #test object
        resp = requests.get(base, json={"text":"test case"})
        statuscode = resp.status_code
        self.assertEqual(statuscode, 200)
    
    def test_data(self):
        base = 'http://127.0.0.1:5000/' #test object
        resp = requests.get(base, json={"text":"test case"})
        data = resp.content
        self.assertTrue(b'prediction' in data)
        
if __name__ == '__main__':
    unittest.main()