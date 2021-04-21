from math import isclose

import ezodf

import mal_fav_bbcode_gen.utils as utils

from mal_fav_bbcode_gen.character import Character
from mal_fav_bbcode_gen.image import Image


class HeaderIncompleteError(Exception):  # pragma: no cover
    def __init__(self, message):
        super().__init__(message)


class CharactersPerRowMissingError(Exception):  # pragma: no cover
    def __init__(self, message):
        super().__init__(message)


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
        self.tiers = {}

    def _get_settings_sheet(self):
        try:
            return self.spreadsheet.sheets[self.SETTINGS_SHEET_NAME]
        except KeyError:
            raise KeyError(
                f"Sheet {self.SETTINGS_SHEET_NAME} not found in spreadsheet.")

    def _parse_tier_list(self, sheet):
        tier_names = []

        for i in range(self.TIER_LIST_ROW_START-1, self.TIER_LIST_ROW_END):
            val = sheet.row(i)[0].value
            if val is not None:
                if isinstance(val, float) and isclose(val, int(val)):
                    val = int(val)
                tier_names.append(str(val))

        tier_names = utils.deduplicate_list(tier_names)

        return tier_names

    def _check_for_missing_tier_sheets(self, tier_names):
        missing = set(tier_names) - set(self.spreadsheet.sheets.names())
        if missing:
            print(f"WARNING the following tiers were specified in SETTINGS "
                  f"but do not match any sheet in the spreadsheet: "
                  f"{', '.join(missing)}")

        return missing

    def _filter_tier_names(self, tier_names, missing):
        return [t for t in tier_names if t not in missing]

    def _get_chars_per_row_setting(self, sheet):
        try:
            return int(sheet[self.CHARACTERS_PER_ROW_ADDRESS].value)
        except TypeError:
            raise CharactersPerRowMissingError(
                f"'Characters per row' setting missing from settings sheet "
                f"{self.SETTINGS_SHEET_NAME}. Should be in cell "
                f"{self.CHARACTERS_PER_ROW_ADDRESS}")

    def _parse_settings(self):
        settings = {}
        sheet = self._get_settings_sheet()
        tier_names = self._parse_tier_list(sheet)
        missing = self._check_for_missing_tier_sheets(tier_names)

        settings['tier_names'] = self._filter_tier_names(tier_names, missing)
        settings['characters_per_row'] = self._get_chars_per_row_setting(sheet)

        return settings

    def _parse_header(self, sheet, tier_name):
        header_entry = [cell.value for cell in sheet.row(1)[1:4]]

        if header_entry[0] == 'yes':
            if all(header_entry):
                header = Image(*header_entry[1:])
                return header
            else:
                raise HeaderIncompleteError(
                    f"Incomplete header entry in sheet '{tier_name}'.")
        else:
            return None

    def _parse_character(self, sheet_row, row_number, tier_name):
        character_entry = [cell.value for cell in sheet_row[1:4]]

        if all(character_entry):
            return Character(*character_entry)
        elif any(character_entry):
            print(f"WARNING Incomplete character entry in sheet "
                  f"'{tier_name}' at row {row_number}")

            return None

    def _parse_characters(self, sheet, tier_name):
        characters = []

        for i in range(self.CHAR_LIST_ROW_START-1, self.CHAR_LIST_ROW_END):
            character = self._parse_character(sheet.row(i), i, tier_name)
            if character:
                characters.append(character)

        return characters

    def _parse_tier(self, tier_name):
        sheet = self.spreadsheet.sheets[tier_name]
        header = self._parse_header(sheet, tier_name)
        characters = self._parse_characters(sheet, tier_name)

        return {'header': header, 'characters': characters}

    def parse_tiers(self):
        for tier_name in self.settings['tier_names']:
            self.tiers[tier_name] = self._parse_tier(tier_name)
