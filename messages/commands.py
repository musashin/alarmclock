

class SoundCmd(object):

    def __init__(self, type, **kwargs):
        self.type = type
        try:
            self.track = kwargs['track']
        except:
            pass

        try:
            self.vol = kwargs['vol']
        except:
            pass