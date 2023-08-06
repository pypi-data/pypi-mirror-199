from splotify.plots import category


def test_bar_chart(track_data):
    cp = category.CategoryPlot(track_data)

    fig = cp.bar_chart("artist")

    assert fig is not None


def test_pie_chart(track_data):
    cp = category.CategoryPlot(track_data)

    fig = cp.pie_chart("artist")

    assert fig is not None
