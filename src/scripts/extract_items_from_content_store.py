import csv
import gzip
import sys

# The purpose of this script is to take a list of URLs and extract the
# preprocessed content items for those urls from the store into another csv file
# that can be passed to the report runner. This makes it quicker to test new and
# existing reports where you already know one URL with an issue they should
# handle.

gzipped_content_store_file_path = "downloads/preprocessed_content_store_230822.csv.gz"
target_file_path = "downloads/abridged_content_store_230822.csv.gz"
item_urls = [
  "/aaib-reports/1-1971-g-atek-and-g-ateh-15-august-1967",
  "/government/statistics/percentile-points-from-1-to-99-for-total-income-before-and-after-tax",
  "/government/organisations/hm-revenue-customs",
  "/anti-money-laundering-registration",
  "/ad-dalu-gordaliadau-budd-dal-plant"
]

csv.field_size_limit(sys.maxsize)

write_obj = gzip.open(target_file_path, mode='wt')
csv_writer = csv.writer(write_obj, delimiter='\t')

read_obj = gzip.open(gzipped_content_store_file_path, mode='rt')
csv_reader = csv.reader(read_obj, delimiter='\t')
header = next(csv_reader)
csv_writer.writerow(header)

line = 0
extracted_items = 0
for row in csv_reader:
  if row[0] in item_urls:
    print("\nFound target URL: ", row[0], flush=True)
    extracted_items += 1
    csv_writer.writerow(row)
  line += 1
  if line % 1000 == 0:
    print(".", end="", flush=True)

read_obj.close()
write_obj.close();

print("Total rows: ", line)
print("Extracted ", extracted_items, " of a desired ", len(item_urls))
