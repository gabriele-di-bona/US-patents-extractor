#!/bin/bash
#$ -cwd
#$ -t 1
#$ -j y
#$ -pe smp 1
#$ -l h_vmem=100G
# #$ -l highmem
#$ -l h_rt=240:0:0
# #$ -m bae
# Download USPTO Weekly Bulk Patent Dumps
#

# Go back to PatentPublicData folder
# This script is made to be run from "US-patents-extractor/bash_scripts/outputs/"
PROJECT_ROOT_FOLDER="../.."
cd $PROJECT_ROOT_FOLDER
PROJECT_ROOT_FOLDER=$(pwd) # subtitute with absolute path if needed
PATENT_EXTRACTOR_FOLDER="${PROJECT_ROOT_FOLDER}/PatentPublicData"


# download maven
mkdir maven
cd maven
wget https://dlcdn.apache.org/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.tar.gz
tar -xf apache-maven-3.8.6-bin.tar.gz
cd .. # to return to root

# load java and run maven
module load java/17.0.0
export JAVA_HOME=/share/apps/centos7/java/17.0.0 # change to the folder where your jave is saved
export PATH=$PATH:$JAVA_HOME/bin/
export M2_HOME=${PROJECT_ROOT_FOLDER}/maven/apache-maven-3.8.6
export M2=$M2_HOME/bin
export MAVEN_OPTS='-Xms256m -Xmx512m'
export PATH=$M2:$PATH
mvn --version

cd ${PATENT_EXTRACTOR_FOLDER}
mvn install -DskipTests