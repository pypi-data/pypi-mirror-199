import numpy as np
na_values = ["", 
            "#N/A", 
            "#N/A N/A", 
            "#NA", 
            "-1.#IND", 
            "-1.#QNAN", 
            "-NaN", 
            "-nan", 
            "1.#IND", 
            "1.#QNAN", 
            "<NA>", 
            "N/A", 
    #              "NA", 
            "NULL", 
            "NaN", 
            "n/a", 
            "nan", 
            "null",
            np.nan,
            float('nan'),
            np.float("nan"),
            np.float64("nan")]

def paddingzero(x, num_digit):
    if type(x)==str:
        return x.zfill(num_digit)
    else:
        type(x)==int
        # print("i am int")
        new_x = str(x).zfill(num_digit)
        # print(new_x)
        return new_x


def addUniqueKeyList(value_prefix = None,
                    value_suffix = None,
                    value_start = None,
                    value_end = None,
                    padding_digit=None):

    unique_list = [value_prefix + paddingzero(i, padding_digit) + value_suffix for i in range(value_start,value_end+1)]

    return unique_list


def format_int(df, subset):
    headers = list(df.columns)
    for field in subset:
        if field in headers:
            df[field] = df[field].apply(lambda x: int(x))
        else:
            print(f"{field} column not exists")
