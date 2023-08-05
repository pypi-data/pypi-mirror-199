import sys 
sys.path.append('.')
from cetl import DataPipeline

cfg = {"pipeline":[ {"type":"dummyStart", "module_type":"functional"},
                    {"type":"parallelTransformer", "transformers":[
                        {"breakpoint":1, "type":"generateDataFrame"},
                        {"type":"generateDataFrame"},
                        {"type":"generateDataFrame"}
                    ]},
                    {"type":"unionAll"}],
                    
        "pipeline_settings":{"print_cfg":1, "print_task_result":1}}

pipe = DataPipeline(cfg)
df = pipe.transform("")
# print(df)


pipe = pipe.build_digraph()
pipe.save_png("./sample7.png")


# python cetl/dev_tests/sample7_build_pipeline_from_cfg.py