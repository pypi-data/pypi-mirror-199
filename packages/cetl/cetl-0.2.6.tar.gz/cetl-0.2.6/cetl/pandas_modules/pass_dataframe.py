from ..utils.builder import DataFrame, PANDAS_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper


@PANDAS_TRANSFORMERS.add()
class passDataFrame(Base):
    """do nothing
    {"type":"passDataFrame", "data_container_type":"functional"}
    """
    def __init__(self):
        super().__init__()
        pass

    @transform_wrapper
    def transform(self, dataframe):
        if not isinstance(dataframe, DataFrame):
            return DataFrame()

        return dataframe


@PANDAS_TRANSFORMERS.add()
class dummyStart(Base):
    """do nothing
    {"type":"dummyStart", "data_container_type":"functional"}
    """
    def __init__(self):
        super().__init__()
        pass

    @transform_wrapper
    def transform(self, dataframe):
        if not isinstance(dataframe, DataFrame):
            return DataFrame()

        return dataframe

@PANDAS_TRANSFORMERS.add()
class dummyStartEmpty(Base):
    """do nothing
    {"type":"dummyStart", "data_container_type":"functional"}
    """
    def __init__(self):
        super().__init__()
        pass

    @transform_wrapper
    def transform(self, dataframe):
        return dataframe
