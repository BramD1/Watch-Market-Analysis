'''
============================================================
Name: Bramantyo Anandaru Suyadi
Batch: HCK - 023
Objective: This is the DAG (Directed Acyclic Graph) program that is created to automate the extraction, transformation, and loading the data from PostgreSQL to ElasticSearch.
The data bellow are taken from the watch market dataset. 
Dataset link : https://www.kaggle.com/datasets/beridzeg45/watch-prices-dataset/data 
============================================================

'''


# Import Libraries
import pandas as pd
import numpy as np
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch
from datetime import datetime
'''
The functions of the libraries are:
1. Pandas is for creating and manipulating the data frame
2. Numpy is for creating and manipulating array, and also useful for computation
3. Airflow is used to automate the process below of extraction, transformation, and also loading to elasticnet
4. elastic search is use to store our data in the localhost API that will be used by Kibana later on
5. datetime is simply to just manipulate datetime data or set a datetime
'''

# deafult parameter
default_args = {
    'owner': 'Bram',
    'retry': None,
    'start_date': datetime(2024, 11, 2)
}

def extract(**context):
    '''
    In this function we will go through 4 processes:
    1. Connecting our local postgres database to the corresponding one in the airflow localhost
    2. Defining the dataframe in sql that is raw, so this is our "extraction" process
    3. saving the data we have extracted in csv to the corresponding path
    4. export the raw data to the next process of transformation
    '''
    # Connect to database
    source_hook = PostgresHook(postgres_conn_id='postgres_airflow')
    source_conn =source_hook.get_conn() 


    # Read data in sql
    data_raw = pd.read_sql('select * from table_m3', source_conn)

    # Save data in csv
    path = '/opt/airflow/dags/P2M3_Bramantyo_data_raw.csv'
    data_raw.to_csv(path, index=False)

    # Export path for raw data
    context['ti'].xcom_push(key='raw_data_path', value=path)

