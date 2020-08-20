# /***********************************************************************
# Copyright 2020 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Note that these code samples being shared are not official Google
# products and are not formally supported.
# ************************************************************************/
import argparse
import sys
import os
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud.bigquery import Table

# Default parameters
# Path to SQL queries. Update here if you have other queries
working_directory = os.getcwd()
feature_set_sql_path = "{}/sql/create_base_feature_set.sql".format(working_directory)
model_sql_path = "{}/sql/train_logistic_regression.sql".format(working_directory)

# Current timestamp (used to generate table names)
current_timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")

# Base Feature Set default parameters. This defaults to a one-year lookback and a 30-day scoring window
feature_set_table = "Base_Feature_Set_{}".format(current_timestamp)
end_date = "{}".format(datetime.now().strftime('%Y%m%d'))
start_date = "{}".format((datetime.now() - timedelta(days=365)).strftime('%Y%m%d'))
days_to_score = "30"

# Model default parameters
remove_fields = "ClientId" # Comma-separated list of fields to remove from model
model_destination_table = "BQML_Model_Output_{}".format(current_timestamp)
model_name = "BQML_Model_{}".format(current_timestamp)

def parse(argv):
  parser = argparse.ArgumentParser(description='Accepts Project ID and GA360 dataset.')
  parser.add_argument('project_id', type=str, help='Your GCP Project ID')
  parser.add_argument('ga_dataset', type=str, help='The dataset where you have your GA360 data')
  args = parser.parse_args()
  return args

def read_query_from_file(file_path):
  with open(file_path) as sqlFile:
      sql = sqlFile.read()
  return sql

def create_and_run_feature_set_query(client, sql, ga_table_ref, destination_table):
  sql = str(sql).replace("{start_date}", start_date).replace("{end_date}", end_date).replace("{ga_data_ref}", ga_table_ref).replace("{days_to_score}", days_to_score)
  job_config = bigquery.QueryJobConfig(destination=destination_table)
  query_job = client.query(sql, job_config=job_config)  # Make an API request.
  query_job.result()  # Wait for the job to complete.

  print("Query results loaded to the table {}".format(destination_table))

def create_and_run_model_query(client, sql, feature_set_table_ref, model_name):
  sql = str(sql).replace("{model_name}", model_name).replace("{remove_fields}", remove_fields).replace("{training_set}", feature_set_table_ref)
  job_config = bigquery.QueryJobConfig()
  query_job = client.query(sql, job_config=job_config)  # Make an API request.
  query_job.result()  # Wait for the job to complete.

  print("Model was created with the name {}".format(model_name))

def main(argv):
  args = parse(argv)
  # Store CLI args
  project_id = args.project_id
  ga_dataset = args.ga_dataset

  # Construct table references: 
  # GA360 BQ Export location
  ga_table_ref = "{}.{}.ga_sessions_*".format(project_id,ga_dataset) 

  # Location to save feature set
  feature_set_table_ref = "{}.{}.{}".format(project_id,ga_dataset,feature_set_table) 
  
  # Location to save BQML Model
  full_model_name = "{}.{}.{}".format(project_id,ga_dataset,model_name) 

  # Construct a BigQuery client object.
  client = bigquery.Client(project=project_id)

  # Create feature set query and query params and execute
  feature_set_sql = read_query_from_file(feature_set_sql_path)
  print("Feature set SQL has been read in.")
  print(create_and_run_feature_set_query(client, feature_set_sql, ga_table_ref, feature_set_table_ref))

  # Create model query and execute
  model_sql = read_query_from_file(model_sql_path)
  print("Model SQL has been read in")
  print(create_and_run_model_query(client, model_sql, feature_set_table_ref, full_model_name))

if __name__ == "__main__":
  main(sys.argv)

