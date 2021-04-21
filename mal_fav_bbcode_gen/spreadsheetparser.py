from collections import defaultdict
from math import isclose

import ezodf

from mal_fav_bbcode_gen.character import Character
from mal_fav_bbcode_gen.header import Header


class SpreadsheetParser:
    SETTINGS_SHEET_NAME = 'SETTINGS'
    CHARACTERS_PER_ROW_ADDRESS = 'E2'
    TIER_LIST_ROW_START = 2
    TIER_LIST_ROW_END = 16
    CHAR_LIST_ROW_START = 5
    CHAR_LIST_ROW_END = 54

    def __init__(self, file_name):
        self.file_name = file_name
        self.spreadsheet = ezodf.opendoc(file_name)
        self.settings = self._parse_settings()
        self.tiers = None

    def _parse_settings(self):
        settings = {}
        try:
            sheet = self.spreadsheet.sheets[self.SETTINGS_SHEET_NAME]
        except KeyError:
            raise KeyError(
                f"Sheet {self.SETTINGS_SHEET_NAME} not found in spreadsheet.")

        tier_names = []
        for i in range(self.TIER_LIST_ROW_START-1, self.TIER_LIST_ROW_END):
            val = sheet.row(i)[0].value
            if val is not None:
                if isinstance(val, float) and isclose(val, int(val)):
                    val = int(val)
                tier_names.append(str(val))

        tier_names = list(dict.fromkeys(tier_names))

        missing = set(tier_names) - set(self.spreadsheet.sheets.names())
        if missing:
            print(f"WARNING the following tiers were specified in SETTINGS "
                  f"but do not match any sheet in the spreadsheet: "
                  f"{', '.join(missing)}")

        settings['tier_names'] = [t for t in tier_names if t not in missing]
        settings['characters_per_row'] = int(
            sheet[self.CHARACTERS_PER_ROW_ADDRESS].value)

        return settings

    def parse_tiers(self):
        tiers = defaultdict(dict)

        for tier in self.settings['tier_names']:
            sheet = self.spreadsheet.sheets[tier]

            header_entry = [cell.value for cell in sheet.row(1)[1:4]]
            tiers[tier]['header'] = Header(*header_entry)

            characters = []
            for i in range(self.CHAR_LIST_ROW_START-1, self.CHAR_LIST_ROW_END):
                character_entry = [cell.value for cell in sheet.row(i)[1:4]]
                if all(character_entry):
                    characters.append(Character(*character_entry))
                elif any(character_entry):
                    print(f"WARNING Incomplete character entry in sheet "
                          f"'{tier}' at row {i+1}")

            tiers[tier]['characters'] = characters

        self.tiers = dict(tiers)
