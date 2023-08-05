from datetime import datetime
from distutils.log import error
import fnmatch
import os
import paramiko
from cetl.utils.builder import pd
import json
from cetl.utils.file_mgt import get_temp_name, get_file_ext

class SFTP:
    def __init__(self, 
                host=None, 
                port=22, 
                username=None, 
                password=None):

        self.host=host
        self.port=port
        self.username=username
        self.password = password

    def __enter__(self, ):
        tran = paramiko.Transport((self.host, int(self.port)))
        tran.connect(username=self.username, password=self.password)
        self.transport = tran

        try:        
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp = sftp
            return self
        except:
            self.transport.close()
            raise

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.sftp.close()
        self.transport.close()

    def search_file_in_sftp(self, target_dir, template_str):
        temp=[]
        for filename in self.sftp.listdir(target_dir):
            # print("#############", template_str)
            # print("              ", filename)
            if fnmatch.fnmatch(filename, template_str):
                temp.append(os.path.join(target_dir, filename))
        return temp

    def search_source_files(self, target_dir=None, template_strs=None):
        filepaths = []
        for template_str in template_strs:
            if not template_str:
                filepaths.append("")
            else:
                paths = self.search_file_in_sftp(target_dir, template_str)
                paths.sort()
                if len(paths)>0:
                    filepaths.append(paths[-1])#we want to get the latest one
                else:
                    filepaths.append("")

        # print(f'find paths: ', filepaths)
        return filepaths


    def search_range_of_files(self, target_dir=None, start=None, end=None, file_filter_regex=None):
        
        filenames = self.sftp.listdir(target_dir)

        # filter the filenames with target file_ext
        filter_filenames = []
        for filename in filenames:
            # file_filter_regex is like "my*.csv"
            if fnmatch.fnmatch(filename, file_filter_regex):
                filter_filenames.append(filename)

        # sort the filenames
        # https://www.geeksforgeeks.org/python-how-to-sort-a-list-of-strings/
        filter_filenames.sort()

        # get the position range
        if not start:
            start_pos = 0
        else:
            start_pos = filter_filenames.index(start)

        if not end:
            end_pos = -1
            filter_filenames = filter_filenames[::end_pos]
        else:
            end_pos = filter_filenames.index(end)+1
            filter_filenames = filter_filenames[start_pos:end_pos]
        
        filter_filepaths = [os.path.join(target_dir, filename) for filename in filter_filenames]
        all_filepaths = [os.path.join(target_dir, filename) for filename in filter_filenames]


        return all_filepaths, filter_filepaths


    def is_file_exists(self, filepath):
        target_dir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        filepaths = self.search_file_in_sftp(target_dir, filename)
        if len(filepaths)>0:
            return True
        else:
            return False

    def remove_file(self, filepath):
        self.sftp.remove(filepath)

    def move_file(self, filename, from_dir, to_dir, overwrite=True):
        from_path = os.path.join(from_dir, filename)
        to_path = os.path.join(to_dir, filename)
        if self.is_file_exists(to_path) and overwrite:
            self.remove_file(to_path)
        self.sftp.rename(from_path, to_path)

    def read_csv_from_sftp(self, filepath, delimiter=",", header=0):
        # open the csv file
        with self.sftp.open(filepath) as f:
            f.prefetch()
            # print(header, "##########################################")
            df = pd.read_csv(f, delimiter=delimiter, header=header)
            return df

    def read_excel_from_sftp(self, 
                            filepath, 
                            delimiter=",", 
                            header=0,
                            skiprow_start=1,
                            skiprow_end=-1,
                            sheet_name=None, 
                            column_dtype=None):
                            

        with self.sftp.open(filepath) as f:
            f.prefetch()
            #dtype=column_dtype,
            df = pd.read_excel(f, sheet_name=sheet_name, index_col=None, header=header, skiprows = range(skiprow_start-1, skiprow_end))
            return df

    
    def read_json_as_dict(self, filepath):
        # open the jso nfile
        with self.sftp.open(filepath) as f:
            f.prefetch()
            json_data = json.load(f)
            return json_data


    def write_csv_to_sftp(self, filepaths, dfs, sep=",", header=None):
        for filepath, df in zip(filepaths, dfs):
            w = self.sftp.open(filepath, "w")
            w.write(df.to_csv(index=False, sep=sep, header=header))
    
    def write_temp_csv_to_sftp(self,
                                out_dir=None, 
                                file_prefix_list=None,
                                file_suffix_list=None,
                                dfs=None,
                                sep=None, 
                                header=True):

        filepaths= []
        for file_prefix, file_suffix in zip(file_prefix_list, file_suffix_list):
            out_file = os.path.join(out_dir, get_temp_name(file_prefix, file_suffix))
            filepaths.append(out_file)
        
        self.write_csv_to_sftp(filepaths, dfs, sep, header)

        return filepaths

    def mkdir(self, remote_directory):
        dir_path = str()
        for dir_folder in remote_directory.split("/"):
            if dir_folder == "":
                continue
            dir_path += r"/{0}".format(dir_folder)
            try:
                self.sftp.listdir(dir_path)
            except IOError:
                self.sftp.mkdir(dir_path)


def search_file_in_sftp(sftp, target_dir, template_str):
        temp=[]
        for filename in sftp.listdir(target_dir):
                if fnmatch.fnmatch(filename, template_str):
                       temp.append(os.path.join(target_dir, filename))
        return temp

def is_file_exists(sftp, filepath):
    target_dir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    filepaths = search_file_in_sftp(sftp, target_dir, filename)
    if len(filepaths)>0:
        if filepaths[0]==filepath:
            return True
        else:
            return False
    else:
        return False



def remove_file(sftp, filepath):
    sftp.remove(filepath)

def move_file(sftp, filename, from_dir, to_dir, overwrite=True):
    from_path = os.path.join(from_dir, filename)
    to_path = os.path.join(to_dir, filename)
    if is_file_exists(sftp, to_path):
        remove_file(sftp, to_path)
    sftp.rename(from_path, to_path)