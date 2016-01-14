%global pkg_name maven-changes-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.8
Release:        7.11%{?dist}
Summary:        Plugin to support reporting of changes between releases

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/%{pkg_name}
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip
Patch0:         0001-Remove-dependency-on-velocity-tools.patch

BuildArch:      noarch

BuildRequires: %{?scl_prefix_java_common}apache-commons-collections
BuildRequires: %{?scl_prefix_java_common}jakarta-commons-httpclient
BuildRequires: %{?scl_prefix_java_common}apache-commons-io
BuildRequires: %{?scl_prefix_java_common}apache-commons-lang
BuildRequires: %{?scl_prefix_java_common}apache-commons-logging
BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix}maven-project
BuildRequires: %{?scl_prefix}maven-doxia-sitetools
BuildRequires: %{?scl_prefix}maven-install-plugin
BuildRequires: %{?scl_prefix}maven-compiler-plugin
BuildRequires: %{?scl_prefix}maven-plugin-plugin
BuildRequires: %{?scl_prefix}maven-resources-plugin
BuildRequires: %{?scl_prefix}maven-surefire-plugin
BuildRequires: %{?scl_prefix}maven-surefire-provider-junit
BuildRequires: %{?scl_prefix}maven-jar-plugin
BuildRequires: %{?scl_prefix}maven-javadoc-plugin
BuildRequires: %{?scl_prefix}maven-filtering
BuildRequires: %{?scl_prefix}maven-reporting-api
BuildRequires: %{?scl_prefix}maven-reporting-impl
BuildRequires: %{?scl_prefix}modello
BuildRequires: %{?scl_prefix}plexus-containers-container-default
BuildRequires: %{?scl_prefix}plexus-containers-component-metadata
BuildRequires: %{?scl_prefix}plexus-mail-sender
BuildRequires: %{?scl_prefix}plexus-i18n
BuildRequires: %{?scl_prefix}plexus-interpolation
BuildRequires: %{?scl_prefix}plexus-utils
BuildRequires: %{?scl_prefix}plexus-velocity
BuildRequires: %{?scl_prefix_java_common}xmlrpc-client
BuildRequires: %{?scl_prefix_java_common}xmlrpc-common
BuildRequires: %{?scl_prefix_java_common}xerces-j2
BuildRequires: %{?scl_prefix_java_common}xml-commons-apis
BuildRequires: %{?scl_prefix}velocity


%description
This plugin is used to inform your users of the changes that have
occurred between different releases of your project. The plugin can
extract these changes, either from a changes.xml file or from the JIRA
issue management system, and present them as a report. You also have
the option of creating a release announcement and even sending this
via email to your users.


%package javadoc
Summary:  Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x

# remove dependency on velocity-tools
%patch0 -p1
%pom_remove_dep :velocity-tools

# Javamail is provided by JDK
%pom_remove_dep :geronimo-javamail_1.4_mail
%pom_remove_dep :geronimo-javamail_1.4_provider
%pom_remove_dep :geronimo-javamail_1.4_spec

# Fix Maven 3 compatibility
%pom_add_dep org.apache.maven:maven-compat

# Disable github module as we don't have dependencies
rm -rf src/main/java/org/apache/maven/plugin/github
%pom_remove_dep org.apache.httpcomponents:
%pom_remove_dep org.eclipse.mylyn.github:
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.11
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.8-7.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 2.8-7.9
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.8-7.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.4
- Rebuild to fix incorrect auto-requires

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-7.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.8-7
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Apr 10 2013 Michal Srb <msrb@redhat.com> - 2.8-5
- Remove dependency on velocity-tools

* Tue Feb 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-4
- Use default packaging layout

* Tue Feb 12 2013 Michal Srb <msrb@redhat.com> - 2.8-3
- Build with xmvn
- Remove custom depmap

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.8-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Sep 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8-1
- Update to upstream version 2.8
- Convert patches to POM macros
- Install LICENSE and NOTICE files
- Remove rpm bug workaround

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.7.1-1
- Update to latest upstream (2.7.1)
- Remove upstreamed patch for component-metadata migration

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Jaromir Capik <jcapik@redhat.com> 2.6-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata

* Mon Jun 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-1
- Update to latest upstream (2.6)
- Properly complete BR/R
- Fix maven3 compatibility

* Tue May 24 2011 Alexander Kurtakov <akurtako@redhat.com> 2.5-2
- Do not require maven2, require maven.

* Tue May 24 2011 Alexander Kurtakov <akurtako@redhat.com> 2.5-1
- Update to latest upstream - 2.5.

* Fri Mar  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4-1
- Update to latest upsteam (2.4)
- Build with maven 3
- Versionless jars & javadocs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-1
- Initial package
