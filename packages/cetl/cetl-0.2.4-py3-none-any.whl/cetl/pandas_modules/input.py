from ..utils.builder import DataFrame, PANDAS_TRANSFORMERS, pd
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper

import csv
import json

@PANDAS_TRANSFORMERS.add()
class generateDataFrame(Base):
    """
    {"type":"generateDataFrame"}
    """
    def __init__(self, data=None):
        super().__init__()
        self.data = data
    
    @transform_wrapper
    def transform(self, input) -> DataFrame:
        
        df = None
        if not self.data:
            self.data = [  {"customer_id":111, "first_name":"peter", "last_name":"Hong", "title":"Mr."},
                                {"customer_id":222, "first_name":"YuCheung", "last_name":"Wong", "title":"Mr."},
                                {"customer_id":333, "first_name":"Cindy", "last_name":"Wong", "title":"Mrs."},
                            ]
            df = pd.DataFrame(self.data)

        return df