# function cleaning
def transform(**context):
    '''
    For this function, we are going through a lot more step because of the cleaning process. 
    First step is to get the task instance context to be used for the next step of getting the raw data from the path that is already defined.
    Before the cleaning process, we want to open our data path as dataframe similar as the previous function.
    Now for the cleaning process:
    1. Drop the columns that is deemed unecessary in accordance to business knowledge for luxury watch. Because the columns being dropped
    below has no affect to prices for luxury brands
    2. Drop rows with missing price value because we don't want missing values in the price columns, and inputting an aggregate or random value will be a breach of SOP for data analysis.
    3. We also don't want missing value in movement mechanism column so we must drop rows with missing values and to not fill it with any values
    4. The case material can be filled with random values, but ensure the values generated still holds the data as balanced as before.
    5. Year of production will be filled with median values because teh column is skewed
    6. The condition value will be filled with a certain value just to be safe and ensure the data is as balanced as before
    7. Water resistance will be filled with median value because of its skewness
    8. The crystal column will be filled with glass because it is the most common value
    9. The watch sold by seller column will be filled with 0 because that is the surest way to tell if a watch is sold or not (based on null values)
    10. Same with seller reviews
    11. Drop duplicates in our dataframe just to be safe
    12. Creating an id column for our great expectation of uniqueness
    13. Change the name of the column to make it easier
    After the process, we create our cleaned dataframe and saved it. After that, we export the path to be processed later on by the loading function.
    '''
    # Getting task instance context
    ti = context['ti']

    # Getting the path for the raw data
    data_path = ti.xcom_pull(task_ids='extract_data', key='raw_data_path')

    # Open as a dataframe
    data_raw = pd.read_csv(data_path)

    # cleaning 1: Drop unecessary columns
    data_raw = data_raw.drop(columns=['Availability', 'Shape', 'Gender', 'Active listing of the seller', 'Dial', 'Bracelet color', 'Face Area', 'Bracelet material', 'Clasp'], axis=1)
    
    # cleaning 2: drop null values in 'Price' column
    data_raw = data_raw.dropna(subset=['Price'], inplace=True)

    # cleaning 3: drop null values in 'Movement'
    data_raw = data_raw.dropna(subset=['Movement'], inplace=True)

    # cleaning 4: fill column 'Case material' with random values, but make sure the data is balanced
    category_counts = data_raw['Case material'].value_counts(normalize=True)
    missing_count = data_raw['Case material'].isnull().sum()
    random_fill = np.random.choice(category_counts.index, size=missing_count, p=category_counts.values)
    data_raw.loc[data_raw['Case material'].isnull(), 'Case material'] = random_fill

    # cleaning 5: fill column 'Year of Production with the median value
    data_raw['Year of production'] = data_raw['Year of production'].fillna(data_raw['Year of production'].median()).replace('.0', '').astype(int)

    # cleaning 6: fill column 'Condition' with the value seen below
    data_raw['Condition'] = data_raw['Condition'].fillna('Used (Incomplete)')

    # cleaning 7: fill column 'Water resistance' with the median value
    data_raw['Water resistance'] = data_raw['Water resistance'].fillna(data_raw['Water resistance'].median())

    # cleaning 8: fill column 'Crystal' with 'Glass'
    data_raw['Crystal'] = data_raw['Crystal'].fillna('Glass')

    # cleaning 9: fill column 'Watched sold by seller' with 0
    data_raw['Watches Sold by the Seller'] = data_raw['Watches Sold by the Seller'].fillna(0)

    # cleaning 10: do the same to the column 'Seller Review'
    data_raw['Seller Reviews'] = data_raw['Seller Reviews'].fillna(0)

    # cleaning 11: drop duplicates
    data_raw = data_raw.drop_duplicates()

    # cleaning 12: create index
    data_idx = len(data_raw)
    data_raw['id'] = range(1, data_idx+1)
    data_raw = data_raw.set_index('id')

    #cleaning Final: renaming columns
    data_raw.rename(columns={'Brand':'brand', 
                   'Movement': 'movement', 
                   'Case material': 'case_material', 
                   'Year of production': 'year_produced', 
                   'Condition': 'condition', 
                   'Scope of delivery': 'packaging', 
                   'Price': 'price',
                   'Water resistance': 'water_resistance', 
                   'Crystal': 'crystal', 
                   'Watches Sold by the Seller': 'sold',
                   'Fast Shipper': 'fast_shipping', 
                   'Trusted Seller': 'trusted_seller', 
                   'Punctuality': 'punctual', 
                   'Seller Reviews': 'review'}, inplace=True)
    data_clean = data_raw

    # Save clean data
    path = '/opt/airflow/dags/P2M3_Bramantyo_data_clean.csv'
    data_clean.to_csv(path, index=False)

    # Export clean data path
    context['ti'].xcom_push(key='clean_data_path', value=path)

# function load data
def load(**context):
    '''
    The first three processes of this function is similar to above, hence we will go through the fourth and fifth process. As we can see below,
    the 4th process is to connect our airflow postgres dataframe to the elasticsearch API (and to make sure it is connected, we will try ping it).
    Then the 5th process is to load our dataframe in json (because elasticsearch can only read json) row by rows.
    '''
    # Getting TI context
    ti = context['ti']

    # Getting cleaned data path
    data_path = ti.xcom_pull(task_ids='transform_data', key='clean_data_path') 

    # load as dataframe
    data_clean = pd.read_csv(data_path)

    # Create elasticsearch connection
    es = Elasticsearch('http://elasticsearch:9200')
    if not es.ping():
        print('tidak terkonek')

    # load data, per rows
    for i, row in data_clean.iterrows():

        doc = row.to_json()
        res = es.index(index='watch_dataframe', doc_type='doc', body = doc)

# define dag
with DAG(
    'pipeline_milestone',
    description = 'pipeline mentoring', 
    schedule_interval = '10-30/10 9 * * 6',
    default_args = default_args,
    catchup = False
) as dag:

    # task extract
    extract_data = PythonOperator(
        task_id = 'extract_data',
        python_callable = extract,
        provide_context=True
    )

    # task transform
    transform_data = PythonOperator(
        task_id = 'transform_data',
        python_callable = transform,
        provide_context = True
    )

    # task load
    load_data = PythonOperator(
        task_id = 'load_data',
        python_callable = load,
        provide_context = True
    )

extract_data >> transform_data >> load_data
