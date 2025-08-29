#!/bin/bash

#BASELINE_JAVA="/wf/tools/amazon-corretto-21.0.9.4.1-linux-aarch64/bin/java"
#TREATMENT_JAVA="/wf/tools/graalvm-ce-ristretto-21/bin/java"

BASELINE_JAVA="/wf/tools/amazon-corretto-25.0.0.32.1-linux-aarch64/bin/java"
TREATMENT_JAVA="/wf/tools/graalvm-community-openjdk-25+25.1/bin/java"

COMMON_ARGS="--add-opens=jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED"
BASELINE_ARGS="-Xms16G -Xmx16G -XX:+UnlockExperimentalVMOptions -XX:-EnableJVMCI"
TREATMENT_ARGS="-Xms16G -Xmx16G -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -XX:+UseJVMCICompiler -XX:+UseJVMCINativeLibrary"

JDKMICRO_ARGS="-wt 60 -it 120 -bt 16 -Dspecjvm.home.dir=/wf/SPECjvm2008 -ikv -ict -crf true -ctf true"

BENCHMARKS=("startup.helloworld"
	"startup.compiler.compiler"
	"startup.compiler.sunflow"
	"startup.compress"
	"startup.crypto.aes"
	"startup.crypto.rsa"
	"startup.crypto.signverify"
	"startup.mpegaudio"
	"startup.scimark.fft"
	"startup.scimark.lu"
	"startup.scimark.monte_carlo"
	"startup.scimark.sor"
	"startup.scimark.sparse"
	"startup.serial"
	"startup.sunflow"
	"startup.xml.transform"
	"startup.xml.validation"
	"compiler.compiler"
	"compiler.sunflow"
	"compress"
	"crypto.aes"
	"crypto.rsa"
	"crypto.signverify"
	"derby"
	"mpegaudio"
	"scimark.fft.large"
	"scimark.lu.large"
	"scimark.sor.large"
	"scimark.sparse.large"
	"scimark.fft.small"
	"scimark.lu.small"
	"scimark.sor.small"
	"scimark.sparse.small"
	"scimark.monte_carlo"
	"serial"
	"sunflow"
	"xml.transform"
	"xml.validation")


for bench in ${BENCHMARKS[@]} ; do
	################   RUN BASELINE CONFIGURATION   ################################
	${BASELINE_JAVA}  ${BASELINE_ARGS}  ${COMMON_ARGS} -jar /wf/SPECjvm2008/SPECjvm2008.jar ${JDKMICRO_ARGS} ${bench}
	 
	sleep 120

	################   RUN TREATMENT CONFIGURATION   ###############################
	${TREATMENT_JAVA} ${TREATMENT_ARGS} ${COMMON_ARGS} -jar /wf/SPECjvm2008/SPECjvm2008.jar ${JDKMICRO_ARGS} ${bench}
done

