#!/bin/bash

```
BASELINE_JAVA="/wf/tools/amazon-corretto-21.0.9.4.1-linux-aarch64/bin/java"
TREATMENT_JAVA="/wf/tools/graalvm-ce-ristretto-21/bin/java"

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

JDKMICRO_ARGS="-f 1 -wi 8"

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


################ Sets a bunch of configs to make the experiment more producible #####################
# source no_noise.sh



for bench in ${BENCHMARKS[@]} ; do
	################   RUN BASELINE CONFIGURATION   ################################
	${BASELINE_JAVA} ${BASELINE_ARGS} ${COMMON_ARGS} -jar /wf/tools/renaissance-jmh-0.16.0.jar -rf json -rff baseline-${bench}.json ${JDKMICRO_ARGS} ${bench}
	 
	# sleep 120

	################   RUN TREATMENT CONFIGURATION   ###############################
	${TREATMENT_JAVA} ${TREATMENT_ARGS} ${COMMON_ARGS} -jar /wf/tools/renaissance-jmh-0.16.0.jar -rf json -rff treatment-${bench}.json ${JDKMICRO_ARGS} ${bench}
done
```

```
IMPLEMENTOR="Amazon.com Inc."
IMPLEMENTOR_VERSION="Corretto-21.0.9.4.1"
JAVA_RUNTIME_VERSION="21.0.9+4-Nightly"
JAVA_VERSION="21.0.9"
JAVA_VERSION_DATE="2025-08-22"
LIBC="gnu"
MODULES="java.base java.compiler java.datatransfer java.xml java.prefs java.desktop java.instrument java.logging java.management java.security.sasl java.naming java.rmi java.management.rmi java.net.http java.scripting java.security.jgss java.transaction.xa java.sql java.sql.rowset java.xml.crypto java.se java.smartcardio jdk.accessibility jdk.internal.jvmstat jdk.attach jdk.charsets jdk.internal.opt jdk.zipfs jdk.compiler jdk.crypto.ec jdk.crypto.cryptoki jdk.dynalink jdk.internal.ed jdk.editpad jdk.hotspot.agent jdk.httpserver jdk.incubator.vector jdk.internal.le jdk.internal.vm.ci jdk.internal.vm.compiler jdk.internal.vm.compiler.management jdk.jartool jdk.javadoc jdk.jcmd jdk.management jdk.management.agent jdk.jconsole jdk.jdeps jdk.jdwp.agent jdk.jdi jdk.jfr jdk.jlink jdk.jpackage jdk.jshell jdk.jsobject jdk.jstatd jdk.localedata jdk.management.jfr jdk.naming.dns jdk.naming.rmi jdk.net jdk.nio.mapmode jdk.random jdk.sctp jdk.security.auth jdk.security.jgss jdk.unsupported jdk.unsupported.desktop jdk.xml.dom"
OS_ARCH="aarch64"
OS_NAME="Linux"
SOURCE=".:git:20640cdde405+"
```

```
IMPLEMENTOR="Amazon.com Inc."
IMPLEMENTOR_VERSION="1.0.1348.0"
JAVA_RUNTIME_VERSION="21.0.8+9-LTS"
JAVA_VERSION="21.0.8"
JAVA_VERSION_DATE="2025-07-15"
LIBC="gnu"
MODULES="java.base java.logging jdk.internal.vm.ci jdk.unsupported org.graalvm.collections java.management jdk.management org.graalvm.truffle.compiler org.graalvm.word jdk.internal.vm.compiler com.oracle.graal.graal_enterprise org.graalvm.nativeimage com.oracle.svm.enterprise.truffle com.oracle.svm.extraimage_enterprise com.oracle.svm.svm_enterprise com.oracle.svm_enterprise.ml_dataset com.oracle.truffle.enterprise com.oracle.truffle.enterprise.svm java.compiler java.datatransfer java.xml java.prefs java.desktop java.instrument java.security.sasl java.naming java.rmi java.management.rmi java.net.http java.scripting java.security.jgss java.transaction.xa java.sql java.sql.rowset java.xml.crypto java.se java.smartcardio jdk.accessibility jdk.internal.jvmstat jdk.attach jdk.charsets jdk.internal.opt jdk.zipfs jdk.compiler jdk.crypto.ec jdk.crypto.cryptoki jdk.dynalink jdk.internal.ed jdk.editpad jdk.hotspot.agent jdk.httpserver jdk.incubator.vector jdk.internal.le jdk.internal.vm.compiler.management jdk.jartool jdk.javadoc jdk.jcmd jdk.management.agent jdk.jconsole jdk.jdeps jdk.jdwp.agent jdk.jdi jdk.jfr jdk.jlink jdk.jpackage jdk.jshell jdk.jsobject jdk.jstatd jdk.localedata jdk.management.jfr jdk.naming.dns jdk.naming.rmi jdk.net jdk.nio.mapmode jdk.random jdk.sctp jdk.security.auth jdk.security.jgss jdk.unsupported.desktop jdk.xml.dom org.graalvm.extraimage.builder"
OS_ARCH="aarch64"
OS_NAME="Linux"
SOURCE="compiler:None java-benchmarks:None regex:None sdk:None substratevm:None truffle:None vm:None"
GRAALVM_VERSION="23.1.8"
COMMIT_INFO={}
```
