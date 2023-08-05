# from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
from cetl import pd
import pytz
import datetime

# SparkConf().set("spark.driver.memory", "50g")
# SparkConf().set('spark.executor.cores', '4')
# SparkConf().set('spark.cores.max', '4')

#maxToStringFields will affect df.show(10, truncate=False)
class SPARK_UTILS:
    def __init__(self, appName="test"):
        self.appName=appName

    def __enter__(self):
        self.spark = SparkSession \
                    .builder \
                    .appName(self.appName) \
                    .getOrCreate()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.spark.stop()

    def read_csv_with_pyspark(self, filepath, delimiter=","):
        sparkDF = self.spark.read.options(delimiter="|", header=True).csv(filepath)
        return sparkDF

    def convertPd2SparkDF(self, pd_df: pd.DataFrame):
        sparkDF = self.spark.createDataFrame(pd_df)
        return sparkDF

    def send2kafka(self, keyPairDF=None, connect_str=None, topic=None):
        """
        send2kafka(sparkDF, host="192.168.1.61:6667", topic="PYSPARK.campaign")
        """
        keyPairDF.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
                .write \
                .format("kafka") \
                .option("kafka.bootstrap.servers", connect_str) \
                .option("topic", topic) \
                .save()


def format_scala_int(x):
    if not x:
        return 0

    if isinstance(x, int):
        return x
    elif isinstance(x, float):
        return int(x)
    elif isinstance(x, str):
        if x.isnumeric:
            return int(float(x))
        else:
            return x

def format_int(df, subset):
    headers = list(df.columns)
    for field in subset:
        if field in headers:
            #float(x) first due to int not able to deal with int('1.0')
            df[field]=df[field].apply(lambda x: format_scala_int(x))
        else:
            print(f'{field} column not exists')
    return df



def format_scala_float(x):
    if not x:
        return float(0)

    if isinstance(x, int):
        return float(x)
    elif isinstance(x, float):
        return x
    elif isinstance(x, str):
        if x.isnumeric:
            return float(x)
        else:
            return x

def format_float(df, subset):
    headers = list(df.columns)
    for field in subset:
        if field in headers:
            df[field] = df[field].apply(lambda x: format_scala_float(x))
        else:
            print(f"{field} column not exists")
    return df


def numeric_format(sparkDF, subset, data_type="int"):
    df = sparkDF

    headers = sparkDF.columns
    for field in subset:
        if field in headers:
            df=df.withColumn(field, col(field).cast(data_type))
            
    return df

def read_csv_from_sftp(sftp, filepath, delimiter=","):
    print(filepath)
    f = sftp.open(filepath)
    f.prefetch()
    df = pd.read_csv(f, delimiter=delimiter)
    return df


def convert2str(pd_df):
    df = pd_df
    headers = list(df.columns)
    for header in headers:
        df[header]=df[header].astype(str)
    return df

def add_index_column(pd_df, index_column_name="key"):
    df =pd_df
    df[index_column_name] = df.index + 1
    return df

def add_key_column(pd_df):
    df = pd_df
    # get datetime of today
    today = datetime.datetime.now()
    # conver the datetime to string
    now_datetime_str = datetime.datetime.strftime(today, '%Y-%m-%d %H:%M:%S')
    # concat the now_datetime_str and row index as unique
    # sometime the row index is not exists in the dataframe, so i regenereate
    indicesSeries = pd.Series([i+1 for i in range(df.shape[0])])
    df["key"] = now_datetime_str + "_" + indicesSeries

    return df

def convertPd2SparkDF(pd_df: pd.DataFrame):
    sparkDF = spark.createDataFrame(pd_df)
    return sparkDF


def send2kafka(keyPairDF=None, connect_str=None, topic=None):
    """
    send2kafka(sparkDF, host="192.168.1.61:6667", topic="PYSPARK.campaign")
    """
    keyPairDF.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
            .write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", connect_str) \
            .option("topic", topic) \
            .save()

########################################this method too slow
def pd_change_local_to_another_timezone(datetime_without_tz, origin_timezone, new_timezone):
    # print(datetime_without_tz)
    datetime_with_tz = origin_timezone.localize(datetime_without_tz, is_dst=None)
    return datetime_with_tz.astimezone(new_timezone)

def pd_change_timezone_to_millsecond(dataframe, subset, origin_timezone, new_timezone):

    df = dataframe

    origin_timezone = pytz.timezone(origin_timezone)
    new_timezone = pytz.timezone(new_timezone)

    for field in subset:
        df[field] = pd.to_datetime(df[field], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        df[field]=df[field].apply(lambda x: pd_change_local_to_another_timezone(x,
                                                                            origin_timezone, 
                                                                            new_timezone))

        #change to millisecond
        df[field]=df[field].dt.strftime("%s")+"000"
    return df





def change_timezone_to_millsecond(dataframe, subset, origin_timezone, new_timezone):
    # origin_timezone = "Asia/Hong_Kong"
    # new_timezone = "UTC"
    origin_timezone = pytz.timezone(origin_timezone)
    new_timezone = pytz.timezone(new_timezone)

    df = dataframe

    #customer function
    def change_local_to_another_timezone(datetime_without_tz):
        # print(datetime_without_tz)
        if datetime_without_tz:
            datetime_without_tz = pd.to_datetime(datetime_without_tz, format="%Y-%m-%d %H:%M:%S", errors="coerce")
            datetime_with_tz = origin_timezone.localize(datetime_without_tz, is_dst=None)
            #change the timezone
            t = datetime_with_tz.astimezone(new_timezone)
            #time to str
            t_str = datetime.datetime.strftime(t, '%s') + "000"
            #return cast to int
            return int(t_str)
        else:
            return datetime_without_tz

    udf_change_local_timezone = udf(change_local_to_another_timezone)

    for field in subset:
        df = df.withColumn(field, udf_change_local_timezone(col(field)))

    return df


def replace_na_value_dict(target_dict):
    target_dict = {k:"" if not v else v for k, v in target_dict.items()}
    return target_dict
def replace_str_dict_na_value(str_dict):
    print(type(str_dict))
    str_dict = str_dict.replace("null", "\"\"")
    return str_dict




def udf_replace_keyvaluepair_value_col_null(keypair_DF):
    udf_replace_str_dict_na_value = udf(replace_str_dict_na_value)
    keypair_DF = keypair_DF.withColumn("value", udf_replace_str_dict_na_value(col("value")))
    return keypair_DF


def udf_string_null_format(sparkDF, subset=None):
    def replace_value(str_value):
        if not str_value:
            return ""

        return str_value
    udf_replace_value = udf(replace_value)
    headers = sparkDF.columns
    for field in subset:
        if field in headers:
            sparkDF = sparkDF.withColumn(field, udf_replace_value(col(field)))
            if sparkDF.schema[field].dataType==StringType():
                sparkDF = sparkDF.withColumn(field, udf_replace_value(col(field)))
            else:
                print(f'   column {field} is not string type')
        else:
            print(f'   column {field} is not valid')
    return sparkDF


    new_sparkDF.dtypes