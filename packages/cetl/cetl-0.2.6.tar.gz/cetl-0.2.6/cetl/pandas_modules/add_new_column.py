import numpy as np
from datetime import datetime
from ..utils.builder import DataFrame, PANDAS_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper
from ..utils.formating import addUniqueKeyList

@PANDAS_TRANSFORMERS.add()
class addNewColumn(Base):
    """This transformer is to add new column to the pandas dataframe

    Args:
        base_field (str):   Indicate the new column name to be added
        value (str): Indicate the value in the new column
    Returns:
        df (pandas.DataFrame): the data container type is dataframe

    Usage:
        {"type":"addNewColumn", "base_field":"Tier", "value":""}
    """
    def __init__(self, 
                base_field=None,
                value=None):
        super().__init__()
        self.base_field = base_field
        self.value = value

    @transform_wrapper
    def transform(self, dataframe: DataFrame):
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe
        df[self.base_field] = self.value
        
        return df

@PANDAS_TRANSFORMERS.add()
class addNewColumns(Base):
    """
    Usage:
        {"type":"addNewColumns", "base_fields":["Tier"], "values":[""]}
    """
    def __init__(self, 
                base_fields=None,
                values=None):
        super().__init__()
        self.base_fields = base_fields
        self.values = values

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe

        for field, value in zip(self.base_fields, self.values):
                df[field] = value
        return df


@PANDAS_TRANSFORMERS.add()
class addNewColumnForIsWithinDayDiff(Base):
    """
    Usage:
        {"type":"addNewColumnForIsWithinDayDiff", "new_field":"", "date_field1":"", "date_field2":"", "day_limit":5}
    """
    def __init__(self, 
                new_field=None,
                date_field1=None,
                date_field2=None,
                day_limit=None):
        super().__init__()
        self.date_field1 = date_field1
        self.date_field2 = date_field2
        self.day_limit = day_limit
        self.new_field = new_field

        # if filter=="true":
        #     self.filter=True
        # else:
        #     self.filter=False

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe

        df[self.new_field] = abs(df[self.date_field1]-df[self.date_field2])
        df[self.new_field] = df[self.new_field].dt.days<=self.day_limit

        # if self.filter:
        #     df = df[df[self.new_field]]

        return df



@PANDAS_TRANSFORMERS.add()
class addNewColumnForDayDiff(Base):
    """
    {"type":"addNewColumnForDayDiff", "new_field":"", "date_field1":"", "date_field2":""}
    """
    def __init__(self, 
                new_field=None,
                date_field1=None,
                date_field2=None):
        super().__init__()

        self.new_field = new_field
        self.date_field1 = date_field1
        self.date_field2 = date_field2

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe

        df[self.new_field] = (df[self.date_field1]-df[self.date_field2]).dt.days


        return df


@PANDAS_TRANSFORMERS.add()
class addNewColumnWithNowDatetimeStr(Base):
    """
    {"type":"addNewColumnWithNowDatetimeStr", "new_field":"", "format":"'%Y-%m-%d %H:%M:%S'"}
    """
    def __init__(self, 
                new_field=None,
                format=None):
        super().__init__()

        self.new_field = new_field
        self.format = format

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe

        # create now datetime string
        today = datetime.now()
        now_datetime_str = datetime.strftime(today, self.format)
        df[self.new_field] = now_datetime_str
        
        return df



@PANDAS_TRANSFORMERS.add()
class addNewColumnByPdSeries(Base):
    def __init__(self, 
                base_field=None,
                pd_series=None):

        super().__init__()
        self.base_field = base_field
        self.pd_series = pd_series

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe
        df[self.base_field] = self.pd_series
        return df



@PANDAS_TRANSFORMERS.add()
class addNewColumnFromExisting(Base):
    """
    {"type":"addNewColumnFromExisting", "base_field":"", "new_field":""}
    """
    def __init__(self,
                 base_field=None,
                 new_field=None):

        super().__init__()
        self.base_field = base_field
        self.new_field = new_field
    

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe
        df[self.new_field] = df[self.base_field]
        return df  



