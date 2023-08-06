from splotify.plots import audiofeatures
from splotify.tests import sp
import pytest
import os


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    return os.path.join("splotify/tests/cassettes", request.module.__name__)


@pytest.fixture
def afp(track_data):
    return audiofeatures.AudioFeaturesPlot(
        sp, track_data, ["loudness", "danceability", "energy"]
    )


@pytest.mark.vcr()
def test_select_features(afp):
    assert afp.get_features() == ["loudness", "danceability", "energy"]

    afp.select_features(["speechiness", "tempo", "key"])

    assert afp.get_features() == ["speechiness", "tempo", "key"]


@pytest.mark.vcr()
def test_scatter_plot_2d(afp):
    fig = afp.scatter_plot_2d(color="album")

    assert fig is not None


@pytest.mark.vcr()
def test_scatter_plot_3d(afp):
    fig = afp.scatter_plot_3d(color="album")

    assert fig is not None


@pytest.mark.vcr()
def test_scatter_plot_2d_average(afp):
    fig = afp.scatter_plot_2d_average(groupby="artist")

    assert fig is not None


@pytest.mark.vcr()
def test_scatter_plot_3d_average(afp):
    fig = afp.scatter_plot_3d_average(groupby="artist")

    assert fig is not None


@pytest.mark.vcr()
def test_histogram(afp):
    fig = afp.histogram(feature="danceability", color="artist")

    assert fig is not None


@pytest.mark.vcr()
def test_box_plot(afp):
    fig = afp.box_plot(feature="danceability", groupby="artist")

    assert fig is not None
