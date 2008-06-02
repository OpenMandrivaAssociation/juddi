# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section         free
%define gcj_support 1

# To make the tarball:
#  export CVSROOT=:pserver:anoncvs@cvs.apache.org:/home/cvspublic
#  cvs login (password: anoncvs)
#  cvs export -r juddi-0_9rc4 ws-juddi
#  find ws-juddi -name '*.jar' | xargs rm

%define basedir %{_localstatedir}/lib/lib/%{name}
#%define appdir %{basedir}/webapps
%define sqldir %{basedir}/sql
%define homedir %{_datadir}/%{name}

Name:           juddi
Summary:        Open source Java implementation UDDI specification
Version:        0.9
Release:        %mkrel 0.rc4.2.0.3
Epoch:          0
URL:            http://ws.apache.org/juddi/
License:        Apache Software License
Group:          Development/Java
Source0:        %{name}-0.9rc4.tar.bz2
BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  axis
BuildRequires:  jakarta-commons-logging
BuildRequires:  tomcat5-servlet-2.4-api
Requires:       axis
Requires:       jakarta-commons-logging
Requires:       tomcat5-servlet-2.4-api
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
jUDDI (pronounced "Judy") is an open source Java implementation 
of the Universal Description, Discovery, and Integration (UDDI) 
specification for Web Services.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package sql-init-statements
Group:          Development/Java
Summary:        SQL statements for database creation/configuration
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description sql-init-statements
SQL statements for creation/configuration of a database 
for storing web services metadata for %{name}.

%package apps
Group:          Development/Java
Summary:        EAR file for jUDDI
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description apps
The Enterprise Archive (ear) file for %{name}.

%package webapps
Group:          Development/Java
Summary:        WAR file for jUDDI
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description webapps
The Web Archive (war) file for %{name}.

%prep
%setup -q -n ws-juddi
mkdir externals
build-jar-repository lib \
    axis/axis \
    axis/jaxrpc \
    axis/saaj \
    jakarta-commons-logging \
    servletapi5 \

%build
unset CLASSPATH
%{ant} -Dant.build.javac.target=1.4 -Dant.build.javac.source=1.4 ear javadoc

%install
rm -rf $RPM_BUILD_ROOT

# *ars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/juddi
install -m 644 build/juddi.ear \
    $RPM_BUILD_ROOT%{_javadir}/juddi/juddi-%{version}.ear
ln -s juddi-%{version}.ear \
    $RPM_BUILD_ROOT%{_javadir}/juddi/juddi.ear

install -m 644 build/juddi.jar \
    $RPM_BUILD_ROOT%{_javadir}/juddi/juddi-%{version}.jar
ln -s juddi-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/juddi/juddi.jar

install -m 644 build/juddi.war \
    $RPM_BUILD_ROOT%{_javadir}/juddi/juddi-%{version}.war
ln -s juddi-%{version}.war \
    $RPM_BUILD_ROOT%{_javadir}/juddi/juddi.war

install -d -m 755 $RPM_BUILD_ROOT{%{appdir},%{sqldir}}

# webapps
#mv build/webapp/* $RPM_BUILD_ROOT%{appdir}

# sql
mv sql/* $RPM_BUILD_ROOT%{sqldir}

# /usr/share/juddi
install -d -m 755 $RPM_BUILD_ROOT/%{homedir}
pushd $RPM_BUILD_ROOT%{homedir}
        [ -d webapps ] || ln -fs %{appdir} webapps
        [ -d sql ] || ln -fs %{sqldir} sql
popd

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/apiDocs/ \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/juddi/*.jar
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files sql-init-statements
%defattr(0644,root,root,0755)
%{sqldir}
%dir %{homedir}/sql
%dir %{homedir}
%dir %{basedir}

%files apps
%defattr(0644,root,root,0755)
%{_javadir}/juddi/*.ear

%files webapps
%defattr(0644,root,root,0755)
%{_javadir}/juddi/*.war
%dir %{homedir}/webapps
