import re

from collections import defaultdict
from math import isclose
from urllib.parse import unquote

import bbcode
import ezodf


class Image:
    SOURCES = ['direct URL', 'Google Drive']

    def _process_image_url(self):
        if self.image_source == 'direct URL':
            pass
        elif self.image_source == 'Google Drive':
            file_id = re.search(r'([-\w]{25,})', self.image_url).group(1)
            self.image_url = f'https://drive.google.com/uc?id={file_id}'
        else:
            msg = f"'{self.image_source}' is not a valid image source. " + \
                  f"Choose from {self.SOURCES}."
            raise KeyError(msg)


class Header(Image):
    def __init__(self, include, image_source, image_url):
        self.include = True if include == 'yes' else False
        self.image_source = image_source
        self.image_url = image_url

        self._process_image_url()

    def __repr__(self):
        return str(self.include)

    def get_bbcode(self):
        return f'[img]{self.image_url}[/img]'


class Character(Image):
    def __init__(self, mal_url, image_source, image_url):
        self.mal_url = mal_url
        self.name = unquote(self.mal_url.split("/")[-1]).replace("_", " ")
        self.image_source = image_source
        self.image_url = image_url

        self._process_image_url()

    def __repr__(self):
        return self.name

    def get_bbcode(self):
        return f'[url={self.mal_url}][img]{self.image_url}[/img][/url]'


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


class BBCodeGenerator:
    def __init__(self, ss_parser):
        self.ss_parser = ss_parser
        self.bbcode = None

    def generate_bbcode(self):
        self.bbcode = ''

        for _, tier in self.ss_parser.tiers.items():
            no_characters = len(tier['characters'])

            if tier['header'].include:
                self.bbcode += tier['header'].get_bbcode() + '\n'

            per_row = self.ss_parser.settings['characters_per_row']
            force_tile = True if per_row > 0 else False
            if force_tile:
                newline_after = range(
                    per_row-1, no_characters-1, per_row)

            for i, character in enumerate(tier['characters']):
                self.bbcode += character.get_bbcode()
                if force_tile and i in newline_after:
                    self.bbcode += '\n'

            if no_characters > 0:
                self.bbcode += '\n'

    def write_bbcode_to_file(self, file_name):
        with open(file_name, "w") as f:
            f.write(self.bbcode)

        print(f"BBCode saved to {file_name}")

    def write_html_preview_to_file(self, file_name):
        parser = bbcode.Parser(replace_links=False)
        parser.add_simple_formatter('img', '<img src=%(value)s>')
        html = parser.format(self.bbcode)
        with open(file_name, "w") as f:
            f.write(html)

        print(f'HTML preview saved to {file_name}')


def main():
    parser = SpreadsheetParser("tiers.ods")
    parser.parse_tiers()

    generator = BBCodeGenerator(parser)
    generator.generate_bbcode()
    generator.write_html_preview_to_file('preview.html')
    generator.write_bbcode_to_file('bbcode.txt')


if __name__ == "__main__":
    main()