@PANDAS_TRANSFORMERS.add()
class addKeyColumnFromExisting(Base):
    def __init__(self,
                 subset=None,
                 new_field=None):
        super().__init__()

        self.subset = subset
        self.new_field = new_field

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe
        headers = df.columns
        df[self.new_field]=""
        for field in self.subset:
            if field in headers:
                pd_series = df[field]
                df[self.new_field] = df[self.base_field] + "_" + pd_series.astype(str)
            else:
                print(f"no field named {field} in the dataframe")
        
        df[self.new_field] = df[self.new_field].apply(lambda x: x[1:])
        return df


@PANDAS_TRANSFORMERS.add()
class addNowColumn(Base):
    def __init__(self,
                 base_field=None,
                 now_format=None):
        super().__init__()

        self.base_field = base_field
        self.now_format = now_format


    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        pass



@PANDAS_TRANSFORMERS.add()
class addNewFromConcatExistingColumns(Base):
    """"
    {"type":"addNewFromConcatExistingColumns", "subset":"", "new_fieldname":"", "delimiter":""}
    """
    def __init__(self,
                 subset=None,
                 new_fieldname=None,
                 delimiter=" "):
        super().__init__()

        self.subset = subset
        self.new_fieldname = new_fieldname
        self.delimiter=delimiter

    def concat_values(self, delimiter, values):
        if delimiter:
            new_value = delimiter.join(values)
        else:
            new_value = "".join(values)
        
        return new_value

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        df = dataframe

        headers = df.columns

        exist_headers = []
        df[self.new_fieldname]=""
        for field in self.subset:
            if field in headers:
                exist_headers.append(field)
            else:
                print(f"header {field} not exist in the dataframe")
                
        # concat method 2
        df[self.new_fieldname] = df[exist_headers[0]]+"_"+df[exist_headers[1]]
        # df[self.new_fieldname]=df.apply(lambda r: self.concat_values(self.delimiter, r[exist_headers]), axis=1)
        
        return df


@PANDAS_TRANSFORMERS.add()
class addUniqueKeyColumn(Base):
    """
    {"type":"addUniqueKeyColumn", "base_field":"", "value_prefix":"IMP1", "value_suffix":"", "value_start":1, "padding_digit":6}
    """
    def __init__(self,
                 base_field=None,
                 value_start=None,
                 value_prefix=None,
                 value_suffix=None,
                 padding_digit=None):
        super().__init__()

        self.base_field = base_field
        self.value_start = value_start
        self.value_prefix = value_prefix
        self.value_suffix = value_suffix
        self.padding_digit = padding_digit

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        df = dataframe
        

        value_end = df.shape[0]
        df[self.base_field] = addUniqueKeyList(value_prefix=self.value_prefix,
                                                value_suffix=self.value_suffix,
                                                value_start=self.value_start, 
                                                value_end = value_end, 
                                                padding_digit=self.padding_digit)

        return df



@PANDAS_TRANSFORMERS.add()
class addNewFromMultiplyCalculation(Base):
    """
    {"type":"addNewFromMultiplyCalculation", "new_field":"", 
            "multiply_fields":["Quantity", "Discount"]}
    """
    def __init__(self,
                 new_field=None,
                 multiply_fields=None):
        super().__init__()

        self.new_field = new_field
        self.multiply_fields = multiply_fields


    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        df = dataframe

        headers = df.columns 

        # true fields checking
        true_fields = []
        for field in self.multiply_fields:
            if field in headers:
                true_fields.append(field)
            else:
                print(f"field {field} not exists")

        df[self.new_field] = 1
        
        for field in true_fields:
            df[self.new_field] = df[self.new_field] * df[field]

        return df


@PANDAS_TRANSFORMERS.add()
class addNewFromMinusCalculation(Base):
    """
    {"type":"addNewFromMinusCalculation", "new_field":"", 
            "minus_fields":["gap_to_next_grade", "Discount"]}
    """
    def __init__(self,
                 new_field=None,
                 minus_fields=None):
        super().__init__()

        self.new_field = new_field
        self.minus_fields = minus_fields

    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        df = dataframe

        headers = df.columns 

        # true fields checking
        true_fields = []
        for field in self.minus_fields:
            if field in headers:
                true_fields.append(field)
            else:
                print(f"field {field} not exists")

        
        
        for i, field in enumerate(true_fields):
            if i ==0:
                df[self.new_field] = df[field]
            else:
                df[self.new_field] = df[self.new_field] - df[field]

        return df
        



