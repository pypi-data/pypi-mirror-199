from sklearn.base import BaseEstimator, TransformerMixin

class Base(BaseEstimator, TransformerMixin):
    def __init__(self):
        
        self.exchange_media = "default" # e.g. "default", "kafka"
        self.broker_host = ""
        self.broker_port = ""
        # can be string or a list
        # if previous transformer is parallelTransformer, then would be a list
        self.pre_node_name = "" 
        self.delete_kafka_topic=1

        self.node_id = ""
        self.node_name = ""
        self.description = ""
        self.isParallel = "false"
        self.total_time = 0
        self.total_input = 0
        self.total_output = 0
        self.data_container_type="pandas"
        self.start_datetime = ""
        self.end_datetime = ""
        self.breakpoint = 0
        self.print_task_result=0
        self.is_first_trans = 0
        self.is_last_trans = 0

        


    def fit(self):
        pass
    