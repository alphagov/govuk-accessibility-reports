# GOV.UK Accessibility Reports

Project containing numerous report generators to monitor accessibility on GOV.UK.

## What it is and how it works

This project contains a number of report generators, which each create a specific accessibility report; this might be
finding all pages where the headings of a page don't follow a particular ordering, or all pages that have links with
the same URLs but different link texts.

Typically, generating these reports require access to two sources of data to generate the reports - the content items
which represent GOV.UK pages and the HTML of said pages. To get this from GOV.UK itself would require over 500K HTTP
requests, which would take a long time to compute, would be an unnecessary overhead for the serving applications and is
prone to numerous errors (timeouts, exceeding rate-limits etc). As the number of accessibility reports we generate
increases, processing each of them in this way becomes more unsustainable.

The purpose of this project, the raison d'être, is to create an alternative approach to generating these reports.
The first way it does this is by relying on a copy of the GOV.UK mirror content and preprocessed content store locally,
thereby eliminating all HTTP requests. Secondly, it runs all of the report generators simultaneously and streams the
outputs to separate report files on disk as the process is running. It achieves this by using the `multiprocessing`
package to process each batch of content items, with each batch running over all of the mirror content (made of up
HTML files) exactly once

### The technical details

The following is a technical breakdown of the report generation process:

- First, the `ReportRunner` takes all of the content items from the preprocessed content store and splits them up into
batches (controlled by the `content_item_batch_size` setting in the report config).
- Each batch is then processed in parallel by the `multiprocessing` package, with each of the report generators run
for a given content item and HTML content of that particular page and the result written to a multiprocessing `Queue`.
- The `Queue` for each report generator is consumed by a separate process which writes to the output CSV file for
that report.

Through this structure, we can run multiple report generators in parallel have them write their output to a `Queue`
continuously, and have the output CSVs written asynchronously. This helps to manage memory consumed on the machine
as we're always writing to output CSVs (in tandem with the config settings to manage batch and buffer sizes).

## Prerequisites

To use the report runner, you'll need to have a local copy of the preprocessed content store (available from the S3
`govuk-data-infrastructure-integration` bucket, with prefix
`knowledge-graph/DATE_OF_YOUR_CHOICE/preprocessed_content_store_DATE_OF_YOUR_CHOICE.csv.gz`). You should download this
file via the `gds-cli` + AWS CLI to avoid issues when downloading via the console, an example of which might look like:

`gds aws govuk-integration-poweruser aws s3 cp s3://govuk-data-infrastructure-integration/knowledge-graph/2020-08-14/
preprocessed_content_store_140820.csv.gz /Users/joebloggs/Downloads/preprocessed_content_store_140820.csv.gz`

You'll also need a copy of the mirror content (a collection of HTML files used by the mirrors). You should use the
`govuk-production-mirror-replica` bucket. This should also be downloaded via the `gds-cli` + AWS CLI (you may wish to
use the `--assume-role-ttl` flag as the mirror is a large download and can take some time - setting to `180m`
(180 minutes) should be reasonable). An example command might look like:

`gds aws govuk-production-poweruser --assume-role-ttl 180m aws s3 cp s3://govuk-production-mirror-replica/www.gov.uk
/User/joebloggs/Downloads/govuk-production-mirror-replica --recursive`

## Getting started

To get started, you should be running Python 3.7. Navigate to the project root (where this README is located) and
install required packages via `pip install -r requirements.txt`.

Next, you should configure which reports you'd like to generate by going into the appropriate config file inside of the
 `config` directory and setting the `skip` property of the reports you require to `false`. No reports are set to run
 by default, in order to ensure that only the reports you require are generated (as generating more reports results
 in a longer processing time).

Once you've enabled the reports you'd like to generate in the config, run the following to generate the reports:

`python -m src.scripts.run_accessibility_reports <REPORT CONFIG FILENAME>`

substituting `<REPORT CONFIG FILENAME>` for the report config you wish to use from the `config` directory.

This may take some time and you'll be informed of progress. Once complete, the reports will be saved in the `data`
directory.

For some reports, some post-processing needs to be done before sharing with the Accessibility team. Where a report
requires this, then you will find it under `src/report_generators/<report_name>_postprocess/py`.

For example, if you want to create the `src/report_generators/attachment_type_report_generator.py` report, then run this
report as normal and then run `src/report_generators/attachment_type_report_postprocess.py` to produce the reports for the
Accessibility team.

## Creating a new report

To create a new report, you should first add a report generator into the `report_generators` directory and inherit from
the `BaseReportGenerator`. You will then have to implement three methods:

- `filename()`: the name of the file that you want the report to be saved out as (must include the `.csv` extension)
- `headers()`: an array of the names of the headers that your report should contain
- `preprocess_page(content_item, html)`: the main component of your report generator, which takes a content item from
the preprocessed content store and the HTML content of that page, runs some computation and returns an array which
corresponds to the output for that page to be included in the report CSV.
    - You can return an empty array (`[]`) if the page you're processing should not be recorded in the CSV for whatever
    reason / if you want to skip particular pages etc.

Once you have created the report generator, you should add a new entry to the `reports` property to the various
configs that can be used to run the reports. These can be found in the `config` directory, and each report entry should
contain:

- `name`: the human-friendly name of the report to be used in console output (i.e. `Heading accessibility report`)
- `filename`: the name of the Python module for your report generator (including the `.py` extension) (i.e
`heading_ordering_report_generator.py`)
- `class`: the name of the class for your report generator (i.e. `HeadingOrderingReportGenerator`)
- `skip`: whether to run or skip this report - ensure this is set to `true` when committed

