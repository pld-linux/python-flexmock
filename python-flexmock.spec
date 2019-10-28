#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python3 # CPython 3.x module

%define 	module	flexmock
Summary:	Testing library that makes it easy to create mocks, stubs and fakes
Name:		python-%{module}
Version:	0.9.6
Release:	9
License:	BSD
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/f/flexmock/flexmock-%{version}.tar.gz
# Source0-md5:	f91c7b608fb4235419d75fe9274f7f0c
# git clone https://github.com/has207/flexmock.git && cd flexmock
# git checkout 0.9.6 && tar -czf python-flexmock-0.9.6-tests.tgz tests/
Source1:	%{name}-%{version}-tests.tgz
# Source1-md5:	6cecfda41b4b86a66dc9b6fc3aa9b002
URL:		https://github.com/has207/flexmock
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flexmock is a testing library for Python that makes it easy to create
mocks, stubs and fakes. The API is inspired by a Ruby library of the
same name, but Python flexmock is not a clone of the Ruby version. It
omits a number of redundancies in the Ruby flexmock API, alters some
defaults, and introduces a number of Python-only features.

%package -n python3-flexmock
Summary:	Testing library that makes it easy to create mocks, stubs and fakes
Group:		Libraries/Python

%description -n python3-flexmock
Flexmock is a testing library for Python that makes it easy to create
mocks, stubs and fakes. The API is inspired by a Ruby library of the
same name, but Python flexmock is not a clone of the Ruby version. It
omits a number of redundancies in the Ruby flexmock API, alters some
defaults, and introduces a number of Python-only features.

%prep
%setup -q -n %{module}-%{version}
install -d build/lib
%{__tar} xf %{SOURCE1} -C build/lib

%build
%py_build

%if %{with python3}
%py3_build
%endif

%if %{with tests}
PYTHONPATH=build-2/lib %{__python} tests/flexmock_unittest_test.py

%if %{with python3}
PYTHONPATH=build-3/lib %{__python3} tests/flexmock_unittest_test.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
%py3_install
%endif

%py_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md CHANGELOG
%{py_sitescriptdir}/flexmock.py[co]
%{py_sitescriptdir}/flexmock-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-flexmock
%defattr(644,root,root,755)
%doc LICENSE README.md CHANGELOG
%{py3_sitescriptdir}/__pycache__/%{module}.*.py[co]
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{py3_sitescriptdir}/%{module}.py
%endif
