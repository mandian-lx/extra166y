%{?_javapackages_macros:%_javapackages_macros}
Name:          extra166y
Version:       1.7.0
Release:       7%{?dist}
Summary:       Concurrency JSR-166 - Collections supporting parallel operations
License:       Public Domain
URL:           http://gee.cs.oswego.edu/dl/concurrency-interest
# cvs -d :pserver:anonymous@gee.cs.oswego.edu/home/jsr166/jsr166 login
# cvs -d :pserver:anonymous@gee.cs.oswego.edu/home/jsr166/jsr166 export -r release-1_7_0 jsr166
# available in java 7 rt.jar
# rm -r jsr166/src/main/java
# rm -r jsr166/src/jsr166x jsr166/.cvsignore
# rm -r jsr166/src/jsr166y
# rm -r jsr166/src/loops
# rm -r jsr166/src/test/jtreg
# rm -r jsr166/src/test/loops
# rm -r jsr166/src/test/tck
# find jsr166 -type f -name "*.jar" -delete
# find jsr166 -type f -name "*.class" -delete
# tar cJf jsr166-1.7.0.tar.xz jsr166
Source0:       jsr166-%{version}.tar.xz
Source1:       http://repository.codehaus.org/org/codehaus/jsr166-mirror/%{name}/%{version}/%{name}-%{version}.pom
Source2:       extra166y-OSGi.bnd
Patch0:        extra166y-osgi-manifest.patch
BuildRequires: ant
BuildRequires: aqute-bnd #>= 3.2.0-2
BuildRequires: javapackages-local
BuildRequires: junit
BuildArch:     noarch

%description
Implementation of Java collections supporting parallel operations using
Fork-Join concurrent framework provided by JSR-166.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n jsr166
#%patch0 -p0

# Use JVM jsr166
for s in $(find . -name "*.java");do
  sed -i "s|jsr166y.|java.util.concurrent.|" ${s}
done
sed -i '/configure-compiler, jsr166ycompile/d' build.xml

sed -i '/<compilerarg line="${build.args}"/d' build.xml

cp -p %{SOURCE2} extra166y.bnd
sed -i "s|@VERSION@|%{version}|" extra166y.bnd

%build

%mvn_file org.codehaus.jsr166-mirror:%{name} %{name}
export CLASSPATH=$(build-classpath junit)
ant extra166yjar extra166ydist-docs
java -jar $(build-classpath aqute-bnd) wrap -properties %{name}.bnd build/%{name}lib/%{name}.jar
mv %{name}.bar build/%{name}lib/%{name}.jar

%mvn_artifact %{SOURCE1} build/%{name}lib/%{name}.jar

%install
%mvn_install -J dist/%{name}docs

%files -f .mfiles
%doc src/main/intro.html src/main/readme

%files javadoc -f .mfiles-javadoc
%doc src/main/intro.html src/main/readme

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun  1 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.7.0-6
- Simplify patch for OSGi manifest

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.7.0-4
- Use aqute-bnd-2.4.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 03 2014 gil cattaneo <puntogil@libero.it> 1.7.0-2
- fix license and URL tag
- remove unused test sources

* Mon Nov 03 2014 gil cattaneo <puntogil@libero.it> 1.7.0-1
- initial rpm
