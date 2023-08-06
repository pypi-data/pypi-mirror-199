from file_modules import compress2Tar
import sys, os

sys.path.insert(0, os.path.join(".."))
from cetl import build_pipeline


filepath = current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(filepath)


c = compress2Tar(   target_dir=os.path.join(current_dir, "images"),
                    file_filter_regex="*.png",
                    out_dir=os.path.join(current_dir, "images"),
                    out_file = "images.tar.gz")

pipe = build_pipeline(c)

result = pipe.transform("")
print(result)


# python test_file_compress.py