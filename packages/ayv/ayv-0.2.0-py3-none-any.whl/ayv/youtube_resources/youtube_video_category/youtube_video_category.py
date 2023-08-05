class YouTubeVideoCategory:
    def __init__(self, id, title):
        self.__id = id
        self.__title = title
        
    def get_id(self):
        return self.__id
    
    def get_title(self):
        return self.__title
    
    def __str__(self):
        return self.get_title()
    
    def __repr__(self):
        return f"YouTubeVideoCategory(id='{self.__id}', title='{self.__title}')"