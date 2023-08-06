from cetl.pandas_modules.input import generateDataFrame
from cetl import DataPipeline, pd


def test_pass_dataframe():

    answer = generateDataFrame().transform("")
    # print(answer)

    cfg = {"pipeline":[ {"type":"generateDataFrame"},
                        {"type":"passDataFrame", "data_container_type":"functional"}
                        ]}

    pipe = DataPipeline(cfg)
    df = pipe.transform("")

    assert df.equals(answer)



# def test_add_numbers():
#     assert add_numbers(2, 3) == 5
#     assert add_numbers(-1, 1) == 0
#     assert add_numbers(0, 0) == 0