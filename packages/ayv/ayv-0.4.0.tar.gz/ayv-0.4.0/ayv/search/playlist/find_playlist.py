from ...youtube_resources.youtube_playlist import Playlist

class FindPlaylist:
    def __init__(self, playlist_id: str):
        """Find the video with the given id."""
        self.__playlist_id = playlist_id
        
    def __generate_basic_info_params(self):
        basic_info_params = dict(
            id=self.__playlist_id,
            part='id,snippet,contentDetails,player',
        ) 
        return basic_info_params
    
    def find_playlist(self, youtube_client):
        """Find the video."""
        basic_info_params = self.__generate_basic_info_params()
        search_request = youtube_client.playlists().list(
                **basic_info_params
            )
        search_response = search_request.execute()
        parsed_response = self.__parse_playlist(search_response)
        youtube_playlist = Playlist(**parsed_response)
        return youtube_playlist
    
    def __parse_playlist(self, search_response):
        playlist_details = dict()
        items = search_response['items'][0]
        playlist_details['id'] = items['id']
        playlist_details['channelId'] = items['snippet']['channelId']
        playlist_details['title'] = items['snippet']['title']
        playlist_details['description'] = items['snippet']['description']
        playlist_details['thumbnails'] = items['snippet']['thumbnails']
        playlist_details['channelTitle'] = items['snippet']['channelTitle']
        playlist_details['itemCount'] = items['contentDetails']['itemCount']
        playlist_details['player'] = items['player']['embedHtml']
        return playlist_details