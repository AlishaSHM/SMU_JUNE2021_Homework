import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json

class SQLFactoryHelper():
    def __init__(self):
        self.db = create_engine("sqlite:///Resources/chinook.sqlite")

    ##################################################################
    ################## HELPER FUNCTIONS ##############################
    ##################################################################

    def executeQuery(self, query):
        conn = self.db.connect()
        df = pd.read_sql(query, conn)
        conn.close()

        data = df.to_json(orient="records") # creates JSON string
        data = json.loads(data) # turns the string back into list of dicts

        return(data)

    def readSQLQuery(self, query_path):
        query = ""
        with open(f"queries/{query_path}", "r") as f: # read in from the query folder
            query = f.read()

        return query

    def readSQLQueryWithReplacement(self, query_path, replacement):
        query = self.readSQLQuery(query_path)
        query = query.replace("PLACEHOLDER", replacement) # replace the placeholder in the query string
        return query