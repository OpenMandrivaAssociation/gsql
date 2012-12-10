Name:           gsql
Version:        0.2.2
Release:        4
Summary:        Integrated database development tool for GNOME
Group:          Development/Databases
License:        GPLv2+
URL:            http://gsql.org
Source0:        http://gsql.googlecode.com/files/gsql-%{version}.tar.bz2
Patch1:		gsql-0.2.2-mysql_cursor-format-not-string-literal-and-no-format.patch
Patch2:		gsql-0.2.2-DESTDIR-duplicate.patch
Patch3:		gsql-0.2.2-libnotify0.7.patch
BuildRequires:  pkgconfig(gtk+-2.0), pkgconfig(gconf-2.0), pkgconfig(libglade-2.0), libgtksourceview-2.0-devel
BuildRequires:  libgnome2-devel, pkgconfig(libgnomeui-2.0), vte-devel, mysql-devel
BuildRequires:  pkgconfig(libnotify) desktop-file-utils gettext
BuildRequires:  postgresql-devel, libssh-devel >= 1:0.4.2
Requires:       %{name}-engine-mysql = %{version}-%{release}
Requires:       %{name}-engine-postgresql = %{version}-%{release}

%description
The mission of GSQL opensource project is to supply database developers with an
universal tool platform tailored against market leading DBMS by providing:

    * native DBMS access (not via ODBC layer)
    * databased objects organised into a tree
    * intuitive and easy database objects handling
    * syntax highlighting
    * query plan builder
    * query constructor
    * query result export (in XML, CSV, HTML)
    * debugger (depending on RDBMS)
    * query planner control (depending on RDBMS)
    * database administration functions
    * database system monitoring
    * GNOME integration (via gconf and gnome-keyring)


%package        devel
Summary:        Development files for %{name}
Group:          Development/Databases
Requires:       %{name} = %{version}-%{release}
Conflicts:	%{name} < 0.2.2-4

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        plugins
Summary:        Additional plugins for %{name}
Group:          Development/Databases
Requires:       %{name} = %{version}-%{release}

%description    plugins
Additional plugins for %{name}:

    * Terminal - opens a terminal session with parameters (such as login,
                 password etc) taken from the active session
    * Exporter - exports query results to a CVS file. So far only fetched
                 records could be exported
    * Runner   - periodically executes SQL queries


%package        engine-mysql
Summary:        MySQL engine for %{name}
Group:          Development/Databases
Requires:       %{name} = %{version}-%{release}

%description    engine-mysql
MySQL engine for GSQL

%package        engine-postgresql
Summary:        PostgreSQL engine for %{name}
Group:          Development/Databases
Requires:       %{name} = %{version}-%{release}

%description    engine-postgresql
PostgreSQL engine for GSQL

%prep
%setup -q
%patch1 -p0
%patch2 -p1 -b .dest
%patch3 -p0 -b .notify

%build
%configure2_5x \
	--disable-schemas-install \
	--disable-static \
	--without-oracle \
	--with-mysql=%{_prefix} \
	--with-mysql-lib=%{_prefix} \
	--with-mysql-include=%{_prefix} \
	--with-pgsql-lib=%{_prefix} \
	--with-pgsql-include=%{_prefix} 

%make

%install
%makeinstall DESTDIR=%buildroot
%find_lang %{name}
# remove improperly placed docs
rm -rf %{buildroot}%{_defaultdocdir}/%{name}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/engines/
%{_libdir}/lib%{name}*.so.*
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/glade/
%{_datadir}/%{name}/glade/%{name}_dialogs.glade
%dir %{_datadir}/%{name}/ui/
%{_datadir}/%{name}/ui/*.ui
%dir %{_datadir}/pixmaps/%{name}/
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/*

%preun
%preun_uninstall_gconf_schemas %{name}

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/*.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/lib%{name}/

%files plugins
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/%{name}/plugins/
%{_sysconfdir}/gconf/schemas/%{name}-plugins.schemas
%{_datadir}/pixmaps/%{name}/plugins/
%{_datadir}/%{name}/ui/plugins/
%{_datadir}/%{name}/glade/plugins/

%preun plugins
%preun_uninstall_gconf_schemas %{name}-plugins

%files engine-mysql
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/%{name}/engines/lib%{name}engine_mysql.so*
%{_sysconfdir}/gconf/schemas/%{name}-engine-mysql.schemas
%{_datadir}/%{name}/ui/mysql/
%{_datadir}/%{name}/glade/mysql/
%{_datadir}/pixmaps/%{name}/mysql/

%preun engine-mysql
%preun_uninstall_gconf_schemas %{name}-engine-mysql

%files engine-postgresql
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/%{name}/engines/lib%{name}engine_pgsql.so*
%{_datadir}/%{name}/ui/postgresql/
%{_datadir}/%{name}/glade/postgresql/
%{_datadir}/pixmaps/%{name}/postgresql/


%changelog
* Mon May 23 2011 Funda Wang <fwang@mandriva.org> 0.2.2-4mdv2011.0
+ Revision: 677507
- move .so into devel package

* Sat Apr 23 2011 Funda Wang <fwang@mandriva.org> 0.2.2-3
+ Revision: 656817
- build with libnotify 0.7

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-2mdv2011.0
+ Revision: 610987
- rebuild

* Fri Apr 09 2010 Lonyai Gergely <aleph@mandriva.org> 0.2.2-1mdv2010.1
+ Revision: 533361
- Probe fix the libssh-devel version with epoch
- rebuild
- Fix the release tag
- initial release
- create gsql

