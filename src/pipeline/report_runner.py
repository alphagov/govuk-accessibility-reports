import csv
import pandas as pd
import math
import multiprocessing

from tqdm import tqdm

from multiprocessing import Pool, Manager, Process


def write_to_csv(q, csv_file_name, headers, buffer_size=500):
    # Create the output files
    csv_file = open(f"data/{csv_file_name}", "w")
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

        report_generators_with_queues = self.create_report_queues_by_generator(report_generators)
        report_writer_processes = self.initialize_report_writers(report_generators_with_queues)

        total_content_items = len(preprocessed_content_items)
        print(f"Content item length: {total_content_items}")

        required_iterations = self.get_iterations_for_batch_size(total_content_items, self.content_item_batch_size)
        content_items_iterator = preprocessed_content_items.iterrows()

        num_work, chunksize = self.get_options_for_multiprocessing(total_content_items)

        for iteration in range(0, required_iterations):
            print(f"Starting batch {iteration + 1}")

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

        self.finalize_queues(report_generators_with_queues.values())
        self.wait_for_report_writers_processes_to_terminate(report_writer_processes)

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

    def initialize_report_writers(self, report_queues_by_generator):
        report_writer_processes = []

        for generator, queue in report_queues_by_generator.items():
            report_writer_processes.append(self.initialize_writer_process(write_to_csv, queue, generator.filename,
                                                                          generator.headers))

        return report_writer_processes

    def get_options_for_multiprocessing(self, total_content_items):
        worker_multiplier = 8 if self.turbo_mode else 0.8
        num_work = int(math.ceil(multiprocessing.cpu_count() * worker_multiplier))  # * 8
        chunksize, remainder = divmod(total_content_items, num_work)
        if remainder:
            chunksize += 1

        return num_work, chunksize

    @staticmethod
    def finalize_queues(queues):
        for queue in queues:
            queue.put(None)
            print("Closing pool, pushing None value to queue")

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
                    queue.put(report_generator.process_page(content_item, html))

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
