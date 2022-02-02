from project import app
import unittest

class FlaksTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertTrue(b'There are' in response.data)


if __name__ == '__main__':
    unittest.main()
