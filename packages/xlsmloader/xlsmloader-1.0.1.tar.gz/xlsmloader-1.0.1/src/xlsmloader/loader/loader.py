import glob
import sys
import warnings
from datetime import datetime, timedelta
from commons.utils import generate_log_filename, current_milli_time
import commons.openpyxl_wo_formatting as openpyxl_wo_formatting
from models.assets import Asset
from models.systems import System
from models.photos import Photo

warnings.simplefilter("ignore", category=UserWarning)

def load():
    if len(sys.argv) <= 1:
        directory_path = input("Inform the XLSM file directory: ")
    else:
        directory_path = sys.argv[1]

    start_time_ms = current_milli_time()
    print(f"Processing start time {datetime.now()}")
    print(f"processing XLSM files from {directory_path}")
    xlsm_files = glob.glob(directory_path + '/*.xlsm')
    print(f"{len(xlsm_files)} files found.")

    with open(generate_log_filename(), "w") as sql_file:
        sql_file.write("DECLARE\n")
        sql_file.write("  description_clob CLOB;\n")
        sql_file.write("  asset_id number;\n")
        sql_file.write("  system_id number;\n")
        sql_file.write("BEGIN\n")
        for workbook_filename in xlsm_files:
            print(f"reading file {workbook_filename}...")
            asset = Asset(workbook_filename)
            system = System(workbook_filename, asset)
            photo = Photo(workbook_filename, asset)
            sql_file.write(asset.create_update_sql())
            sql_file.write("\r\n\n")
            sql_file.write(system.create_update_sql())
            sql_file.write("\r\n\n")
            sql_file.write(photo.create_insert_sql())
            sql_file.write("\r\n")
        sql_file.write("  COMMIT;\n")
        sql_file.write("END;\n")
        sql_file.close()

    print(f"Processing finished time {datetime.now()}")
    end_time_ms = current_milli_time()
    elapsed_time_ms = end_time_ms - start_time_ms
    elapsed_time = timedelta(milliseconds=elapsed_time_ms)
    print(f"Elapsed time: {elapsed_time}")