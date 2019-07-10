import os


class Binary(object):
    def __init__(self, path):
        if os.path.isfile(path):
            self.bin_file = open(path)
        elif os.path.isdir(path):
            self.bin_file = open(os.path.join(path, os.listdir(path)[0]))
        else:
            raise FileNotFoundError

    @property
    def path(self):
        return self.bin_file.name

    @property
    def name(self):
        return os.path.splitext(os.path.basename(self.bin_file.name))[0]
