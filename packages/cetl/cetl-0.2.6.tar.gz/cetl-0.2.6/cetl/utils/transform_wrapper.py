from functools import wraps
import time
from .builder import context_name, DataFrame
from datetime import datetime
from .file_mgt import get_datetime_str
from .kafka import kafka2python, python2kafka
EXCH_MEDIA = "default"


def recursive_records_count(count, data):
    if isinstance(data, dict):
        if context_name in data:
            count += len(data[context_name])
        elif "key" in data:
            return count
        else:
            print("not acceptable context_name")
            # raise ValueError()
            return count

    elif isinstance(data, DataFrame):
        count += data.shape[0]
    elif isinstance(data, str):
        count += 0
    elif isinstance(data, list):
        for item in data:
            count = recursive_records_count(count, item)
    elif isinstance(data, set):
        print("----------------------transformer output seems missing ':'", data)
        raise ValueError("please check the whether output should be dictionary since you are missing ':'")
    else:
        raise ValueError("currently only accept list, str, json and pandas data type")
    
    return count


def transform_wrapper(func):
    """
    Usage
    ----------------------------
    class Calculator:
        @transform_wrapper
        def calculate_something(self, num):
            total = sum((x for x in range(0, num**2)))
            return total

        def __repr__(self):
            return f'calc_object:{id(self)}'
    Reference
    ---------------------------
    https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        transformer = args[0]
        input = args[1]
        
        kafka_media = transformer.kafka_media


        # Calculate the execution time
        start_time = time.perf_counter()
        transformer.start_datetime = get_datetime_str(format="%Y-%m-%d %H:%M:%S")

        # print processing label
        print(f"Processing {transformer.node_name}, started at {transformer.start_datetime} ...") if transformer.print_task_result else ""

        # execute the transform function -----------------------------------------------------
        if transformer.exchange_media == "default":
            result = func(*args, **kwargs) #result here is module output

        elif transformer.exchange_media =="kafka":
            # decode the input from kafka topic
            pre_module_output=""

            if not transformer.is_first_trans:

                if isinstance(input, dict):
                    pre_transformer_key = input["key"]
                    pre_module_output = kafka_media.read_kafka(   task_id=pre_transformer_key.encode('utf-8'))
                
                elif isinstance(input, list):
                    # previous transformer is wrapped by parallelTransformer
                    pre_module_output = []
                    for pre_transformer_key in [item["key"] for item in input]:
                        # ---------------------------------------------------------- read message
                        kafka2python = kafka_media.read_kafka(task_id=pre_transformer_key.encode('utf-8'))
                        pre_module_output.append(kafka2python)

                elif isinstance(input, str):
                    # print("pre_transformer_key", pre_transformer_key)
                    # there is the in airflow, task relationship is not upstream
                    pre_transformer_key = input
                    pre_module_output = ""
                    
            else:
                pre_module_output = ""

            # print("####################")            
            result = func(transformer, pre_module_output) # result here is module output

        else:
            # reserve for future case
            # result = func(*args, **kwargs) #result here is module output
            print(transformer.exchange_media, transformer.node_name)
            assert False

        # ----------------------------------------------------------------------------------------
        # Calcuate the end time
        end_time = time.perf_counter()
        total_time = end_time - start_time
        transformer.end_datetime = get_datetime_str(format="%Y-%m-%d %H:%M:%S")
        # print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')


        # Adding the execution time to the transformer
        transformer.total_time = total_time
        
        # print(self)
        # parallelTransformer will make it run double times, not solved yet

        #count the number of records in input and output of the func:
        transformer.total_input = recursive_records_count(0, input)
        transformer.total_output = recursive_records_count(0, result)

        if transformer.node_name:
            print(f"    - take time {total_time:.4f} seconds, total input records {transformer.total_input}, total output records {transformer.total_output}") if transformer.print_task_result else ""

            # print(f"stop with breakpoint at {transformer.node_name}") if transformer.print_task_result else ""
        # print(f"{transformer.node_name}: take time {total_time:.4f} seconds, total input records {transformer.total_input}, total output records {transformer.total_output}")

        # output result  -------------------------------------------------------------------------
        if transformer.exchange_media == "default":
            return result

        elif transformer.exchange_media =="kafka":
            # print(transformer)
            # print("####################")
            # sending the python object to kafka topic
            # print("transformer.node_name", transformer.node_name.encode('utf-8'))
            # print("result", result)
            kafka_media.send_kafka(task_id=transformer.node_name.encode('utf-8'), value=result)

            result = {  "key":transformer.node_name,
                        "total_input":transformer.total_input, 
                        "total_output":transformer.total_output}
            return result
        else:
            # reserve for future use
            # return result

            print(transformer.exchange_media, transformer.node_name)
            assert False
        # ----------------------------------------------------------------------------------------

    return func_wrapper


    

    


