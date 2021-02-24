import argparse
import importlib
import os
import time
import runpy

from src.pipeline.runner_config import RunnerConfig
from src.pipeline.report_runner import ReportRunner
from definitions import ROOT_DIR


def initialise_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("report_config_filename", metavar="report-config-filename",
                        help="filename of the report config to use for generating reports")

    return parser


def get_class_instance(module_name, klass):
    print(f"Module name: {module_name}")

    cls = getattr(importlib.import_module(module_name), klass)

    print(f"Adding report for class {klass}")

    return cls()


if __name__ == "__main__":
    parser = initialise_parser()
    args = parser.parse_args()

    path = os.path.join(ROOT_DIR, f"config/{args.report_config_filename}")
    config = RunnerConfig(path)

    reports = []
    for report in config.reports:
        if report.skip:
            print(f"Skipping report: {report.name}")
            continue

        print(f"Loading report: {report.name}")
        module_name = report.filename.replace('.py', '')
        reports.append(get_class_instance(f"src.report_generators.{module_name}", report.klass))

    if not any(reports):
        print("No reports to run, exiting...")
        exit(0)

    # Print config settings for visual confirmation
    print(str(config))

    start_time = time.time()
    print(f"Starting processing at {time.strftime('%H:%M:%S')}")

    runner = ReportRunner(config)
    runner.run(reports)

    # Run post processing scripts
    for report in reports:
        if report.postprocess:
            print(f"Applying postprocessing of {report.postprocess}")
            runpy.run_path(f"src/report_generators/{report.postprocess}")

    end_time = time.time() - start_time
    print("Done")
    print(f"Took {end_time}s")
