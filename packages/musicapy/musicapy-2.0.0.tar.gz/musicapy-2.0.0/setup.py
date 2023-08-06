# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musicapy', 'musicapy.saavn_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'wget>=3.2,<4.0']

extras_require = \
{'docs': ['sphinx>=6.1.3,<7.0.0',
          'sphinx-rtd-theme>=1.2.0,<2.0.0',
          'myst-parser>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'musicapy',
    'version': '2.0.0',
    'description': 'Python wrapper for several music platforms API',
    'long_description': "# MusicAPy\n\nMusic API Python wrapper, currently supports limited API.\n\n- Supported API\n  - JioSaavn\n\n## Docs Deployment Status\n\n[![Deploy Docs](https://github.com/dmdhrumilmistry/MusicAPy/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/dmdhrumilmistry/MusicAPy/actions/workflows/deploy-docs.yml)\n\n## Installation\n\n- Using pip and git\n\n    ```bash\n    python3 -m pip install git+https://github.com/dmdhrumilmistry/MusicAPy\n    ```\n\n- Using pypi\n\n    ```bash\n    python3 -m pip install MusicAPy\n    ```\n\n## Usage\n\n- Jio Saavn API\n\n  - From Script\n\n    ```python\n    from musicapy.saavn_api.api import SaavnAPI\n    \n    # create API obj\n    api = SaavnAPI()\n    \n    \n    ## Search Services\n    # Search Song\n    data = api.search_song('song_name')\n\n    # Search Album\n    data = api.search_album('album_name')\n\n    # Search All\n    data = api.search_all('song_or_album_name')\n\n    ## Song Services\n    # get song link\n    saavn_song_link = 'https://www.jiosaavn.com/song/song_name/id'\n    \n    # create identifier\n    identifier = api.create_identifier(link, 'song')\n\n    # get trending songs\n    trending_songs = api.get_trending()\n\n    # get latest charts\n    charts = api.get_charts()\n\n    # get song link from identifier\n    song_link = api.get_song_link(identifier)\n\n    # get song details\n    details = api.get_song_details(identifier)\n\n    # get song lyrics\n    lyrics = api.get_song_lyrics(identifier)\n\n    # get download links\n    download_links = api.generate_song_download_links(identifier)\n\n    ## Albums Service\n    # get song details\n    album_details = api.get_album_details(identifier)\n    \n    # get album songs download links\n    data = api.generate_album_download_links(identifier) \n\n    ## Playlist Service\n    # with featured playlist link\n    id = api.create_identifier('https://www.jiosaavn.com/featured/arijits-sad-songs/8RkefqkCO1huOxiEGmm6lQ__', None)\n\n    # with playlist link\n    id = api.create_identifier('https://www.jiosaavn.com/s/playlist/a60306bf0bd5cacc95a888a361163e07/Ppll/Iz0pi7nkjUHfemJ68FuXsA__', 'playlist')\n\n    # with playlist/list id\n    id = api.create_identifier(802336660, 'playlist')\n\n    # fetch playlist details\n    playlist_details = api.get_playlist_details(id)\n\n    # fetch Playlist song details with download links\n    playlist_songs_details = api.get_playlist_song_download_links(id)\n    ```\n\n  - From Command Line\n\n    ```bash\n    python3 -m musicapy.saavn_api -h\n    ```\n\n    > Command Line Output\n\n    ```bash\n    usage: __main__.py [-h] [-t] [-c] [-d] [-l LINK] [-aD] [-a] [-sS SEARCH_SONG_QUERY] [-sA SEARCH_ALBUM_QUERY] [-sa SEARCH_ALL_QUERY]\n\n    options:\n      -h, --help            show this help message and exit\n      -t, --trending        get trending songs\n      -c, --charts          get charts\n      -d, --download        generate download links\n      -l LINK, --link LINK  link of song or album\n      -aD, --album-details  get album details from link\n      -a, --album           get album download links\n      -sS SEARCH_SONG_QUERY, --search-song SEARCH_SONG_QUERY\n                            search song by name\n      -sA SEARCH_ALBUM_QUERY, --search-album SEARCH_ALBUM_QUERY\n                            search album by name\n      -sa SEARCH_ALL_QUERY, --search-all SEARCH_ALL_QUERY\n                        search album or song by name\n    ```\n\n## License\n\n[MIT License](https://github.com/dmdhrumilmistry/MusicAPy/blob/main/LICENSE)\n",
    'author': 'Dhrumil Mistry',
    'author_email': '56185972+dmdhrumilmistry@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
