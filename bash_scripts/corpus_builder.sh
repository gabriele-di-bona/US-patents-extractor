#!/bin/bash
#$ -cwd
#$ -t 1
#$ -j y
#$ -pe smp 1
#$ -l h_vmem=150G
#$ -l highmem
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

# Load java and run maven
module load java/17.0.0
export JAVA_HOME=/share/apps/centos7/java/17.0.0
export PATH=$PATH:$JAVA_HOME/bin/
export M2_HOME=$PROJECT_ROOT_FOLDER/maven/apache-maven-3.8.6 # change to the folder where your jave is saved
export M2=$M2_HOME/bin
export MAVEN_OPTS='-Xms256m -Xmx512m'
export PATH=$M2:$PATH

# Download whole corpus. If specific date, provide range in format "yyyymmdd-yyyymmdd"
# For some reason, the end date to download is one more than the final date included.
# Therefore, be aware that if we are not in 2023, if you use 20221231 as final date,
# it will try to scrape 2023, which doesn't exist, therefore giving error.
# ==> Write 20221230 as final date to scrape until end of 2022.
DATE="19760102-20221230"

DOWNLOAD_ROOT_FOLDER="${PROJECT_ROOT_FOLDER}/bulk_data/"
mkdir -p $DOWNLOAD_ROOT_FOLDER


cd $PATENT_EXTRACTOR_FOLDER # Run next command from the PATENT_EXTRACTOR_FOLDER
java -cp BulkDownloader/target/BulkDownloader-0.0.1-SNAPSHOT.jar:BulkDownloader/target/dependency-jars/* \
-Dlog4j.configuration=file:BulkDownloader/target/classes/log4j.properties \
gov.uspto.bulkdata.cli2.BulkData --type grant --date $DATE --outdir "${DOWNLOAD_ROOT_FOLDER}" --async true

# Other parameters that can be set
#
# type: [application, grant, gazette]    requited;  patent document type
# date     required; 20140101-20161231
# limit     download limit
# skip      skip over limit
# async     Async Downloads
# filename  specific bulk file name to download
# outdir    directory to download to.
#
