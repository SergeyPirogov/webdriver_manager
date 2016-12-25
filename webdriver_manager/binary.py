import os


class Binary(object):
    def __init__(self, path):
        self.bin_file = file(path)

    @property
    def path(self):
        return self.bin_file.name

    @property
    def name(self):
        return os.path.splitext(os.path.basename(self.bin_file.name))[0]
