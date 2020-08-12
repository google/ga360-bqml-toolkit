# GA360/BQML Toolkit


*Objective*: Provide out of the box and sample code to understand user behavior and build models (with BQML) based on data from the Google Analytics 360 BigQuery Export.

This is not meant to be an exhaustive solution or cover every use case. No two
models are the same, so you should tweak with your own timelines and business
case in mind.

For more on BQML, see the
[documentation](https://cloud.google.com/bigquery-ml/docs).

## Components

### Queries

(TODO) - samchu@ to add explanation of the queries included

### Python script

The Python script included will automate the process of reading in the base
feature set and model training SQL files, passing in the necessary parameters,
running the queries in BigQuery, and saving the results.

## Installation

### Pull in GA360 data

(TODO) - samchu@ to add GA setup info

#### Modify the queries (optional)

(TODO) - samchu@ to add some info about how the queries could be modified (and
what the use cases for that would be)

### Running the Python script

To run, you need a few pieces of information: 
* `project_id`: the ID of your GCP project 
* `ga_dataset`: the BigQuery dataset where you have stored your GA export
data 
* `ga_table_prefix`: the prefix of the BigQuery table where you stored your
GA export data (This should be a set of partitioned tables. The script is
already set up to pass in a wildcard so that it will read in all the partitioned
tables)

Then, run this command in Cloud Shell: `python3 create_queries.py [project_id]
[ga_dataset] [ga_table_prefix]`

For more advanced usage you can modify the script (for example, to use custom
parameters). Simply edit the parameters at the beginning of the file.

### What next?

Now that you have your BQML model set up, the next step is activation. Check out
[Project Modem](https://github.com/google/modem) if you would like to create an
automated pipeline for activating the data from your model.
