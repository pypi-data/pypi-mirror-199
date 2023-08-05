class YouTubeComment:
    def __init__(self, id: str, videoId: str, totalReplyCount: str, textDisplay: str, 
                authorDisplayName: str, authorProfileImageUrl: str, authorChannelId: str,
                likeCount: str, publishedAt: str, updatedAt: str):
        self.__id = id
        self.__video_id = videoId
        self.__total_reply_count = totalReplyCount
        self.__text_display = textDisplay
        self.__author_display_name = authorDisplayName
        self.__author_profile_image_url = authorProfileImageUrl
        self.__author_channel_id = authorChannelId
        self.__like_count = int(likeCount)
        self.__published_at = publishedAt
        self.__updated_at = updatedAt
        
    def get_comment(self):
        comment = dict(
            id=self.__id,
            videoId=self.__video_id,
            totalReplyCount=self.__total_reply_count,
            textDisplay=self.__text_display,
            authorDisplayName = self.__author_display_name,
            authorProfileImageUrl = self.__author_profile_image_url,
            authorChannelId = self.__author_channel_id,
            likeCount = self.__like_count,
            publishedAt = self.__published_at,
            updatedAt = self.__updated_at
        )
        return comment
    
    def get_comment_text(self):
        comment_text = self.__text_display
        return comment_text
    
    def __str__(self):
        return self.get_comment_text()
    
    def __repr__(self):
        return f"YouTubeComment(id='{self.__id}', videoId='{self.__video_id}', \
        totalReplyCount={self.__total_reply_count})"