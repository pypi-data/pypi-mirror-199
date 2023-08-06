import pandas as pd
import numpy as np
import sys
import os
import pytd
import requests
import json
from ast import literal_eval

##-- Declare ENV Variables from YML file
apikey = os.environ['TD_API_KEY'] 
tdserver = os.environ['TD_API_SERVER']
segment_api = tdserver.replace('api', 'api-cdp')
sink_database = os.environ['SINK_DB']
output_table = os.environ['OUTPUT_TABLE']
unique_id = os.environ['UNIQUE_ID']
secondary_id_list = os.environ['SECONDARY_IDS']

#Write Queries to Temp Table
def extract_queries():

    print(output_table)

    headers= {"Authorization":'TD1 '+ apikey, "content-type": "application/json"}

    #Load profile_mapping_temp_table
    query_syntax = f'SELECT * FROM {output_table}'
    
    client = pytd.Client(apikey=apikey, endpoint=tdserver, database=sink_database)
    results = client.query(query_syntax, engine='presto')
    new_tab =  pd.DataFrame(**results)
    
    #Parse final list of user IDs / Join Keys to extract from Parent Segment customers table
    if len(secondary_id_list) > 0:
      sec_ids = secondary_id_list.split(',')
      sec_ids.insert(0, unique_id)
      id_list_final = ["a." + item.strip() for item in sec_ids]
      select_ids = ", ".join(id_list_final)
    else:
      select_ids = unique_id

    print(select_ids)

    #Exctract queries for each segment
    queries = []
    for item in list(zip(new_tab.ps_id, new_tab.rule, new_tab.ps_name, new_tab.ps_population, new_tab.v5_flag, new_tab.folder_name, new_tab.segment_name, new_tab.segment_population, new_tab.segment_id)):
        rule = {"rule": literal_eval(item[1]), "format":"sql"}
        mastersegment_id = item[0]
        ps_name = item[2]
        ps_population = item[3]
        v5_flag = item[4]
        folder_name = item[5]
        segment_name = item[6]
        segment_population = item[7]
        segment_id = item[8]

        #Write query
        post = requests.post(f'https://{segment_api}/audiences/{mastersegment_id}/segments/query', headers=headers, json=rule)
        segment_query = post.json()['sql']

        #Add list of user IDs to query
        segment_query = segment_query.split()
        segment_query[1] = f"{select_ids}, '{ps_name}' as ps_name, {ps_population} as ps_population, {v5_flag} as v5_flag, '{folder_name}' AS folder_name, {segment_id} AS segment_id, '{segment_name}' as segment_name, {segment_population} AS segment_population"
        segment_query = " ".join(segment_query)

        queries.append(segment_query)
     
    #Create final table
    new_tab['segment_query'] = queries
    
    client.load_table_from_dataframe(new_tab, output_table, writer='bulk_import', if_exists='overwrite')