from mal_fav_bbcode_gen.bbcodegenerator import BBCodeGenerator
from mal_fav_bbcode_gen.spreadsheetparser import SpreadsheetParser


def main():
    parser = SpreadsheetParser("tiers.ods")
    parser.parse_tiers()

    generator = BBCodeGenerator(parser)
    generator.generate_bbcode()
    generator.write_html_preview_to_file('preview.html')
    generator.write_bbcode_to_file('bbcode.txt')
