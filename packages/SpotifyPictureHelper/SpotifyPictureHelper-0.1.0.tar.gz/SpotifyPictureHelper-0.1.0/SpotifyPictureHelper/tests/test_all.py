from SpotifyPictureHelper import main as spotify
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import os
import pytest


class TestSpotifyHelper:
    def test_make_request(self):
        response = spotify.make_request('https://open.spotify.com/user/rosycarina')
        assert response.url == 'https://open.spotify.com/user/rosycarina'

    @patch('requests.get')
    def test_get_soup(self, mock_requests):
        # mocking HTTP response
        mock_response = MagicMock()
        mock_response.content = "<!DOCTYPE html>\n"
        soup = spotify.get_soup(mock_response)
        # asserting that the soup text and mock response text are the same
        assert mock_response.content == soup.prettify()

    def test_process_user_profile_pic(self):
        # fake HTML to create BeautifulSoup object
        with open(os.path.join(os.sys.path[0], "fakeUser.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.process_user_profile_pic(soup) == (
                'rosycarina',
                'https://i.scdn.co/image/ab6775700000ee85c88b63d30ae5472bf4bee010',
            )

    def test_get_public_playlists_albums(self):
        with open(os.path.join(os.sys.path[0], "fakeUser.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.get_public_playlists_albums(soup) == ('rosycarina', 10)

    def test_get_individual_album_covers_from_mosaic(self):
        pre = "https://lite-images-i.scdn.co/image/"
        string = "ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6"
        assert spotify.get_individual_album_covers_from_mosaic(
            'https://mosaic.scdn.co/300/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164fc6'
        ) == [pre + string[:40], pre + string[40:80], pre + string[80:120], pre + string[120:]]

    def test_get_individual_album_covers_from_mosaic_invalid_html(self):
        html = "skjfslf;ls"
        with pytest.raises(Exception):
            spotify.get_individual_album_covers_from_mosaic(html)

    def test_get_individual_album_covers_from_mosaic_incomplete_html(self):
        html = "https://mosaic.scdn.co/"
        with pytest.raises(Exception):
            spotify.get_individual_album_covers_from_mosaic(html)

    def test_get_individual_album_covers_from_mosaic_invalid_length(self):
        html = "https://mosaic.scdn.co/ab67616d00001e022a6ab83ec179747bc3b190dcab67616d00001e02335534788cbc39cfd23ee993ab67616d00001e02d6df3bccf3ec41ea2f76debcab67616d00001e02f0855ff71aa79ab842164"
        with pytest.raises(Exception):
            spotify.get_individual_album_covers_from_mosaic(html)

    def test_get_playlist_profile_pic(self):
        with open(os.path.join(os.sys.path[0], "fakePlaylist.html"), "r") as f:
            fake_html = f.read()
            soup = BeautifulSoup(fake_html, "html.parser")
            assert spotify.get_playlist_profile_pic(soup) == (
                'Daily Mix 4',
                "https://dailymix-images.scdn.co/v2/img/ab6761610000e5eb2f8dfdfeb85c3fc2d11b2ae2/4/en/default",
            )

    def test_process_artist_album(self):
        fake_html = ''
        with open(os.path.join(os.sys.path[0], "fakeArtist.html"), "r") as f:
            fake_html = f.read()
        soup = BeautifulSoup(fake_html, "html.parser")
        assert spotify.process_artist_album(soup)[0] == {
            'albumName': 'Midnights (3am Edition)',
            'albumLink': '/album/3lS1y25WAhcqJDATJK70Mq',
            'albumImageUrl': 'https://i.scdn.co/image/ab67616d00001e02e0b60c608586d88252b8fbc0',
            'albumSlug': 'midnights-(3am-edition)',
        }
