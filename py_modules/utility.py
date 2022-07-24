
from os.path import basename, dirname, splitext, split
import os
import glob

# Generates basepath ... to project directory 
basePath = split(dirname(__file__))[0]

def clear_outputs():
    # Define paths for different outputs 
    path_output = f"{basePath}/Test/output"
    path_db = f"{basePath}/Test/db"
    path_query = f"{basePath}/Test/query"

    os.system(f"rm -rf {path_output}/*")
    os.system(f"rm -rf {path_db}/*")
    os.system(f"rm -rf {path_query}/*")


