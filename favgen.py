from urllib.parse import unquote
from collections import defaultdict

import bbcode
import ezodf


class Header:
    def __init__(self, include, image_source, image):
        self.include = True if include == 'yes' else False
        self.image_source = image_source
        self.image = image

    def __repr__(self):
        return str(self.include)

    def get_bbcode(self):
        if self.image_source == 'direct URL':
            return f'[img]{self.image}[/img]'
        else:
            raise NotImplementedError(
                "Currently 'direct URL' is the only method of providing images")


class Character:
    def __init__(self, mal_url, image_source, image):
        self.mal_url = mal_url
        self.image_source = image_source
        self.image = image
        self.name = unquote(mal_url.split("/")[-1]).replace("_", " ")

    def __repr__(self):
        return self.name

    def get_bbcode(self):
        if self.image_source == 'direct URL':
            return f'[url={self.mal_url}][img]{self.image}[/img][/url]'
        else:
            raise NotImplementedError(
                "Currently 'direct URL' is the only method of providing images")


class SpreadsheetParser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.spreadsheet = ezodf.opendoc(file_name)
        self.settings = self._parse_settings()
        self.tiers = None


    def _parse_settings(self):
        settings = {}
        try:
            sheet = self.spreadsheet.sheets["SETTINGS"]
        except KeyError:
            raise KeyError("Sheet 'SETTINGS' not found in spreadsheet.")

        tier_names = []
        for i in range(1, 16):
            val = sheet.row(i)[0].value
            if val is not None:
                tier_names.append(val)

        missing = set(tier_names) - set(self.spreadsheet.sheets.names())
        if missing:
            print(f"WARNING the following tiers were specified in SETTINGS but do "
                  f"not match any sheet in the spreadsheet: {list(missing)}")

        settings['tier_names'] = [t for t in tier_names if t not in missing]
        settings['characters_per_row'] = int(sheet['G2'].value)

        return settings


    def parse_tiers(self):
        tiers = defaultdict(dict)

        for tier in self.settings['tier_names']:
            sheet = self.spreadsheet.sheets[tier]

            header_entry = [cell.value for cell in sheet.row(1)[1:4]]
            tiers[tier]['header'] = Header(*header_entry)

            characters = []
            for i in range(4, 54):
                character_entry = [cell.value for cell in sheet.row(i)[1:4]]
                if all(character_entry):
                    characters.append(Character(*character_entry))
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

        print(f"BBCode written to {file_name}")


    def write_html_preview_to_file(self, file_name):
        parser = bbcode.Parser(replace_links=False)
        parser.add_simple_formatter('img', '<img src=%(value)s>')
        html = parser.format(self.bbcode)
        with open(file_name, "w") as f:
            f.write(html)

        print(f'HTML preview written to {file_name}')


def main():
    parser = SpreadsheetParser("tiers.ods")
    parser.parse_tiers()
    generator = BBCodeGenerator(parser)
    generator.generate_bbcode()
    generator.write_html_preview_to_file('preview.html')
    generator.write_bbcode_to_file('bbcode.txt')


if __name__ == "__main__":
    main()
