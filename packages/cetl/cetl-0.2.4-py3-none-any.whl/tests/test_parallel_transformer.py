from cetl import DataPipeline, pd
from cetl.pandas_modules.input import generateDataFrame

def test_parallel_transformer():

    answer = pd.concat([generateDataFrame().transform(""), 
                        generateDataFrame().transform("")])
    # print(answer)

    cfg = {"pipeline":[
                        {"type":"parallelTransformer", "transformers":[
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"}
                        ]},
                        {"type":"unionAll"}
    ]}

    pipe = DataPipeline(cfg)
    df = pipe.transform("")
    # print(df)

    assert df.equals(answer)


def test_parallel_transformer2():

    answer = pd.concat([generateDataFrame().transform(""), 
                        generateDataFrame().transform("")])
    # print(answer)

    cfg = {"pipeline":[ {"type":"dummyStart", "data_container_type":"functional"},
                        {"type":"parallelTransformer", "transformers":[
                            {"type":"generateDataFrame"},
                            {"type":"generateDataFrame"}
                        ]},
                        {"type":"unionAll"}
    ]}

    pipe = DataPipeline(cfg)
    df = pipe.transform("")
    # print(df)

    assert df.equals(answer)