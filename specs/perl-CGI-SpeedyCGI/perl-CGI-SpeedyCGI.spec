# $Id$
# Authority: dries
# Upstream: Sam Horrocks <sam$daemoninc,com>

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define real_name CGI-SpeedyCGI

Summary: Speed up perl scripts by running them persistently
Name: perl-CGI-SpeedyCGI
Version: 2.22
Release: 1.2%{?dist}
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/CGI-SpeedyCGI/

Source: http://www.cpan.org/modules/by-module/CGI/CGI-SpeedyCGI-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)

%description
SpeedyCGI is a way to run perl scripts persistently, which can make them
run much more quickly. A script can be made to to run persistently by
changing the interpreter line at the top of the script.

%prep
%setup -n %{real_name}-%{version}

%build
echo | CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install

### Clean up buildroot
find %{buildroot} -name .packlist -exec %{__rm} {} \;

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes README
#%doc %{_mandir}/man3/*
%{_bindir}/speedy*
%dir %{perl_vendorlib}/CGI/
%{perl_vendorlib}/CGI/SpeedyCGI.pm

%changelog
* Sat Apr  9 2005 Dries Verachtert <dries@ulyssis.org> - 2.22-1
- Initial package.
