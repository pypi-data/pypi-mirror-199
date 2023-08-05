from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
import json
from google.oauth2.credentials import Credentials
import os
from pathlib import Path
from .oauth_constants import YouTubeAPIOauthConstants


class YouTubeAPIAuth:
    __TOKEN_FILE = YouTubeAPIOauthConstants.TOKEN_FILE
    __API_SERVICE_NAME = YouTubeAPIOauthConstants.API_SERVICE_NAME
    __API_VERSION = YouTubeAPIOauthConstants.API_VERSION
    __SCOPES = YouTubeAPIOauthConstants.SCOPES
    
    def __init__(self):
        self.__credentials_path = None
        self.__client_secrets_file = None
        self.__credentials = None
        
    def get_credentials_path(self):
        return self.__credentials_path
    
    def authenticate_from_client_secrets_file(self, client_secrets_file: str, 
                                              credentials_path: str = ''):
        self.__verify_client_secret_file(client_secrets_file)
        self.__client_secrets_file = client_secrets_file
        if not credentials_path or not os.path.exists(credentials_path):
            self.__credentials_path = self.__get_default_credentials_path()
        else:
            self.__credentials_path = credentials_path
        return self.__from_client_secrets_file()
    
    def authenticate_from_credentials(self, credentials_path: str):
        if not credentials_path:
            raise ValueError('The credentials file path has to be provided.')
        if not isinstance(credentials_path, str):
            raise TypeError('The credentials file should be a string.')
        if not os.path.exists(credentials_path):
            raise ValueError('The credentials file path has to exist!')
        if not Path(credentials_path).is_file():
            raise ValueError('The credentials path must be a file.')
        with open(credentials_path, "r") as credentials:
            self.__credentials = Credentials(**json.load(credentials))
        return self.__from_credentials()
            
    
    def __verify_client_secret_file(self, client_secrets_file: str) -> None:
        """Verfy the client secret file."""
        if not client_secrets_file:
            raise ValueError('The clients secret file path has to be provided.')
        if not isinstance(client_secrets_file, str):
            raise TypeError('The clients secret file should be a string.')
        if not os.path.exists(client_secrets_file):
            raise ValueError(f'The path {client_secrets_file} does not exist!')
            
    def __get_default_credentials_path(self):
        """Generate the default api token file location."""
        current_user_home_dir = os.path.expanduser('~')
        credentials_path = os.path.join(current_user_home_dir, self.__TOKEN_FILE)
        return credentials_path
    
    def __from_client_secrets_file(self):
        if os.path.exists(self.__credentials_path):
            with open(self.__credentials_path, "r") as credentials:
                self.__credentials = Credentials(**json.load(credentials))
        if not self.__credentials or not self.__credentials.valid:
            if self.__credentials and self.__credentials.expired and self.__credentials.refresh_token:
                self.__credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__client_secrets_file, self.__SCOPES)
                self.__credentials = flow.run_local_server(port=0)
            with open(self.__credentials_path, "w") as credentials_path:
                credentials = self.__credentials_to_dict(self.__credentials)
                json.dump(credentials, credentials_path)
        youtube_api_client = build(self.__API_SERVICE_NAME, self.__API_VERSION, 
                                   credentials=self.__credentials)
        return youtube_api_client
    
    def __from_credentials(self):
        if not self.__credentials or not self.__credentials.valid:
            if self.__credentials and self.__credentials.expired and self.__credentials.refresh_token:
                self.__credentials.refresh(Request())
            with open(self.__credentials_path, "w") as credentials_path:
                credentials = self.__credentials_to_dict(self.__credentials)
                json.dump(credentials, credentials_path)
        youtube_api_client = build(self.__API_SERVICE_NAME, self.__API_VERSION, 
                                   credentials=self.__credentials)
        return youtube_api_client
    
    def generate_credentials(self, client_secrets_file: str, credentials_path: str = ''):
        self.__verify_client_secret_file(client_secrets_file)
        self.__client_secrets_file = client_secrets_file
        if not credentials_path or not os.path.exists(credentials_path):
            self.__credentials_path = self.__get_default_credentials_path()
        else:
            self.__credentials_path = credentials_path
        flow = Flow.from_client_secrets_file(
            self.__client_secrets_file,
            scopes=self.__SCOPES,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        auth_url, _ = flow.authorization_url(prompt='consent')

        print('Please go to this URL: {}'.format(auth_url))
        code = input('Enter the authorization code: ')
        flow.fetch_token(code=code)
        self.__credentials = flow.credentials
        credentials_dict = self.__credentials_to_dict(self.__credentials)
        with open(self.__credentials_path, "w") as credentials_path:
            json.dump(credentials_dict, credentials_path)
    
    def __credentials_to_dict(self, credentials: Credentials) -> dict:
        """Convert credentials to a dict for easy work with Flask."""
        return dict(
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=credentials.scopes
        )