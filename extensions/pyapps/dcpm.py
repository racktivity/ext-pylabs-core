from pylabs import p


class DCPM(object):

    def __init__(self):
        # Initialize p.api for DCPM if possible
        try:
            p.api = p.application.getAPI("dcpm")  #pylint: disable=E1101
        except RuntimeError:
            pass
