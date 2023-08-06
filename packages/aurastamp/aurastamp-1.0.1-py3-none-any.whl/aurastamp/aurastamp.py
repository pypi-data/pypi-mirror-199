from .aurastamp_image import AurastampImage

class Aurastamp(object):
    def __init__(self, server_url=None):
        self.image = AurastampImage(server_url)