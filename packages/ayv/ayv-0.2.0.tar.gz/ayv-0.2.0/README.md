# ayv (Analytics for YouTube Videos)

> A library to use with the YouTube API. With it you can find, manage and analyze YouTube resources (Videos, Channels, Playlists, Broadcasts e.t.c) from python scripts.

## Installation

```sh
pip install ayv
```

## Get started

To get started, you a verified Google Account and Google API keys. Follow this [tutorial]() that details the process of getting the API keys as well as enabling the neccssary services and authorizing a test account for use with the library.

To find videos matching a particular search query like *Python programming videos*, import the library, then provide it with the path to the credentials file that you downloaded from Google:

```sh
from ayv import YouTube

credentials_file = '/home/user/Downloads/credentials.json'
token_path = '/home/user'
youtube = Youtube(credentials_file, token_path)
```

Then call the ``search_videos`` method on the youtube object with the query.

```sh
python_programming_videos = youtube.search_videos('python programming videos')
```

To find the most popular Kenyan YouTube Videos:

```sh
most_popular_ke_videos = youtube.find_most_popular_videos_by_region('ke')
```
