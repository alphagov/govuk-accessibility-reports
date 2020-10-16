import csv
import pandas as pd
import math
import multiprocessing
import os
import shutil
import time
import uuid

from definitions import ROOT_DIR
from multiprocessing import Pool, Manager, Process
from tqdm import tqdm


def write_to_csv(q, csv_file_name, headers, buffer_size=500):
    # Create the output files
    csv_file = open(f"tmp/{csv_file_name}/{uuid.uuid4()}.csv", "w")
    csv_writer = csv.writer(csv_file)

    # Write headers
    csv_writer.writerow(headers)

    output = []

    while True:
        message = q.get()

        if message is None:
            if len(output) > 0:
                csv_writer.writerows(output)

            break

        output.append(message)
        if len(output) >= buffer_size:
            csv_writer.writerows(output)
            output = []


class ReportRunner:

    def __init__(self, config):
        self.turbo_mode = config.turbo_mode
        self.preprocessed_content_store_path = config.preprocessed_content_store_path
        self.html_content_dir_path = config.html_content_dir_path
        self.content_item_batch_size = config.content_item_batch_size
        self.csv_writer_buffer_size = config.csv_writer_buffer_size
        self.total_content_items = config.total_content_items
        self.manager = Manager()

    def run(self, report_generators):
        print(f"Reading {self.total_content_items} content items from the preprocessed content store...")
        preprocessed_content_items = pd.read_csv(self.preprocessed_content_store_path, sep="\t", compression="gzip",
                                                 low_memory=False, chunksize=self.total_content_items
                                                 )
        print("Finished reading from the preprocessed content store!")
        preprocessed_content_items = next(preprocessed_content_items)

        total_content_items = len(preprocessed_content_items)
        print(f"Content item length: {total_content_items}")

        num_work, chunksize = self.get_options_for_multiprocessing(total_content_items)

        report_generators_with_queues = self.create_report_queues_by_generator(report_generators)
        report_writer_processes = self.initialize_report_writers(report_generators_with_queues, num_work)

        required_iterations = self.get_iterations_for_batch_size(total_content_items, self.content_item_batch_size)
        content_items_iterator = preprocessed_content_items.iterrows()

        for iteration in range(0, required_iterations):
            print(f"Starting batch {iteration + 1}")
            start_time = time.time()

            content_item_tuples = self.create_batched_input_for_multiprocessing(content_items_iterator,
                                                                                report_generators_with_queues,
                                                                                total_content_items)

            print(f"Created batch of {len(content_item_tuples)} tuples")

            with Pool(num_work) as pool:
                pool.starmap(self.multiprocess_content_items,
                             [content_item_tuple for content_item_tuple in tqdm(content_item_tuples)],
                             chunksize=chunksize)
                pool.close()
                pool.join()

            elapsed_time_in_seconds = time.time() - start_time
            print(f"Took {elapsed_time_in_seconds}s to process batch {iteration + 1}")

        self.finalize_queues_for_report_writers(report_generators_with_queues.values(), num_work)
        self.wait_for_report_writers_processes_to_terminate(report_writer_processes)
        self.create_reports_from_temporary_files(report_generators)

    def create_batched_input_for_multiprocessing(self, content_items_iterator, report_generators_with_queues,
                                                 total_content_items):
        tuples = []

        end_content_item_index = total_content_items - 1

        for i in range(0, self.content_item_batch_size):
            preprocessed_content_item_tuple = next(content_items_iterator)

            tuples.append(
                (preprocessed_content_item_tuple[1], self.html_content_dir_path, report_generators_with_queues))

            if preprocessed_content_item_tuple[0] == end_content_item_index:
                print(f"Reached end of the input file at index {end_content_item_index}")
                break

        return tuples

    def create_report_queues_by_generator(self, report_generators):
        queues_by_generator = {}

        for generator in report_generators:
            report_queue = self.manager.Queue()
            queues_by_generator[generator] = report_queue

        return queues_by_generator

    def initialize_report_writers(self, report_queues_by_generator, number_of_workers_per_report):
        report_writer_processes = []

        # Create temporary dir for partial CSVs
        os.mkdir(os.path.join(ROOT_DIR, 'tmp'))

        for generator, queue in report_queues_by_generator.items():
            os.mkdir(os.path.join(ROOT_DIR, f"tmp/{generator.filename}"))

            # Create a csv writer process for each of the report workers we'll be using for this report
            for i in range(number_of_workers_per_report):
                report_writer_processes.append(self.initialize_writer_process(write_to_csv, queue, generator.filename(),
                                                                              generator.headers()))

        return report_writer_processes

    def get_options_for_multiprocessing(self, total_content_items):
        worker_multiplier = 8 if self.turbo_mode else 0.8
        num_work = int(math.ceil(multiprocessing.cpu_count() * worker_multiplier))  # * 8
        chunksize, remainder = divmod(total_content_items, num_work)
        if remainder:
            chunksize += 1

        return num_work, chunksize

    @staticmethod
    def create_reports_from_temporary_files(report_generators):
        for report_generator in report_generators:
            temporary_dir = os.path.join(ROOT_DIR, f"tmp/{report_generator.filename}")
            output_path = os.path.join(ROOT_DIR, f"data/{report_generator.filename}")

            csv_dataframes = [pd.read_csv(os.path.join(temporary_dir, temporary_csv))
                              for temporary_csv in os.listdir(temporary_dir)]
            pd.concat(csv_dataframes).sort_values(by=['base_path'])\
                .to_csv(output_path, index=False, columns=report_generator.headers)

        # Delete temporary dir
        shutil.rmtree(os.path.join(ROOT_DIR, 'tmp'))

    @staticmethod
    def finalize_queues_for_report_writers(queues, number_of_workers_per_report):
        for queue in queues:
            [queue.put(None) for _i in range(number_of_workers_per_report)]

            print("Closing pool for all workers, pushing None value to queue")

    @staticmethod
    def get_iterations_for_batch_size(total_content_items, batch_size):
        return math.ceil(total_content_items / batch_size)

    @staticmethod
    def initialize_writer_process(target, queue, filename, headers):
        process = Process(target=target, args=(queue, filename, headers))
        process.daemon = True
        process.start()

        return process

    @staticmethod
    def multiprocess_content_items(content_item, base_html_content_path, report_generators):
        try:
            html_file_path = f"{base_html_content_path}{content_item['base_path']}.html"

            with open(html_file_path, "r") as html_file:
                html = html_file.read()

                for report_generator, queue in report_generators.items():
                    # Allow the generators to do what they will with the output, rather than saving output here
                    # This is because a generator might wish to skip certain pages, so we shouldn't mandate an output
                    # for every page, and we don't want to introduce unnecessary logic here to second-guess what the
                    # generator may or may not return
                    result = report_generator.process_page(content_item, html)

                    if any(result):
                        queue.put(result)

            return

        except IOError:
            # Couldn't load the path, it could be that the content no longer exists / exists in the preprocessed store
            # but didn't exist when the mirror back-ups were created
            pass

    @staticmethod
    def wait_for_report_writers_processes_to_terminate(processes):
        for process in processes:
            print("Waiting on report writer process to finish")
            process.join()
