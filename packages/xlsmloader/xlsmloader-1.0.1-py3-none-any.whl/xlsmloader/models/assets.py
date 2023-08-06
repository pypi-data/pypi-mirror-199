from commons.utils import to_excel_date, split_oracle_string
import pandas as pd
from commons.utils import sanitize
from commons.converters import province_converter


class Asset:
    
    def __init__(self, workbook_filename) -> None:
        self.__background_worksheet = pd.read_excel(
            workbook_filename,
            engine='openpyxl_wo_formatting',
            skiprows=0,
            sheet_name='Background'
        );

        row_offset = 0;
        self.region = self.__background_worksheet.iloc[row_offset+5, 3]
        self.campus = self.__background_worksheet.iloc[row_offset+6, 3]
        number_and_name = self.__background_worksheet.iloc[row_offset+7,3]
        self.name = number_and_name.split("-")[1].strip()
        self.number = self.__background_worksheet.iloc[row_offset+10,3]
        self.eid = self.__background_worksheet.iloc[row_offset+9,3]
        self.description = self.__background_worksheet.iloc[row_offset+5,10]
        self.size = self.__background_worksheet.iloc[row_offset+22,3]
        self.size_units = self.__background_worksheet.iloc[row_offset+22,4]
        self.year_constructed = self.__background_worksheet.iloc[row_offset+23,3]
        self.type = self.__background_worksheet.iloc[row_offset+24,3]
        self.use = self.__background_worksheet.iloc[row_offset+25,3]
        self.ocupancy = self.__background_worksheet.iloc[row_offset+26,3]
        self.stories = self.__background_worksheet.iloc[row_offset+27,3]
        self.address_line_1 = self.__background_worksheet.iloc[row_offset+28,3]
        self.address_line_2 = self.__background_worksheet.iloc[row_offset+29,3]
        self.city = self.__background_worksheet.iloc[row_offset+30,3]
        self.province = province_converter(self.__background_worksheet.iloc[row_offset+31,3])
        self.postal_code = self.__background_worksheet.iloc[row_offset+32,3]
        self.date_of_assessment = to_excel_date(self.__background_worksheet.iloc[row_offset+34,3])
        self.country = "CA"
        self.currency = "CAD"

    def create_update_sql(self):
        description_chuncks = split_oracle_string(self.description, 1000)
        if len(description_chuncks) == 0:
            description_chuncks = ['']

        sql = (
            f"  UPDATE ASSETS SET\n" +
            f"    ASSET_NUMBER = {sanitize(self.number)},\n" +
            f"    NAME = {sanitize(self.name)},\n    DESCRIPTION = {sanitize(description_chuncks[0])},\n" + 
            f"    ASSET_SIZE = {sanitize(self.size)},\n    SIZE_UNITS = {sanitize(self.size_units)},\n" + 
            f"    YEAR_CONSTRUCTED = {self.year_constructed},\n    ASSET_TYPE = {sanitize(self.type)},\n" +
            f"    ASSET_USE = {sanitize(self.use)},\n    ASSET_OCCUPANCY = {sanitize(self.ocupancy)},\n" +
            f"    STORIES = {sanitize(self.stories)},\n    ADDRESS_LINE_1 = {sanitize(self.address_line_1)},\n" +
            f"    ADDRESS_LINE_2 = {sanitize(self.address_line_2)},\n    CITY = {sanitize(self.city)},\n" +
            f"    PROVINCE = {sanitize(self.province)},\n    POSTAL_CODE = {sanitize(self.postal_code)},\n" +
            f"    COUNTRY = {sanitize(self.country)},\n    CURRENCY = {sanitize(self.currency)},\n" +
            f"    DATE_OF_ASSESSMENT = TO_DATE({sanitize(self.date_of_assessment)}, 'MM/DD/YYYY')\n" +
            f"  WHERE EID = {sanitize(self.eid)}\n" +
            f"  RETURNING DESCRIPTION\n" +
            f"  INTO description_clob;\n\n"
        );
        
        del description_chuncks[0]

        for chunck in description_chuncks:
            sql = sql + (
                f"  DBMS_LOB.writeappend(\n" +
	            f"    description_clob,\n" +
	            f"    LENGTH ({chunck}),\n" +
                f"    {chunck}\n" +
	            f"  );\n\n"
            )
        sql = sql + f"  SELECT id INTO asset_id FROM ASSETS a WHERE EID = {sanitize(self.eid)};\n\n";
        return sql
