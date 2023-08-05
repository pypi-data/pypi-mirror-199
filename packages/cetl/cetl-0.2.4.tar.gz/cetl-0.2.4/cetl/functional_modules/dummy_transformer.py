from ..utils.builder import DataFrame, FUNCTIONAL_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper

@FUNCTIONAL_TRANSFORMERS.add()
class dummyTransformer(Base):
    """
    Usage:
        if there is not found transformer in the cfg, the DataPipeline will use this dummy transformer to help
        {"type":"dummyTransformer", "data_container_type":"functional"}
    """
    def __init__(self):
        super().__init__()
        pass

    @transform_wrapper
    def transform(self, input_data):
        return input_data