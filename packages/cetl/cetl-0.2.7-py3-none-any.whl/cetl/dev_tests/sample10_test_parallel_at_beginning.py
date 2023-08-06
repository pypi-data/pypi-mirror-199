import sys 
sys.path.append('.')
from cetl import DataPipeline

cfg = { "pipeline": [   {"type":"parallelTransformer", "transformers":[
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"}
                        ]},
                        {"type":"unionAll"}],
                    
        "pipeline_settings":{   "print_cfg":1, 
                                "print_task_result":1, 
                                "exchange_media":"default"}}

pipe = DataPipeline(cfg)
for step in pipe.steps:
    task_id, transformer = step
    print(transformer)
df = pipe.transform("")
# print(df)


pipe = pipe.build_digraph()
pipe.save_png("./sample10.png")


# python cetl/dev_tests/sample10_test_parallel_at_beginning.py