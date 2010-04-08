Name:           gsql
Version:        0.2.2
Release:        1
Summary:        Integrated database development tool for GNOME
Group:          Development/Databases
License:        GPLv2+
URL:            http://gsql.org
Source0:        http://gsql.googlecode.com/files/gsql-%{version}.tar.bz2
Patch1:		gsql-0.2.2-mysql_cursor-format-not-string-literal-and-no-format.patch
Patch2:		gsql-0.2.2-DESTDIR-duplicate.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}
Requires(post):   desktop-file-utils
#Requires(post):   scrollkeeper
Requires(post):   GConf2
Requires(pre):    GConf2
Requires(preun):  GConf2
Requires(postun): desktop-file-utils
#Requires(postun): scrollkeeper
BuildRequires:  gtk2-devel, libGConf2-devel, libglade2-devel, libgtksourceview-2.0-devel
BuildRequires:  libgnome-devel, libgnomeui2-devel, vte-devel, mysql-devel
BuildRequires:  libnotify-devel desktop-file-utils gettext chrpath
BuildRequires:  postgresql-devel, libssh-devel
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
Requires:       %{name} = %{version}-%{release} pkgconfig

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

%build
%configure2_5x \
	--disable-static \
	--without-oracle \
	--with-mysql=%{_prefix} \
	--with-mysql-lib=%{_prefix} \
	--with-mysql-include=%{_prefix} \
	--with-pgsql-lib=%{_prefix} \
	--with-pgsql-include=%{_prefix} 

%make

%install
rm -rf %{buildroot}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall DESTDIR=%{buildroot}
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
#chrpath --delete %{buildroot}%{_bindir}/%{name}
#chrpath --delete %{buildroot}%{_libdir}/%{name}/*/*.so
#desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
find %{buildroot} -name '*.la' -delete
%find_lang %{name}
# remove improperly placed docs
rm -rf %{buildroot}%{_defaultdocdir}/%{name}


%clean
rm -rf %{buildroot}


#%pre
#if [ "$1" -gt 1 ] ; then
#  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#  gconftool-2 --makefile-uninstall-rule \
#    %{_sysconfdir}/gconf/schemas/%{name}.schemas >/dev/null || :
#fi
#
#
#%pre plugins
#if [ "$1" -gt 1 ] ; then
#  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#  gconftool-2 --makefile-uninstall-rule \
#    %{_sysconfdir}/gconf/schemas/%{name}-plugins.schemas >/dev/null || :
#fi
#
#
#%pre engine-mysql
#if [ "$1" -gt 1 ] ; then
#  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#  gconftool-2 --makefile-uninstall-rule \
#    %{_sysconfdir}/gconf/schemas/%{name}-engine-mysql.schemas >/dev/null || :
#fi
#
#
#%post
#update-desktop-database -q
##scrollkeeper-update -q
#export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#gconftool-2 --makefile-install-rule \
#  %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
#/sbin/ldconfig
#
#
#%post plugins
#export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#gconftool-2 --makefile-install-rule \
#  %{_sysconfdir}/gconf/schemas/%{name}-plugins.schemas > /dev/null || :
#
#
#%post engine-mysql
#export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#gconftool-2 --makefile-install-rule \
#  %{_sysconfdir}/gconf/schemas/%{name}-engine-mysql.schemas > /dev/null || :
#
#
#%preun
#  if [ "$1" -eq 0 ] ; then
#  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#  gconftool-2 --makefile-uninstall-rule \
#    %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
#fi
#
#
#%preun plugins
#  if [ "$1" -eq 0 ] ; then
#  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#  gconftool-2 --makefile-uninstall-rule \
#    %{_sysconfdir}/gconf/schemas/%{name}-plugins.schemas > /dev/null || :
#fi
#
#
#%preun engine-mysql
#  if [ "$1" -eq 0 ] ; then
#  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#  gconftool-2 --makefile-uninstall-rule \
#    %{_sysconfdir}/gconf/schemas/%{name}-engine-mysql.schemas > /dev/null || :
#fi
#
#
#%postun
#update-desktop-database -q
##scrollkeeper-update -q
#/sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/engines/
%{_libdir}/lib%{name}*
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

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/lib%{name}/
# scrollkeeper doc generation will be reenabled in future releases
#%{_datadir}/gtk-doc/html/%{name}
#%{_datadir}/gnome/help/%{name}

%files plugins
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/%{name}/plugins/
%{_sysconfdir}/gconf/schemas/%{name}-plugins.schemas
%{_datadir}/pixmaps/%{name}/plugins/
%{_datadir}/%{name}/ui/plugins/
%{_datadir}/%{name}/glade/plugins/

%files engine-mysql
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/%{name}/engines/lib%{name}engine_mysql.so*
%{_sysconfdir}/gconf/schemas/%{name}-engine-mysql.schemas
%{_datadir}/%{name}/ui/mysql/
%{_datadir}/%{name}/glade/mysql/
%{_datadir}/pixmaps/%{name}/mysql/

%files engine-postgresql
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/%{name}/engines/lib%{name}engine_pgsql.so*
%{_datadir}/%{name}/ui/postgresql/
%{_datadir}/%{name}/glade/postgresql/
%{_datadir}/pixmaps/%{name}/postgresql/


%changelog
