from ..utils.builder import DataFrame, PANDAS_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper

@PANDAS_TRANSFORMERS.add()
class filterBy(Base):
    """
    {"type":"filterBy", "fieldname":"keep", "fieldvalue":"yes", "Op":"true"}
    """
    def __init__(self, fieldname=None, fieldvalue=None, Op="true", parallel_index=None):
        super().__init__()
        
        self.fieldname = fieldname
        self.fieldvalue = fieldvalue
        self.Op = Op
        self.parallel_index=parallel_index

    @transform_wrapper
    def transform(self, dataframe):
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        if isinstance(dataframe, list):
            assert isinstance(self.parallel_index, int)
            df=dataframe[self.parallel_index]
            # print(df)
        elif isinstance(dataframe, DataFrame):
            df = dataframe
        else:
            print("input should be pandas DataFrame or list of pandas DataFrames")

        # print(df.columns)
        # if "keep" in df.columns:
        #     print(self.Op)
        #     print(df[df[self.fieldname]==self.fieldvalue])
        if self.Op=="true":
            df = df[df[self.fieldname]==self.fieldvalue]
            # print(self.parallel_index)
        elif self.Op=="false":
            df = df[df[self.fieldname]!=self.fieldvalue]
            # print(self.parallel_index)
        
        return df

@PANDAS_TRANSFORMERS.add()
class filterValuesInList(Base):
    """
    {"type":"filterValuesInList", "fieldname":"keep", 
        "fieldvalues":["CANCELLED", "REPLACED"], "Op":"true"}
    """
    def __init__(self, fieldname=None, fieldvalues=None, Op=None):
        super().__init__()

        self.fieldname = fieldname
        self.fieldvalues = fieldvalues
        self.Op = Op

    @transform_wrapper
    def transform(self, dataframe):
        df = dataframe
        # print(df[self.fieldname])
        if self.Op == "true":
            c = df[self.fieldname].isin(self.fieldvalues)
            new_df = df[c]
            # print(new_df)
        else:
            c = df[self.fieldname].isin(self.fieldvalues)
            new_df = df[~(c)]
        return new_df




@PANDAS_TRANSFORMERS.add()
class filterByEvalStatement(Base):
    """
    {"type":"filterByEvalStatement", "eval_statement":""}
    """
    def __init__(self, 
                eval_statement=None):
        super().__init__()

        self.eval_statement = eval_statement

    @transform_wrapper
    def transform(self, dataframe):
        df = dataframe
        
        c = eval(self.eval_statement)
        df = df[c]


        return df
