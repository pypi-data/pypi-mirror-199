class YouTubeSearchQuery:
    """A query to pass to the search resource."""
    
    def __init__(self, query_string: str):
        self.__query_string = query_string
        
    @property
    def query_string(self):
        return self.__query_string
    
    @query_string.setter
    def query_string(self, query_str: str):
        if not query_str:
            raise ValueError('The query string has to be provided')
        if not isinstance(query_str, str):
            raise TypeError('The query string has to be a string')
        self.__query_string = query_str