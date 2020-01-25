# TODO:
# - patch it to use modern dom4j... If anybode cares.
#
# Conditional build:
%bcond_without	source		# don't build source jar
%bcond_without	tests		# don't build and run tests


%define		srcname		werken-xpath
Summary:	W3C XPath-Rec implementation for DOM4J
Name:		java-werken-xpath
Version:	0.9.5
Release:	0.beta.1
License:	BSD
Group:		Libraries/Java
Source0:	http://mesh.dl.sourceforge.net/project/werken-xpath/werken.xpath/0.9.5/werken.xpath-0.9.5-beta-full.tar.gz 
# Source0-md5:	591dccd1f2bdbae384ae824ca79644f7
URL:		http://werken-xpath.sourceforge.net
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
BuildRequires:	sed >= 4.0
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
W3C XPath-Rec implementation for DOM4J.

%package	source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n werken.xpath-dom4j

# Yeah, I love syntax error in *RELEASED* code
sed 's/;;/;/g' -i src/com/werken/xpath/impl/UnAbbrStep.java

rm -rf build bin

%build
export JAVA_HOME="%{java_home}"

# Use dom4j bundled with werken.xpath, as it need an ancient version of dom4j.
required_jars="antlr junit xerces-j2"
CLASSPATH=$(build-classpath $required_jars):lib/dom4j.jar

%ant -Dbuild.sysclasspath=only

# provide dom4j with werken.xpath.jar
mkdir tmp
cd tmp
jar xf ../lib/dom4j.jar
rm -rf MET-INF
jar uf ../build/werken.xpath.jar .
cd ..

cd src
%if %{with source}
%jar cf ../%{srcname}.src.jar $(find -name '*.java')
%endif
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a build/werken.xpath.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{srcname}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with source}
%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
%endif
