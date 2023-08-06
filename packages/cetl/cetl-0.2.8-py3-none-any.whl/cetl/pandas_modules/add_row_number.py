from ..utils.builder import DataFrame, PANDAS_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper

@PANDAS_TRANSFORMERS.add()
class addRowNumber(Base):
    """
    {"type":"addRowNumber", "mark_field":"rownumber"}
    """
    def __init__(self, mark_field="Number"):
        super().__init__()
        
        self.mark_field=mark_field

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe
        df['A'] = "A"
        df[self.mark_field] = df.groupby(['A']).cumcount()+1
        df=df.drop(columns=['A'])
        return df


