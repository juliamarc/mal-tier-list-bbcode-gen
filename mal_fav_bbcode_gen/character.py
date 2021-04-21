from urllib.parse import unquote

from mal_fav_bbcode_gen.image import Image


class Character(Image):
    def __init__(self, mal_url, image_source, image_url):
        super(Character, self).__init__(image_source, image_url)
        self.mal_url = mal_url
        self.name = unquote(self.mal_url.split("/")[-1]).replace("_", " ")

    def __repr__(self):
        return self.name

    def get_bbcode(self):
        return f'[url={self.mal_url}][img]{self.image_url}[/img][/url]'