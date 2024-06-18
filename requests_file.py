from requests.adapters import BaseAdapter
from requests.compat import urlparse, unquote
from requests import Response, codes
import errno
import os
import stat
import locale
import io
import glob
import urllib

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def parse_query(query):
    p = {}
    for i in query.split('&'):
        i = i.split('=', 1)
        if len(i) > 1:
            p[unquote(i[0])] = unquote(i[1])
    return p

def open_raw(path, query):
    query = parse_query(query)
    try:
        merge = max(int(query.get('merge')), 1)
    except ValueError:
        merge = 1
    if (query.get('glob') == 'yes'):
        files = glob.glob(path)
        filelen = len(files)
        if filelen > merge:
            files = files[:merge]
            filelen = merge
        if filelen == 0:
            raise FileNotFoundError(
    errno.ENOENT, os.strerror(errno.ENOENT), path)
        elif filelen == 1:
            path = files[0]
        else:
            line = b''.join([io.open(path, 'rb').read() for path in files])
            return BytesIO(line)
    return io.open(path, 'rb')

class FileAdapter(BaseAdapter):
    def __init__(self, set_content_length=True):
        super(FileAdapter, self).__init__()
        self._set_content_length = set_content_length

    def send(self, request, **kwargs):
        """Wraps a file, described in request, in a Response object.

        :param request: The PreparedRequest` being "sent".
        :returns: a Response object containing the file
        """

        # Check that the method makes sense. Only support GET
        if request.method not in ("GET", "HEAD"):
            raise ValueError("Invalid request method %s" % request.method)

        # Parse the URL
        url_parts = urlparse(request.url)

        # Reject URLs with a hostname component
        if url_parts.netloc and url_parts.netloc != "localhost":
            raise ValueError("file: URLs with hostname components are not permitted")

        resp = Response()
        resp.request = request

        # Open the file, translate certain errors into HTTP responses
        # Use urllib's unquote to translate percent escapes into whatever
        # they actually need to be
        try:
            # Split the path on / (the URL directory separator) and decode any
            # % escapes in the parts
            path_parts = [unquote(p) for p in url_parts.path.split("/")]

            # Strip out the leading empty parts created from the leading /'s
            while path_parts and not path_parts[0]:
                path_parts.pop(0)

            # If os.sep is in any of the parts, someone fed us some shenanigans.
            # Treat is like a missing file.
            if any(os.sep in p for p in path_parts):
                raise IOError(errno.ENOENT, os.strerror(errno.ENOENT))

            # Look for a drive component. If one is present, store it separately
            # so that a directory separator can correctly be added to the real
            # path, and remove any empty path parts between the drive and the path.
            # Assume that a part ending with : or | (legacy) is a drive.
            if path_parts and (
                path_parts[0].endswith("|") or path_parts[0].endswith(":")
            ):
                path_drive = path_parts.pop(0)
                if path_drive.endswith("|"):
                    path_drive = path_drive[:-1] + ":"

                while path_parts and not path_parts[0]:
                    path_parts.pop(0)
            else:
                path_drive = ""

            # Try to put the path back together
            # Join the drive back in, and stick os.sep in front of the path to
            # make it absolute.
            path = path_drive + os.sep + os.path.join(*path_parts)

            # Check if the drive assumptions above were correct. If path_drive
            # is set, and os.path.splitdrive does not return a drive, it wasn't
            # really a drive. Put the path together again treating path_drive
            # as a normal path component.
            if path_drive and not os.path.splitdrive(path):
                path = os.sep + os.path.join(path_drive, *path_parts)

            # Use io.open since we need to add a release_conn method, and
            # methods can't be added to file objects in python 2.
            raw = open_raw(path, url_parts.query)
            resp.raw = raw
            resp.raw.release_conn = raw.close
        except IOError as e:
            if e.errno == errno.EACCES:
                resp.status_code = codes.forbidden
            elif e.errno == errno.ENOENT:
                resp.status_code = codes.not_found
            else:
                resp.status_code = codes.bad_request

            # Wrap the error message in a file-like object
            # The error message will be localized, try to convert the string
            # representation of the exception into a byte stream
            resp_str = str(e).encode(locale.getpreferredencoding(False))
            raw = resp.raw = BytesIO(resp_str)
            if self._set_content_length:
                resp.headers["Content-Length"] = len(resp_str)

            # Add release_conn to the BytesIO object
            resp.raw.release_conn = raw.close
        else:
            resp.status_code = codes.ok
            resp.url = request.url

            # If it's a regular file, set the Content-Length
            resp_stat = os.fstat(raw.fileno())
            if stat.S_ISREG(resp_stat.st_mode) and self._set_content_length:
                resp.headers["Content-Length"] = resp_stat.st_size

        return resp

    def close(self):
        pass
