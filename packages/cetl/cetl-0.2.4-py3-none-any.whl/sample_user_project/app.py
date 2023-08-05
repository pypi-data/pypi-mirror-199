# running command: python3.6 app.py
# -----------------------------------
# from sample_modules.add_new_column import addNewColumn
# from cetl import DataPipeline

# result=""
# cfg = {"pipeline":[
#                     {"type":"addRowNumber"},
#                     {"type":"parallelTransformer", "isParallel":1, "transformers":[
#                             {"type":"format2String", "description":"help following filterBy transformer"},
#                             {"pipeline":[   {"type":"filterBy"},
#                                             {"type":"parallelTransformer", "isParallel":1, "transformers":[
#                                                 {"type":"addRowNumber"},
#                                                 {"type":"passDataFrame"}]},
#                                             {"type":"toCSV", "out_dir":"./", "out_file":"out.csv"}]},
#                             {"pipeline":[{"type":"paddingZero"}]},
#                             {"type":"dropColumns", "description":"remove temp columns"}
#                         ]},
#                     {"type":"passDataFrame"},
#                     {"type":"addNewColumn", "base_field":"Tier", "value":"hi"},
#                     {"pipeline":[   {"type":"passDataFrame"},
#                                     {"type":"toCSV", "out_dir":"./", "out_file":"out.csv"}]}
#         ]}


# cfg = {"pipeline":[
#                     {"type":"generateDataFrame"},
#                     {"type":"addNewColumn", "base_field":"rownumber", "value":""},
#                     {"type":"addRowNumber", "mark_field":"rownumber"},
#                     {"type":"parallelTransformer", "transformers":[
                        

#                     ]}

# ]}



# from cetl import make_pipeline, DataPipeline
# from cetl.pandas_modules import generateDataFrame, unionAll
# from cetl.functional_modules import dummyStart, parallelTransformer, passDataFrame
# from cetl.utils.pipeline import _name_estimators



# print(_name_estimators([dummyStart(), passDataFrame()]))

    # pipe = make_pipeline(   dummyStart(),
    #                         parallelTransformer([generateDataFrame(), generateDataFrame()]), 
    #                         unionAll())
    # df = pipe.transform("")
    # print(df.to_markdown())
    # dot = pipe.build_digraph()
    # print(dot)

from cetl import build_pipeline
from cetl.pandas_modules import generateDataFrame, unionAll
from cetl.functional_modules import dummyStart, parallelTransformer

pipe = build_pipeline(   dummyStart(),
                        parallelTransformer([generateDataFrame(), generateDataFrame()]), 
                        unionAll())
df = pipe.transform("")
print(df)





# with DataPipeline(cfg) as pipe:
    # result = pipe.transform(result)
#     # print(pipe.steps)
#     # print(result)
#     # -----------------------------------------------
#     # create dot graph
#     pipe = pipe.build_digraph()
#     pipe.save_png("./sample5.png")

# ---------------------------------------------
# check all the module
# from cetl import PANDAS_TRANSFORMERS
# print(PANDAS_TRANSFORMERS.module_dict)

