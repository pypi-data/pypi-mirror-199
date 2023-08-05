from email import header
import numpy as np
from ..utils.builder import pd, DataFrame, PANDAS_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper

@PANDAS_TRANSFORMERS.add()
class unionAll(Base):
    """
    {"type":"unionAll"}
    """
    def __init__(self):
        super().__init__()
        pass
        

    @transform_wrapper
    def transform(self, dataframes: list):
        #skip transformation if dataframe is an empty dataframe
        for dataframe in dataframes:
            if dataframe is None:
                return dataframes
            if dataframe.empty:
                return dataframes
        
        df = pd.concat(dataframes)
        return df


@PANDAS_TRANSFORMERS.add()
class sqlJoin(Base):
    """
    {"type":"sqlJoin", "how":"left", "left_column":"MemberID", "right_column":"MemberID"}
    """
    def __init__(self,
                how=None,
                left_column=None,
                right_column=None):
        super().__init__()

        self.how = how
        self.left_column = left_column
        self.right_column = right_column
        


    @transform_wrapper
    def transform(self, dataframes):
        #https://www.statology.org/pandas-merge-on-different-column-names/
        dataframe1 = dataframes[0]
        dataframe2 = dataframes[1]

        if dataframe1.empty or dataframe2.empty:
            return pd.DataFrame()

        df = pd.merge(dataframe1, 
                      dataframe2, 
                      how=self.how, 
                      left_on=self.left_column,
                      right_on = self.right_column)
        return df
    

class multiJoin(Base):
    """
    {"type":"multiJoin", rules=[{"how":"left", "left_column":"grade_id", "right_column":""},
                                {"how":"left", "left_column":"grade_id", "right_column":""},
                                {"how":"left", "left_column":"grade_id", "right_column":""}
                                ]}
    usage of reduce lambda
    -----------------------------
    from functools import reduce
    numbers = [0, 1, 2, 3, 4]

    def my_add(a, b):
        result = a + b
        print(f"{a} + {b} = {result}")
        return result

    reduce(my_add, numbers)
    0 + 1 = 1
    1 + 2 = 3
    3 + 3 = 6
    6 + 4 = 10
    """


    def __init__(self, rules=None):
        super().__init__()

        self.rules = rules

    @transform_wrapper
    def transform(self, input_list):
        from functools import reduce
        def newSqlJoin(first_cfg=None, second_cfg=None):
            left_df = first_cfg["df"]
            how=first_cfg["how"]
            left_column=first_cfg["left_column"]
            right_column=first_cfg["right_column"]
            right_df = second_cfg["df"]

            transformer = sqlJoin(how=how, left_column=left_column, right_column=right_column)
            df = transformer.transform([left_df, right_df])
            second_cfg["df"]=df
            return second_cfg
        
        # prepare iterrable list
        self.rules.append({})
        # every rule is a dict
        for rule, df in zip(self.rules, input_list):
            rule["df"]=df
        
        result = reduce(lambda cfg1, cfg2:newSqlJoin(cfg1, cfg2), self.rules)
        return self.output_df

