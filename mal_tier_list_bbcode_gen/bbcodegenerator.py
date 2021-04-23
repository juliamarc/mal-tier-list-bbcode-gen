import bbcode


class BBCodeGenerator:
    def __init__(self, settings, tiers):
        self.settings = settings
        self.tiers = tiers
        self.bbcode = None

    def generate_bbcode(self):
        self.bbcode = ''

        for _, tier in self.tiers.items():
            no_entries = len(tier['entries'])

            if tier['header']:
                self.bbcode += tier['header'].get_bbcode() + '\n'

            per_row = self.settings['entries_per_row']
            force_tile = True if per_row > 0 else False
            if force_tile:
                newline_after = range(
                    per_row-1, no_entries-1, per_row)

            for i, entry in enumerate(tier['entries']):
                self.bbcode += entry.get_bbcode()
                if force_tile and i in newline_after:
                    self.bbcode += '\n'

            if no_entries > 0:
                self.bbcode += '\n'

    def write_bbcode_to_file(self, file_name):  # pragma: no cover
        with open(file_name, "w") as f:
            f.write(self.bbcode)

        print(f"BBCode saved to {file_name}")

    def _generate_html_preview(self):
        parser = bbcode.Parser(replace_links=False)
        parser.add_simple_formatter('img', '<img src=%(value)s>')

        return parser.format(self.bbcode)

    def write_html_preview_to_file(self, file_name):  # pragma: no cover
        html = self._generate_html_preview()
        with open(file_name, "w") as f:
            f.write(html)

        print(f'HTML preview saved to {file_name}')
