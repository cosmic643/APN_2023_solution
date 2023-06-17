import directory_handlers
import API_code
import data_extraction_code
import zip_extracter
directory_handlers.dir_handler()
for i in range(100):
    API_code.get_data_from_api(i)
    zip_extracter.extract(i)
    data_extraction_code.extract(i)
