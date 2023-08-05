from pyspark.sql import DataFrame, functions as F
import functools
from joblib import Parallel, delayed
from ..utils.builder import FUNCTIONAL_TRANSFORMERS
from ..utils.base import Base


@FUNCTIONAL_TRANSFORMERS.add()
class multiThreadTransformers(Base):
    
    def __init__(self, 
                 steps: list,
                 n_jobs=-1,
                 multithread=False):
        
        self.steps = steps
        self.n_jobs = n_jobs
        self.multithread = multithread
        
    def fit(self):
        pass
    

    def transform(self, X):

        assert len(self.steps)>0
        
        dfs=None
        if isinstance(X, list):
            X=X
        else:
            # prepare multiple input for parallel transform
            X = [X.copy(deep=True) if isinstance(X, DataFrame) else X for result in range(len(self.steps))]

            
        assert len(X) == len(self.steps)
        parallel_result = None

        if self.multithread:

            with Parallel(n_jobs=self.n_jobs, verbose=5) as parallel:
                funcs = [delayed(lambda t:t.transform(x))(transformer) for x, transformer in zip(X, self.steps)]
                parallel_result = parallel(funcs)
        else:
            parallel_result = [transformer.transform(x) for x, transformer in zip(X, self.steps)]

        return parallel_result