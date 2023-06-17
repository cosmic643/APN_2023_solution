import os

def dir_handler():
    if(not os.path.exists("Adobe_API results")):
        os.mkdir("Adobe_API results")

    if(not os.path.exists("Extracted_outputs")):
        os.mkdir("Extracted_outputs")