For testing, you may wish to set the `total_content_items` property in the config file to a low
number (i.e. `1000`). This limits the report generators run to only be run against the first `total_content_items`
content items, meaning you'll get output faster.

## Configuration settings

There are a number of configuration settings defined in the configuration files (in the `config` directory), under
the `settings` property (the `reports` property is covered in the previous section)

- `turbo_mode`: setting this to `true` increases the number of workers (processes) used when running the report
generators for a batch of preprocessed content items, to 8x the number of available CPUs on the machine (defaults to
`false` so that your machine doesn't become unresponsive, which runs at 0.8x the number of available CPUs)
- `html_content_dir_path`: the absolute path to the directory containing the HTML content from the GOV.UK mirrors
- `preprocessed_content_store_path`: the absolute path to the preprocessed content store (gzipped) file
- `total_content_items`: the total number of content items to process. Set to a low number for testing and a high
number when running the report for real (defaults to `1000`)
- `content_item_batch_size`: the number of content items that should be contained in a batch, to be parallel-executed
by the `multiprocessing` package (defaults to `50000`)
- `csv_writer_buffer_size`: the number of rows to cache in-memory for each report before writing them out to the
appropriate report CSV (defaults to `500`)

##  Installing pre-commit hooks

This repo uses the Python package `pre-commit` (https://pre-commit.com) to manage pre-commit hooks. Pre-commit hooks are
actions which are run automatically, typically on each commit, to perform some common set of tasks. For example, a
pre-commit hook might be used to run any code linting automatically, providing any warnings before code is committed,
ensuring that all of our code adheres to a certain quality standard.

For this repo, we are using `pre-commit` for a number of purposes:
- Checking for any secrets being committed accidentally
- Checking for any large files (over 5MB) being committed
- Cleaning Jupyter notebooks, which means removing all outputs and execution counts

We have configured `pre-commit` to run automatically on _every commit_. By running on each commit, we ensure
that `pre-commit` will be able to detect all contraventions and keep our repo in a healthy state.

In order for `pre-commit` to run, action is needed to configure it on your system.

- Run `pip install -r requirements-dev.txt` to install `pre-commit` in your Python environment
- Run `pre-commit install` to set-up `pre-commit` to run when code is _committed_

### Setting up a baseline for the `detect-secrets` hook (if one doesn't already exist)

The `detect-secrets` hook requires that you generate a baseline file if one is not already present within the root
directory. This is done via running the following at the root of the repo:

`detect-secrets scan > .secrets.baseline`

Next, audit the baseline that has been generated by running:

`detect-secrets audit .secrets.baseline`

When you run this command, you'll enter an interactive console and be presented with a list of high-entropy string /
anything which _could_ be a secret, and asked to verify whether or not this is the case. By doing this, the hook will
be in a position to know if you're later committing any _new_ secrets to the repo and it will be able to alert you
accordingly.

### If pre-commit detects secrets during commit:

If pre-commit detects any secrets when you try to create a commit, it will detail what it found and where to go to check
the secret.

If the detected secret is a false-positive, you should update the secrets baseline through the following steps:

- Run `detect-secrets scan --update .secrets.baseline` to index the false-positive(s)
- Next, audit all indexed secrets via `detect-secrets audit .secrets.baseline` (the same as during initial set-up, if a
secrets baseline doesn't exist)
- Finally, ensure that you commit the updated secrets baseline in the same commit as the false-positive(s) it has been
updated for

If the detected secret is actually a secret (or other sensitive information), remove the secret and re-commit. There is
no need to update the secrets baseline in this case.

If your commit contains a mixture of false-positives and actual secrets, remove the actual secrets first before
updating and auditing the secrets baseline.

###  Note on Jupyter notebook cleaning

It may be necessary or useful to keep certain output cells of a Jupyter notebook, for example charts or graphs
visualising some set of data. To do this, add the following comment at the top of the input block:

`# [keep_output]`

This will tell `pre-commit` not to strip the resulting output of this cell, allowing it to be committed.

## Setting environment variables

Environment variables can be set locally using a `.envrc` file. This should only be used for local development / running
of the reports and is ignored by the `.gitignore` file.

### Creating `.envrc`

You can create the `.envrc` file by running:
```
./make_envrc.sh
```

Once the file has been created, you should update all of the vars described in the previous section, with the exception
of `DATA_DIR` which will be set automatically.

### Loading environment variables from `.envrc`

To load environment variables from `.envrc`, it is assumed that you have `direnv` installed - https://direnv.net.
`direnv` is an extension for your shell, which loads environment variables from `.envrc` files automatically when you
navigate to a directory containing such a file, as well as updating those environment variables in your shell whenever
they change in the file itself.

Once installed and hooked into your terminal, navigate to this project directory. You should then see the following
output:

```
direnv: loading ~/govuk/govuk-user-journey-models/.envrc
direnv: export +DATA_DIR (plus any additional environment variables)
```

If you don't see this, try running `direnv allow` to enable `direnv` to access the `.envrc` file (you will only need to
do this once.)

## Exploring the preprocessed_content_store file

The `preprocessed_content_store_*.csv.gz` can be explored using the command-line
tool [visidata](https://www.visidata.org/).  The following command opens the
file without decompressing the whole thing.

```sh
zcat < preprocessed_content_store_011020.csv.gz | vd --filetype=csv --csv-delimiter=$'\t' -
```

You can expand the JSON columns by highlighting the column and typing
`=eval(nameofcolumn)`, for example, `=eval(details)`, and then typing `(` to
expand the new column that was created.  Type `)` on an expanded column to
collapse it.
