from multiprocessing.pool import ThreadPool
import boto3
import boto3.session
import pandas as pd
import json
import math
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv
import os.path

def process(item):
    print(f"starting {item['content_item']['base_path']}")
    start_time = time.time()
    sagemaker_client = boto3.session.Session().client('sagemaker-runtime', 'eu-west-1')
    entities = []
    govner_version = "-1"
    try:
        response = sagemaker_client.invoke_endpoint(
            EndpointName="govner-endpoint",
            ContentType="application/json",
            Accept="application/json",
            Body= json.dumps({"text": item['text']}),
        )
        response = json.loads(response['Body'].read())
        entities = response['results']['entities']
        govner_version = response['results']['govner_version']
    except:
        pass
    csv_file = open(item['filename'], "w")
    csv_writer = csv.writer(csv_file)
    # Write headers
    csv_writer.writerow(['base_path', 'entities', 'updated_at', 'govner_version'])
    csv_writer.writerow([item['content_item']['base_path'], entities, datetime.now(), govner_version])
    print(f"Got entities {item['content_item']['base_path']}, time {time.time() - start_time}")

def get_iterations_for_batch_size(total_content_items, batch_size):
    return math.ceil(total_content_items / batch_size)

def extract_texts(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in ['b', 'i', 'u', 'a', 'abbr']:
        for match in soup.findAll(tag):
            match.replaceWithChildren()
            # If we don't extract them, the old tags stick
            # around and mess up the soup.strings call
    [x.extract() for x in soup.findAll('script')]
    soup = BeautifulSoup(str(soup), 'html.parser')
    return ". ".join(list(soup.strings))

def filename_for_content_item(content_item):
    return f"tmp/multithreaded/{content_item['content_id']}.csv"

total_content_items = 3000
html_content_dir_path = "/Users/oscarwyatt/govuk/govuk-knowledge-extractor/govuk-production-mirror-replica"
preprocessed_content_store_path = "/Users/oscarwyatt/govuk/govuk-knowledge-graph/data/preprocessed_content_store_070920.csv.gz"
content_item_batch_size = 5
print(f"Reading {total_content_items} content items from the preprocessed content store...")
all_content_items = pd.read_csv(preprocessed_content_store_path, sep="\t", compression="gzip",
                                         low_memory=False)

print("Finished reading from the preprocessed content store!")
all_content_items = all_content_items[all_content_items['publishing_app'] == 'publisher']
preprocessed_content_items = pd.DataFrame()
for index, content_item in all_content_items.iterrows():
    if os.path.isfile(filename_for_content_item(content_item)) == False:
        preprocessed_content_items = preprocessed_content_items.append(content_item)


required_iterations = get_iterations_for_batch_size(total_content_items, content_item_batch_size)

batch_start_index = 0
for iteration in range(0, required_iterations):
    print(f"Starting batch {iteration + 1}")
    items_in_batch = preprocessed_content_items[batch_start_index:batch_start_index + content_item_batch_size]
    data_for_batch = []
    for index, content_item in items_in_batch.iterrows():
        item = {
            "content_item": content_item,
            "filename": filename_for_content_item(content_item),
        }
        html_file_path = f"{html_content_dir_path}{content_item['base_path']}.html"
        try:
            with open(html_file_path, "r") as html_file:
                html = html_file.read()
                item["text"] = extract_texts(html)
            data_for_batch.append(item)
        except:
            pass
    pool = ThreadPool(processes=content_item_batch_size)
    pool.map(process, data_for_batch)
    batch_start_index += content_item_batch_size

temporary_dir = "tmp/multithreaded/"
output_path = "merged.csv"

merged = pd.DataFrame()
for i, temporary_csv in enumerate(os.listdir(temporary_dir)):
    print(i)
    try:
        df = pd.read_csv(os.path.join(temporary_dir, temporary_csv))
        merged = merged.append(df)
    except:
        pass
merged.to_csv(output_path, index=False, columns=['base_path', 'entities', 'updated_at', 'govner_version'])


