import unittest

from databaseFunctions import *

class Tests(unittest.TestCase):
    def test_successful_login(self):
        self.assertTrue(check_login_credentials("hamiltonm", "admin1"))

    def test_failed_login(self):
        self.assertFalse(check_login_credentials("hamiltonm", "wrongpassword"))


if __name__ == '__main__':
    unittest.main()
