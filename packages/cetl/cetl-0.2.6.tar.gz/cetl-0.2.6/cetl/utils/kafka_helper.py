# pip install kafka-python
# pip install avro-python3
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
import json
import pandas as pd
from kafka import KafkaProducer
import io
import pandas as pd
import pickle
from cryptography.fernet import Fernet
from kafka.errors import UnknownTopicOrPartitionError

class kafkaHelper:
    """usage

    """
    def __init__(self,
                bootstrap_servers=None,
                topic=None):

        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer=None
        self.consumer=None
        self.pub_key = Fernet.generate_key()
        self.fernet = Fernet(self.pub_key)
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
        

    def __enter__(self,):
        
        try:
            # delete original topic
            self.delete_topic()

            # Create a Kafka producer instance
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

            # create instance of KafkaConsumer
            self.consumer = KafkaConsumer(self.topic,
                                    bootstrap_servers=self.bootstrap_servers,
                                    auto_offset_reset='earliest',
                                    enable_auto_commit=True)
        except Exception as e:
            if self.producer:
                self.producer.close()
            if self.consumer:
                self.consumer.close()
            print("has error")
        
        return self


    def __exit__(self, exc_type, exc_value, exc_tb):
        print("test when will run exit ################################")
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()

    def topic_exists(self, admin_client, topic_name):
        """
        [{'error_code': 3, 'topic': 'c', 'is_internal': False, 'partitions': []}, 
        {'error_code': 3, 'topic': 'o', 'is_internal': False, 'partitions': []}, 
        {'error_code': 3, 'topic': '3', 'is_internal': False, 'partitions': []}, 
        {'error_code': 3, 'topic': 'm', 'is_internal': False, 'partitions': []}, 
        {'error_code': 3, 'topic': 't', 'is_internal': False, 'partitions': []}, 
        {'error_code': 3, 'topic': 'p', 'is_internal': False, 'partitions': []}, 
        {'error_code': 3, 'topic': 'y', 'is_internal': False, 'partitions': []}, 
        {'error_code': 3, 'topic': 'i', 'is_internal': False, 'partitions': []}]
        """
        try:
            topic_metadata = admin_client.describe_topics([topic_name])
            print(topic_metadata)
            # for partition_data in topic_metadata:
            #     if "error_code" in partition_data:

            # print("show topic_metadata", topic_metadata)
            if "error_code" in topic_metadata[0]:
                if topic_metadata[0]["error_code"]==3:
                    return False
                if topic_metadata[0]["error_code"]==0:
                    return True
            
            return True
        except UnknownTopicOrPartitionError:
            return False


    def delete_topic(self):   
        if self.topic_exists(self.admin_client, self.topic):
            print("delete topic ...")
            self.admin_client.delete_topics([self.topic])

    def send(self, key=None, value=None):
        if not isinstance(key, bytes):
            key = key.encode("utf-8")

        self.producer.send(self.topic, key=key, value=value)


    def receive(self, key):
        if not isinstance(key, bytes):
            key = key.encode("utf-8")
        for message in self.consumer:
            # print("message.key", message.key)
            # print("message.value", message.value)
            if message.key == key:
                received_message = message.value
                return received_message


    def close(self):
        self.producer.close()
        self.consumer.close()


    def serialize_dataframe(self, df):
        return pickle.dumps(df)

    
    def deserialize_dataframe(self, serialized_data):
        # deserialize the data
        file_obj = io.BytesIO(serialized_data)
        df = pickle.load(file_obj)
        return df