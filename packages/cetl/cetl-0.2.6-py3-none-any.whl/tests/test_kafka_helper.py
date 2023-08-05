# run command: python test_kafka_helper
import pandas as pd

import sys, os
sys.path.insert(0, os.path.join(".."))
from cetl.utils.kafka_helper import kafkaHelper

# Define Kafka connection parameters
# althought it is not in docker container, 
# still need to use docker inspect to find the docker network
bootstrap_servers = ['172.31.0.1:9092']
topic_name = "mytopic"
# task_id
task_id = "1.filterBy"
# Create a pandas dataframe
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})

with kafkaHelper(   bootstrap_servers=bootstrap_servers,
                    topic=topic_name) as kh:

    # serialize the dataframe to pickle
    serialized_data = kh.serialize_dataframe(df)
    # print("serialized_data: ", serialized_data)

    # create instance of encryption
    encrypted_data = kh.fernet.encrypt(serialized_data)
    # print(encrypted_data)

    # send the data to kafka topic
    kh.send(key=task_id, value=encrypted_data)


    # received message
    message = kh.receive(task_id)

    # decrypt the message
    decrypted_data = kh.fernet.decrypt(message)

    # decode by pickle
    df = kh.deserialize_dataframe(decrypted_data)

    print(df)

    # delete the topic
    kh.delete_topic()