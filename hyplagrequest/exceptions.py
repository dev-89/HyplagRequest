class HyplagRequestException(Exception): 
    def __init__(self, value): 
        self.value = value
    def __str__(self): 
        return "Error: %s" % self.value