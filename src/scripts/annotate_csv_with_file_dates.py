import csv
import os
import time
from datetime import datetime

base_path = 'downloads/govuk-production-mirror-replica'
input_file = 'data/basic_heading_accessibility_report.csv'
output_file = 'data/basic_heading_accessibility_report_annotated.csv'

write_obj = open(output_file, mode='wt')
csv_writer = csv.writer(write_obj, delimiter=',')

read_obj = open(input_file, mode='rt')
csv_reader = csv.reader(read_obj, delimiter=',')

header = next(csv_reader)
header.insert(7, 'mirror_updated_at')
header.insert(8, 'diff')
csv_writer.writerow(header)

line = 0
for row in csv_reader:
  filename = base_path + row[0] + '.html'
  timestamp = os.path.getmtime(filename)
  dt = datetime.fromtimestamp(timestamp)
  updated_time = time.strptime(row[6],'%Y-%m-%d %H:%M:%S.000')
  updated_timestamp = time.mktime(updated_time)
  row.insert(7,dt)
  row.insert(8,timestamp - updated_timestamp)
  csv_writer.writerow(row)
  line += 1
  if line % 1000 == 0:
    print(".", end="", flush=True)

read_obj.close()
write_obj.close();

print("Total rows: ", line)
