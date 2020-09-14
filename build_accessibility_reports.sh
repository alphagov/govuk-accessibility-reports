#!/bin/bash

usage="Script to build the Knowledge Graph data

The following options are available:
  -c    Report config filename (Required)
  -d    Database platform bucket name  (Required)
  -h    Show this help message"

while getopts c:d:h: option
do
case "${option}"
in
c) report_config_filename=${OPTARG};;
d) data_platform_bucket_name=${OPTARG};;
h) echo "$usage"
   exit;;
esac
done

date_today=$(date '+%F')

export REPO_DIR=$PWD
export DATA_DIR=$PWD/data
export CONFIG=$PWD/config

mirror_bucket_prefix=$(/usr/local/bin/aws ssm get-parameter --name govuk_accessibility_reports_mirror_bucket_prefix --query "Parameter.Value" --region eu-west-1 | jq -r '.')

cd /var/data
mkdir govuk_mirror_html_content

aws configure set default.s3.max_concurrent_requests 5

# Download the mirror content
aws s3 cp s3://govuk-staging-mirror-replica/${mirror_bucket_prefix} /var/data/govuk_mirror_html_content --recursive

# Download the preprocessed content store
python_formatted_date=$(date '+%d%m%y')
aws s3 cp s3://${data_platform_bucket_name}/knowledge-graph/${date_today}/preprocessed_content_store_${python_formatted_date}.csv.gz /var/data/preprocessed_content_store.csv.gz

cd /var/data/github/govuk-accessibility-reports

# Install dependencies
pip install -r requirements.txt

# Build the graph data
python3.7 -m src.scripts.run_accessibility_reports ${report_config_filename}

# Get graph data directory
cd data

# Upload reports
echo "Uploading reports..."
aws s3 cp $DATA_DIR s3://${data_platform_bucket_name}/accessibility-reports/${date_today} --recursive
