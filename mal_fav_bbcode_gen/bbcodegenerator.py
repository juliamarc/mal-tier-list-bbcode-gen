import bbcode


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
