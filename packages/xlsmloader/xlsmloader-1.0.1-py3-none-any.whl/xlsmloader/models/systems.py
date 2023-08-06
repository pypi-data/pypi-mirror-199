from commons.utils import to_excel_datetime, split_oracle_string
import pandas as pd
import math
from commons.utils import sanitize
from commons.converters import requeriment_type_converter

class System:
    def __init__(self, workbook_filename, asset) -> None:
        self.__bca_worksheet = pd.read_excel(
            workbook_filename,
            engine='openpyxl_wo_formatting',
            header=None,
            skiprows=0,
            sheet_name='BCA Worksheet'
        );

        row_offset = 0;
        self.systems = []
        eid = self.__bca_worksheet.iloc[row_offset+4,0]
        self.load_system_data(row_offset, eid)
        while self.has_system_data(eid):
            self.systems.append({
                "asset": asset,
                "eid": eid,
                "name": self.__name,
                "uniformat": self.__uniformat,
                "uniformat_code": self.__uniformat_code,
                "description": self.__description,
                "year_installed": self.__year_installed,
                "lifetime": self.__lifetime,
                "quantity": self.__quantity,
                "unit": self.__unit,
                "unit_cost": self.__unit_cost,
                "percent_renew": self.__percent_renew,
                "date_inspected": self.__date_inspected,
                "inspector": self.__inspector,
                "adjustment_factor": self.__adjustment_factor,
                "renewal_cost": self.__renewal_cost,
                "replacement_cost": self.__replacement_cost,
                "years_remaining": self.__years_remaining,
                "current_year": self.__current_year,
                "requirement_type": self.__requirement_type,
                "requirement_action_item": self.__requirement_action_item
            })
            row_offset = row_offset + 1
            if row_offset+4 >= self.__bca_worksheet.shape[0]:
                eid = ""
            else:
                eid = self.__bca_worksheet.iloc[row_offset+4,0]
            self.load_system_data(row_offset, eid)

    def has_system_data(self, eid):
        return eid != None and eid != "" and not (type(eid) == float and math.isnan(eid))

    def load_system_data(self, row_offset, eid):
        if(self.has_system_data(eid)):
            self.__uniformat = self.__bca_worksheet.iloc[row_offset+4,5]
            self.__uniformat_code = self.__uniformat.split("-")[0].strip()
            self.__name = self.__bca_worksheet.iloc[row_offset+4,8]
            self.__description = self.__bca_worksheet.iloc[row_offset+4,9]
            if type(self.__description) == float:
                self.__description = ""
            self.__current_year = int(self.__bca_worksheet.iloc[0,7])
            self.__year_installed = self.__bca_worksheet.iloc[row_offset+4,13]
            self.__lifetime = self.__bca_worksheet.iloc[row_offset+4,14]
            self.__requirement_type = requeriment_type_converter(self.__bca_worksheet.iloc[row_offset+4,15])
            self.__requirement_action_item = self.__bca_worksheet.iloc[row_offset+4,18]
            self.__quantity = float(self.__bca_worksheet.iloc[row_offset+4, 19])
            self.__unit = self.__bca_worksheet.iloc[row_offset+4, 20]
            self.__unit_cost = float(self.__bca_worksheet.iloc[row_offset+4, 21])
            self.__percent_renew = self.__bca_worksheet.iloc[row_offset+4,22]
            self.__date_inspected = to_excel_datetime(self.__bca_worksheet.iloc[row_offset+4,32])
            self.__inspector = self.__bca_worksheet.iloc[row_offset+4,36]
            self.__adjustment_factor = float(self.__bca_worksheet.iloc[row_offset+4, 25])
            self.__years_remaining = self.__bca_worksheet.iloc[row_offset+4,16]
            if self.__requirement_type != None:
                if self.__requirement_type.upper() == "LIFECYCLE":
                    self.__replacement_cost = float(self.__bca_worksheet.iloc[row_offset+4, 26])
                    self.__renewal_cost = None
                elif self.__requirement_type.upper() == "MAJOR REPAIR":
                    self.__renewal_cost = float(self.__bca_worksheet.iloc[row_offset+4, 26])
                    self.__replacement_cost = None
                else:
                    self.__replacement_cost = None
                    self.__renewal_cost = None
            else:
                self.__replacement_cost = None
                self.__renewal_cost = None

    def create_update_sql(self):
        sqls = []
        for sys in self.systems:
            description_chuncks = split_oracle_string(sys['description'], 1000)
            if len(description_chuncks) == 0:
                description_chuncks = ['']

            sql = (
                f"  UPDATE SYSTEMS SET\n" +
                f"    ASSET_ID = asset_id,\n" +
                f"    UNIFORMAT_CODE = {sanitize(sys['uniformat_code'])},\n" +
                f"    UNIFORMAT = {sanitize(sys['uniformat'])},\n    NAME = {sanitize(sys['name'])},\n" +
                f"    DESCRIPTION = {sanitize(description_chuncks[0])},\n    YEAR_INSTALLED = {sanitize(sys['year_installed'])},\n" +
                f"    LIFETIME = {sanitize(sys['lifetime'])},\n    YEARS_REMAINING = {sys['years_remaining']},\n" +
                f"    QUANTITY = {sanitize(sys['quantity'])},\n    UNIT = {sanitize(sys['unit'])},\n" +
                f"    UNIT_COST = {sanitize(sys['unit_cost'])},\n    PERCENT_RENEW = {sanitize(sys['percent_renew'])},\n" +
                f"    ADJUSTMENT_FACTOR = {sanitize(sys['adjustment_factor'])},\n" +
                f"    DATE_INSPECTED = TO_DATE({sanitize(sys['date_inspected'])}, 'MM/DD/YYYY'),\n" +
                f"    INSPECTOR = {sanitize(sys['inspector'])},\n    RENEWAL_COST = {sanitize(sys['renewal_cost'])},\n" +
                f"    REPLACEMENT_COST = {sanitize(sys['replacement_cost'])}\n"
                f"  WHERE EID = {sanitize(sys['eid'])}\n" +
                f"  RETURNING DESCRIPTION\n" +
                f"  INTO description_clob;\n\n"
            )

            del description_chuncks[0]

            for chunck in description_chuncks:
                sql = sql + (
                    f"  DBMS_LOB.writeappend(\n" +
                    f"    description_clob,\n" +
                    f"    LENGTH ({chunck}),\n" +
                    f"    {chunck}\n" +
                    f"  );\n\n"
                )

            sql = sql + f"  SELECT id INTO system_id FROM SYSTEMS WHERE EID = {sanitize(sys['eid'])};\n\n";

            sql = sql + f"  UPDATE REQUIREMENTS r SET r.NAME = '[LEGACY] ' || r.NAME\n"
            sql = sql + f"  WHERE SYSTEM_ID = system_id\n"
            sql = sql + f"  AND SUBSTR(r.NAME, 1, 8) <> '[LEGACY]';\n\n"

            sql = sql + f"  UPDATE PHOTOS p SET p.CAPTION = '[LEGACY] ' || p.CAPTION\n"
            sql = sql + f"  WHERE ASSET_ID = asset_id\n"
            sql = sql + f"  AND SUBSTR(p.CAPTION, 1, 8) <> '[LEGACY]';\n\n"

            sql = sql + f"  INSERT INTO REQUIREMENTS(SYSTEM_ID, REQUIREMENT_TYPE, ACTION_YEAR)\n"
            sql = sql + f"  VALUES(system_id, {sanitize(sys['requirement_type'])}, {sanitize(sys['requirement_action_item'])});\n\n"

            sqls.append(sql)
        return "\n\n".join(sqls);
