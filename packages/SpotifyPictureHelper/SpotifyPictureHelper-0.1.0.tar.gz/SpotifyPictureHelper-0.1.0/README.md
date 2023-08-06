# SpotifyPictureHelper
This is a library of helper functions that allows users to process images in Spotify. 

![Hex.pm](https://img.shields.io/hexpm/l/apa?style=plastic)
![Hex.pm](https://img.shields.io/github/issues/daisyye0730/spotify_find_beats)
[![Package Status](https://img.shields.io/github/actions/workflow/status/daisyye0730/spotify_find_beats/build.yml)](https://github.com/daisyye0730/spotify_find_beats/)
[![codecov](https://codecov.io/gh/daisyye0730/SpotifyPictureHelper/branch/main/graph/badge.svg)](https://codecov.io/gh/daisyye0730/SpotifyPictureHelper)

## Overview
Some tasks that it performs include:

1. process_user_profile_pic: extracts user profile picture given its html

2. get_public_playlists_albums: extracts all public playlist album covers from a user's html page 

3. get_individual_album_covers_from_mosaic: extracts four individual cover photos from a mosaic cover photo

4. get_playlist_profile_pic: extracts the profile picture from a playlist 

5. process_artist_album: extracts all the album covers of an artist 

6. make_request: accepts a html string and requests a session with the html with a response code 

7. get_soup: accepts the return object from make_request and parses into content acceptable in tasks 1-5

## How to Use  
1. Install the library by running: pip install SpotifyPictureHelper

2. Import the library in Python by including from SpotifyPictureHelper import main

## Details
The following are commands included in the Makefile:
- `make develop`: install the library's dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `black` and `flake8`
- `make format`: autoformat this library with `black`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information (passes with coverage >50%)
- `make clean`: cleans the repo