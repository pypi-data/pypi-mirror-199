from splotify import helpers
from splotify.tests import sp
import pytest
import os


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    return os.path.join("splotify/tests/cassettes", request.module.__name__)


@pytest.mark.vcr()
def test_search_id():
    result = helpers.search_id(sp, "No Surprises")
    assert len(result) == 11
    assert result[0] == ["Name", "Album", "Artists", "URI"]
    assert len(result[1]) == 4
    assert result[1] == [
        "No Surprises",
        "OK Computer",
        ["Radiohead"],
        "spotify:track:10nyNJ6zNy2YVYLrcwLccB",
    ]

    result = helpers.search_id(sp, "OK Computer", limit=23, type="album")
    assert len(result) == 24
    assert result[0] == ["Name", "Artists", "URI"]
    assert len(result[1]) == 3
    assert result[1] == [
        "OK Computer",
        ["Radiohead"],
        "spotify:album:6dVIqQ8qmQ5GBnJ9shOYGE",
    ]

    result = helpers.search_id(sp, "Radiohead", limit=15, type="artist")
    assert len(result) == 16
    assert result[0] == ["Name", "URI"]
    assert len(result[1]) == 2
    assert result[1] == ["Radiohead", "spotify:artist:4Z8W4fKeB5YxbusRsdQVPb"]

    result = helpers.search_id(sp, "This is Radiohead", limit=3, type="playlist")
    assert len(result) == 4
    assert result[0] == ["Name", "Owner", "URI"]
    assert len(result[1]) == 3
    assert result[1] == [
        "This Is Radiohead",
        "Spotify",
        "spotify:playlist:37i9dQZF1DZ06evO2VxlyE",
    ]


@pytest.mark.vcr()
def test_my_id():
    result = helpers.my_id(sp)

    assert len(result) == 11
    assert result[0] == ["Name", "URI"]
    assert len(result[1]) == 2
