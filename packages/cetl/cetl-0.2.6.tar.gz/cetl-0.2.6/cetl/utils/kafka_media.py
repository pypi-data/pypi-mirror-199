# pip install kafka-python
# pip install avro-python3
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import UnknownTopicOrPartitionError
import json
import pandas as pd
from kafka import KafkaProducer
from avro import schema, io
import io
import pandas as pd
import pickle
from cryptography.fernet import Fernet



class kafkaMedia:
    def __init__(self,
                bootstrap_servers=None,
                topic=None):

        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer=None
        self.consumer=None
        # print("init fernet ##########################")
        self.pub_key = Fernet.generate_key()
        self.fernet = Fernet(self.pub_key)
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)


    def __enter__(self,):
        
        # self.delete_topic()

        # # Create a Kafka producer instance
        # self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

        # # create instance of KafkaConsumer
        # self.consumer = KafkaConsumer(self.topic,
        #                         bootstrap_servers=self.bootstrap_servers,
        #                         auto_offset_reset='earliest',
        #                         enable_auto_commit=True)

        try:
            # self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
            self.delete_topic()

            # Create a Kafka producer instance
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

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
        print("# test when will run exit ####################")
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()

    def topic_exists(self, admin_client, topic_name):
        try:
            topic_metadata = admin_client.describe_topics([topic_name])
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
        # if not self.admin_client:
            # self.__enter__()
        if self.topic_exists(self.admin_client, self.topic):
            print("delete topic ...")
            self.admin_client.delete_topics([self.topic])


    def send(self, key=None, value=None):
        # if not self.producer:
            # self.__enter__()
        # print("topic", self.topic)
        # print("send key", key)
        if not isinstance(key, bytes):
            key = key.encode("utf-8")

        try:
            self.producer.send(self.topic, key=key, value=value)
        except Exception as e:
            print(self.producer)
            print("key", key)
            print("value", value)
            print(e)
        # producer.flush()

    def send_kafka(self, task_id=None, value=None):

        df = value

        # serialize the dataframe to pickle
        serialized_data = self.serialize_dataframe(df)
        # print("serialized_data: ", serialized_data)

        # create instance of encryption
        encrypted_data = self.fernet.encrypt(serialized_data)
        # print(encrypted_data)

        # send the data to kafka topic
        # print("send key", task_id)
        self.send(key=task_id, value=encrypted_data)
        # print("send encrypted_data", encrypted_data)


    def receive(self, key=None):
        # if not self.consumer:
        #     # create instance of KafkaConsumer
        #     self.consumer = KafkaConsumer(self.topic,
        #                             bootstrap_servers=self.bootstrap_servers,
        #                             auto_offset_reset='earliest',
        #                             enable_auto_commit=True)

        # print("self.consumer", self.consumer)
        for message in self.consumer:
            # print("dectect message", message.key, key)
            # print(message.key, key)
            if message.key == key:
                received_message = message.value
                return received_message


    def receive_with_partition(self, key=None):
        if not self.consumer:
            # create instance of KafkaConsumer
            self.consumer = KafkaConsumer(self.topic,
                                    bootstrap_servers=self.bootstrap_servers,
                                    auto_offset_reset='earliest',
                                    enable_auto_commit=True)

        # Get partitions for the topic
        partitions = self.consumer.partitions_for_topic(self.topic)

        # Loop through partitions and clear messages
        for partition in partitions:
            # Get current partition offset
            tp = TopicPartition(self.topic, partition)
            current_offset = self.consumer.position(tp)

            # Seek to beginning of partition
            self.consumer.seek_to_beginning(tp)

            # Consume messages and send null messages with same keys to clear the topic
            for message in self.consumer:
                # print("detect message", message.key, key)
                if message.key == key:
                    received_message = message.value
                    return received_message
            
            

    def read_kafka(self, task_id=None):
        # received message
        # print("self.receive###############", self.receive)
        message = self.receive_with_partition(key=task_id)
        assert message
        # print("received message", message)
        
        # decrypt the message
        # print(key)
        decrypted_data = self.fernet.decrypt(message)

        # # decode by pickle
        df = self.deserialize_dataframe(decrypted_data)

        return df


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


# from .kafka_helper import kafkaHelper
# from ..utils.builder import pd
# from cryptography.fernet import Fernet

# class kafkaMedia(kafkaHelper):
#     def __init__(self, 
#                 bootstrap_servers=None,
#                 topic=None):
#         super().__init__(bootstrap_servers=bootstrap_servers,
#                         topic=topic)

#     def send_kafka(self, key=None, value=None):

#         if isinstance(value, pd.DataFrame):
#             df = value

#             # serialize the dataframe to pickle
#             serialized_data = self.serialize_dataframe(df)
#             # print("serialized_data: ", serialized_data)

#             # create instance of encryption
#             self.pub_key = Fernet.generate_key()
#             self.fernet = Fernet(self.pub_key)

#             encrypted_data = self.fernet.encrypt(serialized_data)
#             # print("encrypted_data", encrypted_data)

#             # send the data to kafka topic
#             self.send(key=key, value=encrypted_data)

#     def read_kafka(self, key=None):

        
#         # received message
#         message = self.receive(key=key)

#         # decrypt the message
#         decrypted_data = self.fernet.decrypt(message)

#         # decode by pickle
#         df = self.deserialize_dataframe(decrypted_data)

#         # delete the topic
#         # kh.delete_topic()

        return df


