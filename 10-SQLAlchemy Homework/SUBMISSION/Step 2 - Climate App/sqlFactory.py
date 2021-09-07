import pandas as pd
import numpy as np
from sqlFactoryHelper import SQLFactoryHelper

class SQLFactory():
    def __init__(self):
        self.sqlFactoryHelper = SQLFactoryHelper()

    ##################################################################
    ################## QUERY FUNCTIONS ##############################
    ##################################################################

    def getAllInvoices(self):
        query = self.sqlFactoryHelper.readSQLQuery('getAllInvoices.sql')
        data = self.sqlFactoryHelper.executeQuery(query) # read in using helper function
        return(data)

    def getAllInvoiceItems(self):
        query = self.sqlFactoryHelper.readSQLQuery('getAllInvoiceItems.sql')
        data = self.sqlFactoryHelper.executeQuery(query) # read in using helper function
        return(data)

    def getInvoiceForInvoiceID(self, invoiceId):
        query = self.sqlFactoryHelper.readSQLQueryWithReplacement('getInvoiceForInvoiceID.sql', invoiceId)
        data = self.sqlFactoryHelper.executeQuery(query) # read in using helper function
        return(data)