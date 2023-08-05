import sys
import os
from pathlib import Path
from .youtube_api import YouTube

print('=======Generate Credentials========')
try:
    if len(sys.argv) < 2:
        print('Some arguments are missing. Usage python -m ayv path/to/secrets/file')
        print('=========Exiting==========')
        sys.exit()   
    print('Generating credentials.....')
    secrets_file = sys.argv[1]
    if os.path.exists(secrets_file) and Path(secrets_file).is_file():
        youtube = YouTube()
        youtube.generate_credentials(secrets_file)
        credentials_path = youtube.get_credentials_path()
        print(f'Credentials stored at: {credentials_path}')
        print('=======Done Generating Credentials========')
        sys.exit()
    print(f'The file {secrets_file} does not exist.')
    print('=========Exiting==========')
    sys.exit(1)
except KeyboardInterrupt:
    print('=========Exiting==========')
    sys.exit(1)