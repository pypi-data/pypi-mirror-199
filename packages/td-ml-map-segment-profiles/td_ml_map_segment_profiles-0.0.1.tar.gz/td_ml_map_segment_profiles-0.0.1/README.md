# td-ml-map-segment-profiles

## Introduction

This Python Library allows you to extract the query syntax for each Segment built in Audience Studio and write syntax to a table in TD with Folder/Segment names and canonical_ids that belong to each Audience. This mapping table can then be joined to attribute/behavior tables, so you can calcualte KPIs across different Audiences and track performance and auience changes over time. 


## Input Params

`config.yml`: The workflow `YAML` file contains the params that are required by this library to extract the neded information. See below:

- **apikey** = TD APIKEY  
- **tdserver** = TD ENDPOINT
- **sink_database** = Database where outout tables will be written
- **output_table** = name of output table
- **unique_id** = distinct user_id in `gldn` database (ex. `canoncial_id`)
- **secondary_id_list** = any secondary IDs needed for joins in Parent Segment if one main identifier is not used across all tables in PS
