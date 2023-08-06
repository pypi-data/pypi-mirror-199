# splotify

A python library for easily graphing and visualizing your Spotify data.

[![Build Status](https://github.com/cordeliachen/splotify/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/cordeliachen/splotify/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/cordeliachen/splotify/branch/main/graph/badge.svg)](https://codecov.io/gh/cordeliachen/splotify)
![](https://img.shields.io/badge/license-Apache--2.0-blue)
![](https://img.shields.io/github/issues/cordeliachen/splotify)

## Installation

Install the library by running:

`pip install splotify`

## Usage

1. First, you need to get your `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and redirect uri. [Here](https://www.youtube.com/watch?v=3RGm4jALukM) is a video created by Spotipy that explains how to do so.

2. Declare a `SpotifyAPI` object that allows you to access data from Spotify.

3. Declare a `Data` object to store all the songs which you want to plot. You can add individual or multiple tracks, albums, or playlists at a time.

4. Determine the kind of data you want to plot:

   - Category plots (bar charts, pie charts) allow you to plot songs by groups (i.e. artists or albums).
   - Audio Feature Plots allow you to plot songs by their audio features.

5. If you need to look up the Spotify ids of tracks, albums, artists, or playlists, you can use the `search_id` (for general searches) or `my_id` (for user-specific playlists) functions.

Here is an example analyzing Spotify's "This is Radiohead" playlist:

```
import spotifyapi
import data
import plots.audiofeatures as af
import plots.category as c

sp = spotifyapi.SpotifyApi(
    "234645624be5451eb959f0af3d9e00ac",
    "a1425a973e8d4574a0dfbd3c9e20438f",
    "https://localhost:8888/callback",
)

d = data.Data(sp)

# add tracks from the "This is Radiohead" playlist
d.add_playlist("37i9dQZF1DZ06evO2VxlyE")

# view data about the tracks' audio features
afp = af.AudioFeaturesPlot(sp, d.get_data(), ["energy", "loudness"])

# scatter plot of energy vs. loudness of the tracks in the playlist
afp.scatter_plot_2d(color="album")

# box plot of the tracks' energy values, grouped by album
afp.box_plot(["energy"], groupby="album")


cp = c.CategoryPlot(d.get_data())

# pie chart of albums in the playlist
cp.pie_chart()

```

This code produces the following plots:
![](/examples/radiohead_scatter_plot.png)
![](/examples/radiohead_box_plot.png)
![](/examples/radiohead_pie_chart.png)
