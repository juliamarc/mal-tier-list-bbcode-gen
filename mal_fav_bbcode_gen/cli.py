from os.path import basename, splitext

import click

from mal_fav_bbcode_gen.bbcodegenerator import BBCodeGenerator
from mal_fav_bbcode_gen.spreadsheetparser import SpreadsheetParser


@click.command()
@click.option('--preview', '-p', is_flag=True,
              help='Generate HTML preview of the BBCode. '
              'Doesn\'t save the BBCode.')
@click.option('--output_path', default=None, type=str,
              help='Path to file where the BBCode will be saved. Default '
              'path is generated based on the input file name like this: '
              '<name>.ods -> <name>.bbcode.txt')
@click.argument('ods_file_path', type=click.Path(exists=True))
def main(preview, output_path, ods_file_path):
    parser = SpreadsheetParser(ods_file_path)
    parser.parse_tiers()

    generator = BBCodeGenerator(parser)
    generator.generate_bbcode()
    if preview:
        generator.write_html_preview_to_file('preview.html')
    else:
        if not output_path:
            output_path = splitext(basename(ods_file_path))[0] + '.bbcode.txt'
        generator.write_bbcode_to_file(output_path)