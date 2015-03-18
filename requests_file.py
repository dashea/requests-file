from requests.adapters import BaseAdapter
from requests.compat import urlparse, unquote
from requests import Response
import errno
import os
import stat
import locale

from six import BytesIO

class FileAdapter(BaseAdapter):
    def send(self, request, **kwargs):
        """ Wraps a file, described in request, in a Response object.

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

        # Open the file, translate certain errors into HTTP responses
        # Use urllib's unquote to translate percent escapes into whatever
        # they actually need to be
        try:
            # Split the path on / (the URL directory separator) and decode any
            # % escapes in the parts
            path_parts = [unquote(p) for p in url_parts.path.split('/')]

            # If os.sep is in any of the parts, someone fed us some shenanigans.
            # Treat is like a missing file.
            if any(os.sep in p for p in path_parts):
                raise IOError(errno.ENOENT, os.strerror(errno.ENOENT))

            # Put it the path back together
            # [0] will be an empty string, so stick os.sep in there to make
            # the path absolute
            path_parts[0] = os.sep
            path = os.path.join(*path_parts)

            resp.raw = open(path, "rb")
        except IOError as e:
            if e.errno == errno.EACCES:
                resp.status_code = 403
            elif e.errno == errno.ENOENT:
                resp.status_code = 404
            else:
                resp.status_code = 400

            # Wrap the error message in a file-like object
            # The error message will be localized, try to convert the string
            # representation of the exception into a byte stream
            resp_str = str(e).encode(locale.nl_langinfo(locale.CODESET))
            resp.raw = BytesIO(resp_str)
            resp.headers['Content-Length'] = len(resp_str)
        else:
            resp.status_code = 200

            # If it's a regular file, set the Content-Length
            resp_stat = os.fstat(resp.raw.fileno())
            if stat.S_ISREG(resp_stat.st_mode):
                resp.headers['Content-Length'] = resp_stat.st_size

        return resp

    def close(self):
        pass
