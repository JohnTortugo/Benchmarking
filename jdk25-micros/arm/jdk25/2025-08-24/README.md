
This is the script used to collect the results:

```
#!/bin/bash

BASELINE_JAVA="/wf/tools/amazon-corretto-25.0.0.32.1-linux-aarch64/bin/java"
TREATMENT_JAVA="/wf/tools/graalvm-community-openjdk-25+25.1/bin/java"

BASELINE_ARGS="-Xms16G -Xmx16G -XX:+UnlockExperimentalVMOptions -XX:-EnableJVMCI"
TREATMENT_ARGS="-Xms16G -Xmx16G -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -XX:+UseJVMCICompiler -XX:+UseJVMCINativeLibrary"

JDKMICRO_ARGS=""

BENCHMARKS=("org.openjdk.bench.java.io." "org.openjdk.bench.java.nio.")

# DONE	    "org.openjdk.bench.java.math."               \
# DONE      "org.openjdk.bench.java.net."                \
# DONE      "org.openjdk.bench.java.lang.Array"          \
# DONE      "org.openjdk.bench.javax.crypto."            \	# Takes ~4hrs total
# DONE      "org.openjdk.bench.java.util."               \	# Takes ~34hrs total
# DONE 	    "org.openjdk.bench.java.lang.String"	 \
# DONE      "org.openjdk.bench.java.lang.Integers"       \
# DONE      "org.openjdk.bench.java.io."                 \
# DONE      "org.openjdk.bench.java.nio."                \


################ Sets a bunch of configs to make the experiment more producible #####################
# source no_noise.sh



for bench in ${BENCHMARKS[@]} ; do
	################   RUN BASELINE CONFIGURATION   ################################
	${BASELINE_JAVA} ${BASELINE_ARGS} -jar /wf/tools/jdk-25-microbenchmarks.jar -rf json -rff baseline-${bench}.json ${JDKMICRO_ARGS} ${bench}

	sleep 120

	################   RUN TREATMENT CONFIGURATION   ###############################
	${TREATMENT_JAVA} ${TREATMENT_ARGS} -jar /wf/tools/jdk-25-microbenchmarks.jar -rf json -rff treatment-${bench}.json ${JDKMICRO_ARGS} ${bench}
done
```


This is the release file for the OpenJDK build:

```
IMPLEMENTOR="Amazon.com Inc."
IMPLEMENTOR_VERSION="Corretto-25.0.0.32.1"
JAVA_RUNTIME_VERSION="25+32-Nightly"
JAVA_VERSION="25"
JAVA_VERSION_DATE="2025-07-20"
LIBC="gnu"
MODULES="java.base java.compiler java.datatransfer java.xml java.prefs java.desktop java.instrument java.logging java.management java.security.sasl java.naming java.rmi java.management.rmi java.net.http java.scripting java.security.jgss java.transaction.xa java.sql java.sql.rowset java.xml.crypto java.se java.smartcardio jdk.accessibility jdk.internal.jvmstat jdk.attach jdk.charsets jdk.internal.opt jdk.zipfs jdk.compiler jdk.crypto.cryptoki jdk.crypto.ec jdk.dynalink jdk.internal.ed jdk.editpad jdk.internal.vm.ci jdk.graal.compiler jdk.graal.compiler.management jdk.hotspot.agent jdk.httpserver jdk.incubator.vector jdk.internal.le jdk.internal.md jdk.jartool jdk.javadoc jdk.jcmd jdk.management jdk.management.agent jdk.jconsole jdk.jdeps jdk.jdwp.agent jdk.jdi jdk.jfr jdk.jlink jdk.jpackage jdk.jshell jdk.jsobject jdk.jstatd jdk.localedata jdk.management.jfr jdk.naming.dns jdk.naming.rmi jdk.net jdk.nio.mapmode jdk.sctp jdk.security.auth jdk.security.jgss jdk.unsupported jdk.unsupported.desktop jdk.xml.dom"
OS_ARCH="aarch64"
OS_NAME="Linux"
SOURCE=".:git:0f7ca194fb71+"
```


This is the release file for the GraalVM build:

