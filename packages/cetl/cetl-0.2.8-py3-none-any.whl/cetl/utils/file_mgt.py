from datetime import datetime
import fnmatch
import os
import tempfile

def gen_uniq_filename(filename):
        today = datetime.now()
        # conver the datetime to string
        now_datetime_str = datetime.strftime(today, '%Y-%m-%d %H:%M:%S')
        return now_datetime_str

def get_datetime_for_filename(format='%Y%m%d%H%M%S'):
        today = datetime.now()
        # conver the datetime to string
        now_datetime_str = datetime.strftime(today, format)
        return now_datetime_str

def get_temp_name(file_prefix, file_suffix):
        # generate temp outfile
        file_datetime = get_datetime_for_filename()
        temp = tempfile.NamedTemporaryFile(prefix=file_prefix+file_datetime+"_", suffix=file_suffix)
        basename = os.path.basename(temp.name)
        return basename

def get_file_ext(filename):
        split_values = filename.split(".")
        if len(split_values)>1:
                ext = "."+split_values[-1]
        else:
                ext = ""
        return ext

def get_datetime_str(format=None):
    today = datetime.now()
    now_datetime_str = datetime.strftime(today, format)
    return now_datetime_str

