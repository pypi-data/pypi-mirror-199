from commons.openpyxl_wo_formatting import OpenpyxlReaderWOFormatting
from commons.utils import sanitize
import math


class Photo:
    def __init__(self, workbook_filename, asset) -> None:
        xlsmReader = OpenpyxlReaderWOFormatting(workbook_filename)

        workbook = xlsmReader.load_workbook(workbook_filename)
        worksheet = workbook['BCA Worksheet']

        self.photos = []
        row_offset = 0
        eid_cell = worksheet.cell(row=5, column=1)
        while self.has_system_data(eid_cell.value):
            photo_set_index = 39
            photo_cell = worksheet.cell(row=5+row_offset, column=photo_set_index)
            while photo_cell.value != None:
                if not (photo_cell.hyperlink == None):
                    self.photos.append(
                        {"system_eid": eid_cell.value, "asset": asset, "name": photo_cell.value,
                        "url": photo_cell.hyperlink.target}
                    )
                photo_set_index = photo_set_index + 1
                photo_cell = worksheet.cell(row=5+row_offset, column=photo_set_index)
            row_offset = row_offset + 1
            eid_cell = worksheet.cell(row=5+row_offset, column=1)
            
    def has_system_data(self, eid):
        return eid != None and eid != "" and not (type(eid) == float and math.isnan(eid))

    def create_insert_sql(self):
        sqls = []
        for photo in self.photos:
            sqls.append(
                f"  INSERT INTO PHOTOS (ASSET_ID, SYSTEM_ID, CAPTION, PATH)\n" +
                f"  VALUES (\n" +
                f"    asset_id,\n" +
                f"    null,\n" +
                f"    '',\n" +
                f"    {sanitize(photo['url'])}\n" +
                f"  );\n"
            )
        return "\n\n".join(sqls)
