import os

# class config():
username = os.getenv('SNOWFLAKE_USERNAME')
password = os.environ.get('SNOWFLAKE_PASSWORD')
account = os.environ.get('SNOWFLAKE_ACCOUNT')
role="SYSADMIN"
warehouse="appwh"
database="txtappdb"
schema="schema"
table="example_table"
