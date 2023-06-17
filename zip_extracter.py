from zipfile import ZipFile

'''This function extracts the zipped data with a parameter file_index for specifying a file
    through the native python library zipfile'''
def extract(fileIndex):
    file_path = 'Adobe_API results/' + 'output' + str(fileIndex) + '.zip'
    with ZipFile(file_path,'r') as file:
        output_path = 'Extracted_outputs/' + 'output' + str(fileIndex)
        file.extractall(output_path)

