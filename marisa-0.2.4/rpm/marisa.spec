Name:		marisa
Version:	0.2.4
Release:	4.0.0
Summary:	Static and spece-efficient trie data structure library

License:	BSD or LGPL
URL:		https://code.google.com/p/marisa-trie/
Source0:	https://marisa-trie.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	swig
BuildRequires:	perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:	python-devel
BuildRequires:	ruby-devel

%description
Matching Algorithm with Recursively Implemented StorAge (MARISA) is a
static and space-efficient trie data structure. And libmarisa is a C++
library to provide an implementation of MARISA. Also, the package of
libmarisa contains a set of command line tools for building and
operating a MARISA-based dictionary.

A MARISA-based dictionary supports not only lookup but also reverse
lookup, common prefix search and predictive search.


%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tools
Summary:	Tools for %{name}
Group:		Development/Tools
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	tools
The %{name}-tools package contains tools for developing applications
that use %{name}.


%package perl
Summary:	Perl language binding for marisa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description perl
Perl language binding for marisa


%package python
Summary:	Python language binding for marisa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description python
Python language binding for marisa


%package ruby
Summary:	Ruby language binding for marisa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%if 0%{?fedora} >= 19
Requires:	ruby(release) = 2.0.0
%else
Requires:	ruby(abi) = 1.9.1
%endif

%description ruby
Ruby language binding for groonga


%prep
%setup -q


%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

# build Perl bindings
pushd bindings/perl
%{__perl} Makefile.PL INC="-I%{_builddir}/lib" LIBS="-L%{_builddir}/lib/.libs"
make %{?_smp_mflags}
popd

# build Python bindings
pushd bindings/python
%{__python} setup.py build_ext --include-dirs="%{_builddir}/lib" --library-dirs="%{_builddir}/lib/.libs"
%{__python} setup.py build
popd

# build Ruby bindings
pushd bindings/ruby
ruby extconf.rb --with-opt-include="%{_builddir}/lib" --with-opt-lib="%{_builddir}/lib/.libs" --vendor
make
popd

%install
%make_install INSTALL="install -p"

# install Perl bindings
pushd bindings/perl
%make_install INSTALL="install -p"
popd

# install Python bindings
pushd bindings/python
%{__python} setup.py install --root="$RPM_BUILD_ROOT"
popd

# install Ruby bindings
pushd bindings/ruby
%if 0%{?fedora} >= 20
%make_install INSTALL="install -p"
%else
%make_install INSTALL="install -p" hdrdir=%{_includedir} arch_hdrdir="%{_includedir}/\$(arch)" rubyhdrdir=%{_includedir}
%endif
popd

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name 'perllocal.pod' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc docs/* AUTHORS COPYING README
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/marisa*

%files perl
%{perl_sitearch}/*
%exclude %dir %{perl_sitearch}/auto/

%files python
%{python_sitearch}/*

%files ruby
#%{ruby_vendorarchdir}/*
/usr/lib/ruby/vendor_ruby/*


%changelog
* Fri May 02 2014 Takahiro Hashimoto <kenya888@gmail.com> - 0.2.4-4.0.0.jolla
- ported to Jolla

* Tue Aug 13 2013 Daiki Ueno <dueno@redhat.com> - 0.2.4-4
- disable workaround for ruby bindings needed for F19 (Closes:#992166)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.2.4-2
- Perl 5.18 rebuild

* Thu May  2 2013 Daiki Ueno <dueno@redhat.com> - 0.2.4-1
- new upstream release

* Wed Mar 20 2013 Vít Ondruch <vondruch@redhat.com> - 0.2.2-2
- Move Ruby bindings into correct location.

* Thu Mar 14 2013 Daiki Ueno <dueno@redhat.com> - 0.2.2-1
- new upstream release
- for Fedora 19 or later, use 'ruby(release)' instead of 'ruby(abi)',
  and also update the required Ruby ABI/release version to 2.0.0

* Thu Feb  7 2013 Daiki Ueno <dueno@redhat.com> - 0.2.1-3
- add perl, python, ruby bindings

* Fri Feb  1 2013 Daiki Ueno <dueno@redhat.com> - 0.2.1-2
- remove unnesseary BR
- don't embed rpath in executables
- add docs
- drop buildroot cleanup
- preserve timestamp when make install

* Thu Jan 24 2013 Daiki Ueno <dueno@redhat.com> - 0.2.1-1
- initial packaging