```
IMPLEMENTOR="GraalVM Community"
JAVA_RUNTIME_VERSION="25+25-jvmci-b01"
JAVA_VERSION="25"
JAVA_VERSION_DATE="2025-09-16"
LIBC="gnu"
MODULES="java.base java.logging jdk.internal.vm.ci org.graalvm.collections java.management jdk.management jdk.unsupported org.graalvm.truffle.compiler org.graalvm.word jdk.graal.compiler com.oracle.graal.graal_enterprise org.graalvm.nativeimage com.oracle.svm.enterprise.truffle com.oracle.svm.extraimage_enterprise com.oracle.svm.svm_enterprise com.oracle.svm_enterprise.ml_dataset com.oracle.truffle.enterprise.svm java.compiler java.datatransfer java.xml java.prefs java.desktop java.instrument java.security.sasl java.naming java.rmi java.management.rmi java.net.http java.scripting java.security.jgss java.transaction.xa java.sql java.sql.rowset java.xml.crypto java.se java.smartcardio jdk.accessibility jdk.internal.jvmstat jdk.attach jdk.charsets jdk.internal.opt jdk.zipfs jdk.compiler jdk.crypto.cryptoki jdk.crypto.ec jdk.dynalink jdk.internal.ed jdk.editpad jdk.graal.compiler.management jdk.hotspot.agent jdk.httpserver jdk.incubator.vector jdk.internal.le jdk.internal.md jdk.jartool jdk.javadoc jdk.jcmd jdk.management.agent jdk.jconsole jdk.jdeps jdk.jdwp.agent jdk.jdi jdk.jfr jdk.jlink jdk.jpackage jdk.jshell jdk.jsobject jdk.jstatd jdk.localedata jdk.management.jfr jdk.naming.dns jdk.naming.rmi jdk.net jdk.nio.mapmode jdk.sctp jdk.security.auth jdk.security.jgss jdk.unsupported.desktop jdk.xml.dom org.graalvm.extraimage.builder org.graalvm.extraimage.librarysupport org.graalvm.nativeimage.libgraal org.graalvm.webimage.api"
OS_ARCH="aarch64"
OS_NAME="Linux"
SOURCE=".:git:5f461e36d9bb+ labsjdk-builder:b9a413c20b6de505462af407eb83a662a09e7509 compiler:1ec3a06da275663e8332428bdb9fda0f08aedb30 espresso-shared:1ec3a06da275663e8332428bdb9fda0f08aedb30 regex:1ec3a06da275663e8332428bdb9fda0f08aedb30 sdk:1ec3a06da275663e8332428bdb9fda0f08aedb30 substratevm:1ec3a06da275663e8332428bdb9fda0f08aedb30 truffle:1ec3a06da275663e8332428bdb9fda0f08aedb30 vm:1ec3a06da275663e8332428bdb9fda0f08aedb30"
GRAALVM_VERSION="25.0.0-dev"
COMMIT_INFO={"compiler": {"commit.committer": "Paul W\u00f6gerer <paul.woegerer@oracle.com>", "commit.committer-ts": 1749567040, "commit.rev": "1ec3a06da275663e8332428bdb9fda0f08aedb30"}, "espresso-shared": {"commit.committer": "Paul W\u00f6gerer <paul.woegerer@oracle.com>", "commit.committer-ts": 1749567040, "commit.rev": "1ec3a06da275663e8332428bdb9fda0f08aedb30"}, "regex": {"commit.committer": "Paul W\u00f6gerer <paul.woegerer@oracle.com>", "commit.committer-ts": 1749567040, "commit.rev": "1ec3a06da275663e8332428bdb9fda0f08aedb30"}, "sdk": {"commit.committer": "Paul W\u00f6gerer <paul.woegerer@oracle.com>", "commit.committer-ts": 1749567040, "commit.rev": "1ec3a06da275663e8332428bdb9fda0f08aedb30"}, "substratevm": {"commit.committer": "Paul W\u00f6gerer <paul.woegerer@oracle.com>", "commit.committer-ts": 1749567040, "commit.rev": "1ec3a06da275663e8332428bdb9fda0f08aedb30"}, "truffle": {"commit.committer": "Paul W\u00f6gerer <paul.woegerer@oracle.com>", "commit.committer-ts": 1749567040, "commit.rev": "1ec3a06da275663e8332428bdb9fda0f08aedb30"}, "vm": {"commit.committer": "Paul W\u00f6gerer <paul.woegerer@oracle.com>", "commit.committer-ts": 1749567040, "commit.rev": "1ec3a06da275663e8332428bdb9fda0f08aedb30"}}
```
