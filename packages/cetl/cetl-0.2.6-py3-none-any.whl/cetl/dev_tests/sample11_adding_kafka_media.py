import sys 
sys.path.append('.')
from cetl import DataPipeline


cfg = { "pipeline": [   {"type":"dummyStart"},
                        {"type":"parallelTransformer", "transformers":[
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"}
                        ]},
                        {"type":"unionAll"}],
                    
        "pipeline_settings":{   "print_cfg":1, 
                                "print_task_result":1, 
                                "exchange_media":"kafka",
                                "bootstrap_servers":["172.31.0.1:9092"]}}




# pipe = build_cetl_pipeline(cfg, bootstrap_servers=["192.168.176.1:9092"])
pipe = DataPipeline(cfg)
for step in pipe.steps:
    task_id, transformer = step
    print(transformer)
result = pipe.transform("")

# get the output of transformer by task_id
task_id = b"3.generateDataFrame"
df = pipe.kafka_media.read_kafka(task_id=task_id)
print(df)

# # delete the topic
# pipe.kafka_media.delete_topic()



# pipe = pipe.build_digraph()
# pipe.save_png("./sample11.png")


# python cetl/dev_tests/sample11_adding_kafka_media.py