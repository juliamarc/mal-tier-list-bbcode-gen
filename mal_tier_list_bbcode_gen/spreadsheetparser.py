import warnings

from math import isclose

import ezodf

import mal_tier_list_bbcode_gen.exceptions as exceptions
import mal_tier_list_bbcode_gen.utils as utils

from mal_tier_list_bbcode_gen.entry import Entry
from mal_tier_list_bbcode_gen.image import Image


class SpreadsheetParser:
    SETTINGS_SHEET_NAME = 'SETTINGS'
    ENTRIES_PER_ROW_ADDRESS = 'E2'
    TIER_ORDER_ROW_START = 2
    TIER_ORDER_ROW_END = 16
    ENTRY_LIST_ROW_START = 5
    ENTRY_LIST_ROW_END = 54

    def __init__(self, ods_file_path):
        self.ods_file_path = ods_file_path
        self.spreadsheet = self._read_ods_file(ods_file_path)

        self.settings = self._parse_settings()
        self.tiers = {}

    def _read_ods_file(self, ods_file_path):
        try:
            return ezodf.opendoc(ods_file_path)
        except KeyError:
            raise FileNotFoundError(f"Path '{ods_file_path}' does not exist.")

    def _get_settings_sheet(self):
        try:
            return self.spreadsheet.sheets[self.SETTINGS_SHEET_NAME]
        except KeyError:
            raise exceptions.SettingsSheetMissingError(
                f"Sheet {self.SETTINGS_SHEET_NAME} not found in spreadsheet.")

    def _parse_tier_order(self, sheet):
        tier_names = []

        for i in range(self.TIER_ORDER_ROW_START-1, self.TIER_ORDER_ROW_END):
            val = sheet.row(i)[0].value
            if val is not None:
                if isinstance(val, float) and isclose(val, int(val)):
                    val = int(val)
                tier_names.append(str(val))

        tier_names = utils.deduplicate_list(tier_names)

        return tier_names

    def _check_for_missing_tier_sheets(self, tier_names):
        sheets_names = list(self.spreadsheet.sheets.names())
        missing = set(tier_names) - set(sheets_names)
        if missing:
            warnings.warn(
                f"The following tiers were specified in the "
                f"'{self.SETTINGS_SHEET_NAME}' sheet but do not match any "
                f"sheet in the spreadsheet: {', '.join(missing)}. Sheets in "
                f"spreadsheet: {', '.join(sheets_names)}.")

        return missing

    def _get_entries_per_row_setting(self, sheet):
        entries_per_row = sheet[self.ENTRIES_PER_ROW_ADDRESS].value
        if entries_per_row is None:
            raise exceptions.EntriesPerRowMissingError(
                f"'Entries per row' setting missing from settings sheet "
                f"{self.SETTINGS_SHEET_NAME}. Should be in cell "
                f"{self.ENTRIES_PER_ROW_ADDRESS}")
        elif isinstance(entries_per_row, float):
            entries_per_row = int(entries_per_row)
            if entries_per_row >= 0:
                return entries_per_row
            else:
                warnings.warn(
                    "'Entries per row' setting set to less than 0. Defaulting "
                    " to 0 (free flow tiling).")
                return 0
        else:
            raise exceptions.EntriesPerRowNotANumberError(
                f"'Entries per row' setting from sheet "
                f"'{self.SETTINGS_SHEET_NAME}' should be a number.")

    def _parse_settings(self):
        settings = {}
        sheet = self._get_settings_sheet()
        tier_names = self._parse_tier_order(sheet)
        missing = self._check_for_missing_tier_sheets(tier_names)

        settings['tier_names'] = utils.filter_list_by_set(tier_names, missing)
        settings['entries_per_row'] = self._get_entries_per_row_setting(sheet)

        return settings

    def _parse_header(self, sheet, tier_name):
        header_entry = [cell.value for cell in sheet.row(1)[1:4]]

        if header_entry[0] == 'yes':
            if all(header_entry):
                header = Image(*header_entry[1:])
                return header

            raise exceptions.HeaderIncompleteError(
                f"Incomplete header entry in sheet '{tier_name}'.")

        return None

    def _parse_entry(self, sheet_row, row_number, tier_name):
        entry = [cell.value for cell in sheet_row[1:4]]

        if all(entry):
            return Entry(*entry)
        elif any(entry):
            warnings.warn(
                f"Incomplete entry in sheet '{tier_name}' at sheet row "
                f"{row_number+1}.")

        return None

    def _parse_entries(self, sheet, tier_name):
        entries = []

        for i in range(self.ENTRY_LIST_ROW_START-1, self.ENTRY_LIST_ROW_END):
            entry = self._parse_entry(sheet.row(i), i, tier_name)
            if entry:
                entries.append(entry)

        return entries

    def _parse_tier(self, tier_name):
        sheet = self.spreadsheet.sheets[tier_name]
        header = self._parse_header(sheet, tier_name)
        entries = self._parse_entries(sheet, tier_name)

        return {'header': header, 'entries': entries}

    def parse_tiers(self):
        for tier_name in self.settings['tier_names']:
            self.tiers[tier_name] = self._parse_tier(tier_name)
