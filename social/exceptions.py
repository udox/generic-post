class FacebookParameterException(Exception):

    def __init__(self, param_name):
        self.parameter = param_name

    def __str__(self):
        return '%s parameter is required but is None' % repr(self.parameter)
