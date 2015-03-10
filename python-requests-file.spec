Name:           python-requests-file
Version:        1.0
Release:        1%{?dist}
Summary:        Transport adapter for using file:// URLs with python-requests

License:        ASL 2.0
URL:            https://github.com/dashea/requests-file
Source0:        https://pypi.python.org/packages/source/r/requests-file/requests-file-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-requests
BuildRequires:  python-six

Requires:       python-requests
Requires:       python-six

%description
Requests-File is a transport adapter for use with the Requests Python
library to allow local filesystem access via file:// URLs.

This is the Python 2 version of the requests_file module

%package -n python3-requests-file
Summary:        Transport adapter for using file:// URLs with python3-requests

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-requests
BuildRequires:  python3-six

Requires:       python3-requests
Requires:       python3-six

%description -n python3-requests-file
Requests-File is a transport adapter for use with the Requests Python
library to allow local filesystem access via file:// URLs.

This is the Python 3 version of the requests_file module

%prep
%setup -qc
mv requests-file-%{version} python2
pushd python2
rm -rf requests-file.egg-info

# Copy common doc files to top dir
cp -pr LICENSE README.rst ../

popd

cp -a python2 python3

%build
pushd python2
%{__python2} setup.py build
popd

pushd python3
%{__python3} setup.py build
popd

%install
pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
popd

pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

%check
pushd python2
%{__python2} setup.py test
popd

pushd python3
%{__python3} setup.py test
popd

%files
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
* Tue Mar 10 2015 David Shea <dshea@redhat.com> - 1.0-1
- Initial package