@PANDAS_TRANSFORMERS.add()
class addMarkColumnFromWithinPeriod(Base):
    """
    {"type":"addMarkColumnFromWithinPeriod", "new_field":"isWithinGradePeriod", "period_start_field":"EffectiveDate", 
        "period_end_field":"ExpiryDate", "check_datetime_field":"MovementDate")
    """
    def __init__(self,
                 new_field=None,
                 period_start_field=None,
                 period_end_field=None,
                 check_datetime_field=None):
        super().__init__()

        self.new_field = new_field
        self.period_start_field = period_start_field
        self.period_end_field = period_end_field
        self.check_datetime_field = check_datetime_field

    @transform_wrapper
    def transform(self, dataframe) -> DataFrame:
        df = dataframe
        c1 = df[self.period_start_field]<=df[self.check_datetime_field]
        c2 = df[self.check_datetime_field]<=df[self.period_end_field]

        # df=None
        df[self.new_field] = "0"
        df.loc[(c1 & c2), self.new_field] = "1"
        return df



@PANDAS_TRANSFORMERS.add()
class addNewColumnWithReplaceDict(Base):
    """
    {"type":"addNewColumnWithReplaceDict", "new_field":"", "base_field":"", "values_dict":{}}
    """
    def __init__(self,
                new_field=None,
                base_field=None,
                values_dict=None):
        super().__init__()

        self.new_field = new_field
        self.base_field = base_field
        self.values_dict = values_dict

    @transform_wrapper
    def transform(self, dataframe) -> DataFrame:

        df = dataframe

        #create the new field
        df[self.new_field] = ""
        df[self.new_field] = df[self.base_field].replace(self.values_dict)

        return df

@PANDAS_TRANSFORMERS.add()
class addNewColumnWithDateAdjustment(Base):
    """
    {"type":"addNewColumnWithDateAdjustment", "new_field":"", "base_field":"", "year":-1, "month":0, "day":0}
    """
    def __init__(self,
                new_field=None,
                base_field=None,
                year=None,
                month=None,
                day=None):
        super().__init__()

        self.new_field = new_field
        self.base_field = base_field
        self.year = 0 if not year else year
        self.month = 0 if not month else month
        self.day = 0 if not day else day


    @transform_wrapper
    def transform(self, dataframe) -> DataFrame:

        df = dataframe

        #create the new field
        df[self.new_field] = df[self.base_field].apply(lambda x: x.replace(year=x.year+self.year, 
                                                    month=x.month+self.month,
                                                    day=x.day+self.day))
        return df

@PANDAS_TRANSFORMERS.add()
class addNewColumnWithDateTimeAdjustment(Base):
    """
    {"type":"addNewColumnWithDateAdjustment", "new_field":"", "base_field":"", "year":-1, "month":0, "day":0, "hour":23, "minute":59, "second":59}
    """
    def __init__(self,
                new_field=None,
                base_field=None,
                year=None,
                month=None,
                day=None,
                hour=None,
                minute=None,
                second=None):
        super().__init__()

        self.new_field = new_field
        self.base_field = base_field
        self.year = 0 if not year else year
        self.month = 0 if not month else month
        self.day = 0 if not day else day
        self.hour = 0 if not hour else hour
        self.minute = 0 if not minute else minute
        self.second = 0 if not second else second


    @transform_wrapper
    def transform(self, dataframe) -> DataFrame:

        df = dataframe


        def replace_datetime(x):

            # print(f"month:{x.month}, day:{x.day}")
            #avoid non leap year Feb 29
            cond1 = (x.year+self.year) % 4 >0
            cond2 = (x.month+self.month)==2
            cond3 = (x.day + self.day) == 29
            
            if cond1 and cond2 and cond3:
                return x.replace(year=x.year+self.year, 
                        month=x.month + self.month,
                        day=x.day + self.day - 1,
                        hour=x.hour + self.hour,
                        minute=x.minute + self.minute,
                        second=x.second + self.second)
            else:
                return x.replace(year=x.year+self.year, 
                        month=x.month + self.month,
                        day=x.day + self.day,
                        hour=x.hour + self.hour,
                        minute=x.minute + self.minute,
                        second=x.second + self.second)


        #create the new field
        df[self.new_field] = df[self.base_field].apply(lambda x: replace_datetime(x))
        return df



