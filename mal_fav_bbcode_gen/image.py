import re


class Image:
    SOURCES = ['direct URL', 'Google Drive']

    def __init__(self, image_source, image_url):
        self.image_source = image_source
        self.image_url = image_url
        self._process_image_url()

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

    def get_bbcode(self):
        return f'[img]{self.image_url}[/img]'
