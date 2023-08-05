from .builder import FILE_TRANSFORMERS
import tarfile
from glob import glob
import os
import sys
sys.path.insert(0, os.path.join(".."))
from cetl import Base, transform_wrapper, context_name

@FILE_TRANSFORMERS.add()
class compress2Tar(Base):
    def __init__(   self, 
                    target_dir=None, 
                    file_filter_regex=None,
                    out_dir=None,
                    out_file=None):
        super().__init__()

        self.target_dir = target_dir
        self.file_filter_regex = file_filter_regex
        self.out_dir = out_dir
        self.out_file = out_file


    @transform_wrapper
    def transform(self, input):
        # retrieve filepaths
        filepaths = glob(os.path.join(self.target_dir, self.file_filter_regex))


        # compress file one by one into the out_archive
        out_archive = os.path.join(self.out_dir, self.out_file)
        with tarfile.open(out_archive, 'w:gz') as archive:
            for filepath in filepaths:
                archive.add(filepath)
            return {context_name:out_archive}
        
