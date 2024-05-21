2.1.0 (21 May 2024)
===================
- Set the request property in the returned Response object

2.0.0 (29 Jan 2024)
===================
- Correct a typo in requests_file.py (github PR #21)
- Remove dependency on six (github PR #23)
- Move metadata to pyproject.toml (github PR #26)
  - Remove support for Python 2
  - Remove support for raw distutils
- Correct homepage link in pyproject.toml (github PR #28)
- Fix black formatting (github PR #27)

1.5.1 (25 Apr 2020)
===================
- Fix python 2.7 compatibility
- Rename test file for pytest
- Add tests via github actions
- Format code with black

1.5.0 (23 Apr 2020)
==================
- Add set_content_length flag to disable on demand setting Content-Length

1.4.3 (2 Jan 2018)
==================
- Skip the permissions test when running as root
- Handle missing locale in tests

1.4.2 (28 Apr 2017)
===================
- Set the response URL to the request URL

1.4.1 (13 Oct 2016)
===================
- Add a wheel distribution

1.4 (24 Aug 2015)
=================

- Use getprerredencoding instead of nl_langinfo (github issue #1)
- Handle files with a drive component (github issue #2)
- Fix some issues with running the tests on Windows

1.3.1 (18 May 2015)
==================

- Add python version classifiers to the package info

1.3 (18 May 2015)
=================

- Fix a crash when closing a file response.
- Use named aliases instead of integers for status codes.

1.2 (8 May 2015)
=================

- Added support for HEAD requests

1.1 (12 Mar 2015)
=================

- Added handling for % escapes in URLs
- Proofread the README

1.0 (10 Mar 2015)
=================

- Initial release
