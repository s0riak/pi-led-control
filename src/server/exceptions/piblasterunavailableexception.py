class PiBlasterUnavailableException(Exception):
    
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(PiBlasterUnavailableException, self).__init__(message)