@PANDAS_TRANSFORMERS.add()
class addNewColumnFromGradeHistory(Base):
    """
    {"type":"addNewColumnFromGradeHistory", "sort_fields":["customer_id", "id"], "grouping_fields":["customer_id"], 
        "grade_history_id":"id", "new_field":"pre_grade_history_id", "is_ascending":"true", "na_position":"last"}

    Description: This method is going to help you find the pre-grade is of the same customer
    """
    def __init__(self,
                sort_fields=None,
                grouping_fields=None,
                grade_history_id=None,
                new_field=None,
                is_ascending=None,
                na_position="last"):
        super().__init__()

        self.sort_fields = sort_fields
        self.grouping_fields = grouping_fields
        self.grade_history_id = grade_history_id
        self.new_field = new_field
        if is_ascending=="true":
            self.is_ascending=True
        else:
            self.is_ascending=False

        self.na_position = na_position


    @transform_wrapper
    def transform(self, dataframe) -> DataFrame:

        df = dataframe

        # step 1: sort value by field of customer (i.e. customer_id)
        # if sort_fields is ["customer_id", "id"], then sorting is done from the right to the left
        # i.e. sort "id" first, then sort by "customer_id"
        df = df.sort_values(by=self.sort_fields, ascending=self.is_ascending, na_position=self.na_position)

        # step 2: get the list of grade history ids
        pre_grade_history_id_list = df[self.grade_history_id].to_list()
        pre_grade_history_id_list = [None] + pre_grade_history_id_list[:-1]

        # step 3: create the new field
        # print(pre_grade_history_id_list)
        # assert False
        df[self.new_field] = pre_grade_history_id_list

        # step 4: edit the first record of each group (customers)
        # print(f"df.groupby({self.grouping_fields})[{self.sort_fields}].head({1}).index")
        c = df.groupby(self.grouping_fields)[self.sort_fields].head(1).index
        df.loc[c, self.new_field] = None

        # format to int
        # df[self.new_field]=df[self.new_field].astype(int)

        return df



@PANDAS_TRANSFORMERS.add()
class addNewColumnFromEvalStatement(Base):
    """
    {"type":"addNewColumnFromEvalStatement", "new_field":"grade_value", "eval_value":"df[\"grade_id\"]-df[\"pre_grade_id\"]"}

    Description: This method is going to help you find the pre-grade is of the same customer
    """
    def __init__(self,
                new_field=None,
                eval_value=None):
        super().__init__()

        self.new_field = new_field
        self.eval_value = eval_value



    @transform_wrapper
    def transform(self, dataframe) -> DataFrame:

        df = dataframe

        df[self.new_field]=eval(self.eval_value)

        return df


@PANDAS_TRANSFORMERS.add()
class addGradeChangeType(Base):
    """
    {"type":"addGradeChangeType", "new_field":"temp_grade_change", "grade_diff":"grade_diff"}
    """
    def __init__(self, grade_diff=None, new_field=None):
        super().__init__()

        self.grade_diff=grade_diff
        self.new_field = new_field



    @transform_wrapper
    def transform(self, dataframe) -> DataFrame:
        df = dataframe

        # df[self.grade_diff].fillna(-800)

        c= (df[self.grade_diff]>0) & (df[self.grade_diff]<9)
        df.loc[c, self.new_field]="UPGRADE"

        c= (df[self.grade_diff]>=9)
        df.loc[c, self.new_field]="Set_Grade"
        
        c= df[self.grade_diff]<0
        df.loc[c, self.new_field]="DOWNGRADE"

        c= df[self.grade_diff]==0
        df.loc[c, self.new_field]="Renew"


        c = df[self.grade_diff].isnull()
        df.loc[c, self.new_field]="Opening Grade"

        
        return df

@PANDAS_TRANSFORMERS.add()
class addNewColumnForRowNumberToGroup(Base):
    """
    {"type":"addNewColumnForRowNumberToGroup", "group_fields":[], "new_field":""}
    """
    def __init__(self, 
                group_fields=None, 
                new_field=None):
        super().__init__()
        
        self.group_fields=group_fields
        self.new_field = new_field



    @transform_wrapper
    def transform(self, dataframe: DataFrame) -> DataFrame:
        #skip transformation if dataframe is an empty dataframe
        if dataframe.empty:
            return dataframe

        df = dataframe

        df[self.new_field] = df.groupby(self.group_fields).cumcount()+1
        
        return df