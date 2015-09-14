%global srcname requests-file

Name:           python-%{srcname}
Version:        1.4
Release:        1%{?dist}
Summary:        Transport adapter for using file:// URLs with python-requests

License:        ASL 2.0
URL:            https://github.com/dashea/requests-file
Source0:        https://pypi.python.org/packages/source/r/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description
Requests-File is a transport adapter for use with the Requests Python
library to allow local file system access via file:// URLs.

This is the Python 2 version of the requests_file module

%package -n python2-%{srcname}
Summary:        Transport adapter for using file:// URLs with python-requests
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-requests
BuildRequires:  python-six

Requires:       python-requests
Requires:       python-six

%description -n python2-%{srcname}
Requests-File is a transport adapter for use with the Requests Python
library to allow local file system access via file:// URLs.

This is the Python 2 version of the requests_file module

%package -n python3-requests-file
Summary:        Transport adapter for using file:// URLs with python3-requests
%{?python_provide:%python_provide python3-%{srcname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-requests
BuildRequires:  python3-six

Requires:       python3-requests
Requires:       python3-six

%description -n python3-requests-file
Requests-File is a transport adapter for use with the Requests Python
library to allow local file system access via file:// URLs.

This is the Python 3 version of the requests_file module

%prep
%autosetup -n %{srcname}-%{version}
rm -rf requests_file.egg-info

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/requests_file.py*
%{python2_sitelib}/requests_file*.egg-info*

%files -n python3-requests-file
%license LICENSE
%doc README.rst
%{python3_sitelib}/requests_file.py*
%{python3_sitelib}/__pycache__/requests_file.*
%{python3_sitelib}/requests_file*.egg-info*

%changelog
* Mon Sep 14 2015 David Shea <dshea@redhat.com> - 1.4-1
- Use getprerredencoding instead of nl_langinfo
- Handle files with a drive component
- Switch to the new Fedora packaging guidelines, which renames python-requests-file to python2-requests-file

* Mon May 18 2015 David Shea <dshea@redhat.com> - 1.3.1-1
- Add python version classifiers to the package info

* Mon May 18 2015 David Shea <dshea@redhat.com> - 1.3-1
- Fix a crash when closing a file response.
- Use named aliases instead of integers for status codes.

* Fri May  8 2015 David Shea <dshea@redhat.com> - 1.2-1
- Added support for HEAD requests

* Thu Mar 12 2015 David Shea <dshea@redhat.com> - 1.1-1
- Added handing for %% escapes in URLs
- Proofread the README

* Tue Mar 10 2015 David Shea <dshea@redhat.com> - 1.0-1
- Initial package
