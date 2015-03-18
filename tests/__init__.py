import unittest
import requests
from requests_file import FileAdapter

import os, stat
import tempfile
import shutil

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

    def test_head(self):
        # Check that HEAD returns the content-length
        testlen = os.stat(__file__).st_size
        response = self._session.head("file://%s" % os.path.abspath(__file__))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Length'], testlen)

    def test_fetch_post(self):
        # Make sure that non-GET methods are rejected
        self.assertRaises(ValueError, self._session.post,
                ("file://%s" % os.path.abspath(__file__)))

    def test_fetch_nonlocal(self):
        # Make sure that network locations are rejected
        self.assertRaises(ValueError, self._session.get,
                ("file://example.com%s" % os.path.abspath(__file__)))
        self.assertRaises(ValueError, self._session.get,
                ("file://localhost:8080%s" % os.path.abspath(__file__)))

        # localhost is ok, though
        with open(__file__, "rb") as f:
            testdata = f.read()
        response = self._session.get("file://localhost%s" % os.path.abspath(__file__))
        self.assertEqual(response.content, testdata)

    def test_funny_names(self):
        testdata = 'yo wassup man\n'.encode('ascii')
        tmpdir = tempfile.mkdtemp()

        try:
            with open(os.path.join(tmpdir, 'spa ces'), "w+b") as space_file:
                space_file.write(testdata)
                space_file.flush()
                response = self._session.get("file://%s/spa%%20ces" % tmpdir)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content, testdata)

            with open(os.path.join(tmpdir, 'per%cent'), "w+b") as percent_file:
                percent_file.write(testdata)
                percent_file.flush()
                response = self._session.get("file://%s/per%%25cent" % tmpdir)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content, testdata)

            # percent-encoded directory separators should be rejected
            with open(os.path.join(tmpdir, 'badname'), "w+b") as bad_file:
                response = self._session.get("file://%s%%2Fbadname" % tmpdir)
                self.assertEqual(response.status_code, 404)

        finally:
            shutil.rmtree(tmpdir)
