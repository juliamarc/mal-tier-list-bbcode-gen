from mal_fav_bbcode_gen.image import Image


class Header(Image):
    def __init__(self, include, image_source, image_url):
        super(Header, self).__init__(image_source, image_url)
        self.include = True if include == 'yes' else False

    def __repr__(self):
        return str(self.include)
