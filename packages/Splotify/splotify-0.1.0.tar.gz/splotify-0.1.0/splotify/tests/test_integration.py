from splotify import data
from splotify.plots import audiofeatures
from splotify import helpers
from splotify.tests import sp
import pytest
import os


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    return os.path.join("splotify/tests/cassettes", request.module.__name__)


@pytest.mark.vcr()
def test_integration():
    d = data.Data(sp)

    id1 = "spotify:album:7iLuHJkrb9KHPkMgddYigh"
    id2 = helpers.search_id(sp, "OK Computer", limit=1, type="album")[1][2]

    d.add_albums([id1, id2])

    afp = audiofeatures.AudioFeaturesPlot(
        sp, d.get_data(), ["loudness", "danceability"]
    )

    fig = afp.scatter_plot_2d(color="album")

    assert fig is not None
