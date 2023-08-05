import sys 
sys.path.append('.')
from cetl import DataPipeline, build_pipeline
from cetl.functional_modules.pass_dataframe import dummyStart
from cetl.functional_modules.parallel_transformer import parallelTransformer
from cetl.pandas_modules.input import generateDataFrame
from cetl.pandas_modules.two2one import unionAll

cfg = {"pipeline":[ {"type":"dummyStart", "module_type":"functional"},
                    {"type":"parallelTransformer", "transformers":[
                        {"type":"generateDataFrame"},
                        {"type":"generateDataFrame"}
                    ]},
                    {"type":"unionAll"}
]}

# pipe = DataPipeline(cfg)
steps = [   dummyStart(), 
            parallelTransformer([   generateDataFrame(), 
                                    generateDataFrame()]), 
            unionAll()]

pipe = build_pipeline(*steps)
pipe.print_task_result = 1
df = pipe.transform("")
print(df)


# pipe = pipe.build_digraph()
# pipe.save_png("./sample8.png")


# python cetl/dev_tests/sample8_build_pipeline.py