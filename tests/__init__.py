import unittest
import requests
from requests_file import FileAdapter

import os, stat
import tempfile

class FileRequestTestCase(unittest.TestCase):
    def setUp(self):
        self._session = requests.Session()
        self._session.mount("file://", FileAdapter())

    def test_fetch_regular(self):
        # Fetch this file using requests
        with open(__file__, "rb") as f:
            testdata = f.read()
        response = self._session.get("file://%s" % os.path.abspath(__file__))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Length'], len(testdata))
        self.assertEqual(response.content, testdata)

    def test_fetch_missing(self):
        # Fetch a file that (hopefully) doesn't exist, look for a 404
        response = self._session.get("file:///no/such/path")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.text)

    def test_fetch_no_access(self):
        # Create a file and remove read permissions, try to get a 403
        # probably doesn't work on windows
        with tempfile.NamedTemporaryFile() as tmp:
            os.chmod(tmp.name, 0)
            response = self._session.get("file://%s" % os.path.abspath(tmp.name))

            self.assertEqual(response.status_code, 403)
            self.assertTrue(response.text)

    def test_fetch_missing_localized(self):
        # Make sure translated error messages don't cause any problems
        import locale

        saved_locale = locale.setlocale(locale.LC_MESSAGES, None)
        try:
            locale.setlocale(locale.LC_MESSAGES, 'ru_RU.UTF-8')
            response = self._session.get("file:///no/such/path")
            self.assertEqual(response.status_code, 404)
            self.assertTrue(response.text)
        finally:
            locale.setlocale(locale.LC_MESSAGES, saved_locale)
