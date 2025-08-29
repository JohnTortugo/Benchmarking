### Title
OpenJDK25 vs Graal25 on Renaissance-0.16 @ AArch64

### Operating System
Linux

### Platform Architecture
AArch64

### Benchmark Details
Renaissance-JMH-0.16.0

### Baseline Label
OpenJDK25

### Treatment Label
GraalVM25

### Baseline VM Details
openjdk version "25" 2025-07-20
OpenJDK Runtime Environment Corretto-25.0.0.32.1 (build 25+32-Nightly)
OpenJDK 64-Bit Server VM Corretto-25.0.0.32.1 (build 25+32-Nightly, mixed mode, sharing)

### Treatment VM Details
openjdk version "25" 2025-09-16
OpenJDK Runtime Environment GraalVM CE 25-dev+25.1 (build 25+25-jvmci-b01)
OpenJDK 64-Bit Server VM GraalVM CE 25-dev+25.1 (build 25+25-jvmci-b01, mixed mode, sharing)

### Machine Details
=== RAM ===
MemTotal:       131615788 kB

=== CPU ===
CPU(s):                               64
Model name:                           Neoverse-V1
Thread(s) per core:                   1
Core(s) per socket:                   64
Socket(s):                            1

=== OS ===
PRETTY_NAME="Ubuntu 24.04.2 LTS"
VERSION_ID="24.04"
Kernel:  uname -r

=== AMI ===
ami-0c4e709339fa8521a

### Script used to run the benchmarks

```
BASELINE_JAVA="/wf/tools/amazon-corretto-25.0.0.32.1-linux-aarch64/bin/java"
TREATMENT_JAVA="/wf/tools/graalvm-community-openjdk-25+25.1/bin/java"

COMMON_ARGS="--enable-native-access=ALL-UNNAMED			  				\
	         --illegal-access=permit --add-exports java.base/jdk.internal.ref=ALL-UNNAMED	\
             --add-opens=java.base/java.net=ALL-UNNAMED 	  				\
             --add-opens=java.base/java.lang=ALL-UNNAMED 	  				\
             --add-opens=java.base/sun.nio.ch=ALL-UNNAMED 	  				\
             --add-opens=java.base/java.lang.reflect=ALL-UNNAMED  				\
             --add-opens=java.base/java.lang.invoke=ALL-UNNAMED   				\
	         --add-opens=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED 			\
             --add-opens=java.base/java.util=ALL-UNNAMED 	  				\
             --add-opens=java.base/java.nio=ALL-UNNAMED		  				"
BASELINE_ARGS="-Xms16G -Xmx16G -XX:+UnlockExperimentalVMOptions -XX:-EnableJVMCI"
TREATMENT_ARGS="-Xms16G -Xmx16G -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -XX:+UseJVMCICompiler -XX:+UseJVMCINativeLibrary"

JDKMICRO_ARGS=""

BENCHMARKS=("JmhAkkaUct"
            "JmhReactors"
            "JmhAls"
            "JmhChiSquare"
            "JmhDecTree"
            "JmhGaussMix"
            "JmhLogRegression"
            "JmhMovieLens"
            "JmhNaiveBayes"
            "JmhPageRank"
            "JmhDbShootout"
            "JmhFjKmeans"
            "JmhFutureGenetic"
            "JmhMnemonics"
            "JmhParMnemonics"
            "JmhScrabble"
            "JmhNeo4jAnalytics"
            "JmhRxScrabble"
            "JmhDotty"
            "JmhScalaDoku"
            "JmhScalaKmeans"
            "JmhPhilosophers"
            "JmhScalaStmBench7"
            "JmhFinagleChirper"
            "JmhFinagleHttp")





for bench in ${BENCHMARKS[@]} ; do
	################   RUN BASELINE CONFIGURATION   ################################
	${BASELINE_JAVA} ${BASELINE_ARGS} ${COMMON_ARGS} -jar /wf/tools/renaissance-jmh-0.16.0.jar -rf json -rff baseline-${bench}.json ${JDKMICRO_ARGS} ${bench}
	 
	# sleep 120

	################   RUN TREATMENT CONFIGURATION   ###############################
	${TREATMENT_JAVA} ${TREATMENT_ARGS} ${COMMON_ARGS} -jar /wf/tools/renaissance-jmh-0.16.0.jar -rf json -rff treatment-${bench}.json ${JDKMICRO_ARGS} ${bench}
done
```

### OpenJDK "release" file content

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


### GraalVM "release" file content

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
