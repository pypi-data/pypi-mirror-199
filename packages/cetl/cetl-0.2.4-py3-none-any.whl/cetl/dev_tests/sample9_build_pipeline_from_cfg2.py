import sys 
sys.path.append('.')
from cetl import DataPipeline

cfg = { "pipeline": [   {"type":"dummyStart", "module_type":"functional"},
                        {"type":"parallelTransformer", "transformers":[
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


# pipe = pipe.build_digraph()
# pipe.save_png("./sample7.png")


# python cetl/dev_tests/sample9_build_pipeline_from_cfg2.py