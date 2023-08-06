from pandas import DataFrame
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.join(".."))
from cetl import TEST_TRANSFORMERS as test_transformers
from cetl.utils.base import Base

@test_transformers.add()
class addNewColumn(Base):
    """
    {"type":"addNewColumn", "base_field":"Tier", "value":""}
    """
    def __init__(self, 
                base_field=None,
                value=None):

        self.base_field = base_field
        self.value = value

    def transform(self, dataframe: DataFrame):
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe
        df[self.base_field] = self.value
        
        return df