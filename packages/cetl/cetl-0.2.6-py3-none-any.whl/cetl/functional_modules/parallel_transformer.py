from ..utils.builder import FUNCTIONAL_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper
import copy
from ..utils.file_mgt import get_datetime_str

@FUNCTIONAL_TRANSFORMERS.add()
class parallelTransformer(Base):
    def __init__(self, transformers: list):
        super().__init__()
        self.transformers = transformers


    def transform(self, X)-> list:
        if isinstance(X, list):
            X=X
        elif X is None:
            X = ""
            X = [X for i in range(len(self.transformers))]
        else:
            X = [copy.deepcopy(X) for i in range(len(self.transformers))]

        # print(X)
        # assert len(X)>0
        outputs = []
        for i, transformer in enumerate(self.transformers):
            if hasattr(transformer, "breakpoint"):
                if transformer.breakpoint:
                    # print(transform.node_name, "has breakpoint", transform.breakpoint)
                    outputs.append(transformer.transform(X[i]))
                    datetime_str = get_datetime_str(format="%Y-%m-%d %H:%M:%S")
                    print(f"{datetime_str} stop with breakpoint at {transformer.node_name}") if transformer.print_task_result else ""
                else:
                    outputs.append(transformer.transform(X[i]))    
            else:
                outputs.append(transformer.transform(X[i]))
            
        return outputs

