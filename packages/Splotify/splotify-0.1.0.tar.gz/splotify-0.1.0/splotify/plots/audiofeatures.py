import plotly.express as px
import pandas as pd
from tqdm import tqdm

# Generate plots to view the audio features of a group of tracks


class AudioFeaturesPlot:
    def __init__(self, sp, tracks, features):
        self.df = tracks
        self.sp = sp
        self.add_features()
        self.select_features(features)

    def add_features(self):
        data = []
        for id in tqdm(self.df["uri"].values, desc="Adding features"):
            audio_features = self.sp.audio_features(id)[0]
            features = [
                "acousticness",
                "danceability",
                "duration_ms",
                "energy",
                "instrumentalness",
                "key",
                "liveness",
                "loudness",
                "mode",
                "speechiness",
                "tempo",
                "time_signature",
                "valence",
            ]
            track_data = [audio_features.get(feature) for feature in features]
            data.append(track_data)
        fs = pd.DataFrame(data, columns=features)
        self.df = pd.concat([self.df, fs], axis=1)

    def select_features(self, features):
        if len(features) > 0:
            self.f1 = features[0]
        else:
            self.f1 = None

        if len(features) > 1:
            self.f2 = features[1]
        else:
            self.f2 = None

        if len(features) > 2:
            self.f3 = features[2]
        else:
            self.f3 = None

    def get_features(self):
        return [self.f1, self.f2, self.f3]

    def scatter_plot_2d(self, color=None):
        fig = px.scatter(
            self.df,
            x=self.f1,
            y=self.f2,
            color=color,
            custom_data=["name", "artist", "album"],
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    "name: %{customdata[0]}",
                    "artist: %{customdata[1]}",
                    "album: %{customdata[2]}",
                ]
            )
        )
        fig.show()

        return fig

    def scatter_plot_3d(self, color=None):
        fig = px.scatter_3d(
            self.df,
            x=self.f1,
            y=self.f2,
            z=self.f3,
            color=color,
            custom_data=["name", "artist", "album"],
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    "name: %{customdata[0]}",
                    "artist: %{customdata[1]}",
                    "album: %{customdata[2]}",
                ]
            )
        )
        fig.show()

        return fig

    def scatter_plot_2d_average(self, groupby="album"):
        avg_df = self.df.groupby(groupby, as_index=False).mean()

        fig = px.scatter(
            avg_df,
            x=self.f1,
            y=self.f2,
            color=groupby,
            custom_data=[groupby],
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    groupby + ": %{customdata[0]}",
                ]
            )
        )
        fig.show()

        return fig

    def scatter_plot_3d_average(self, groupby="album"):
        avg_df = self.df.groupby(groupby, as_index=False).mean()

        fig = px.scatter_3d(
            avg_df,
            x=self.f1,
            y=self.f2,
            z=self.f3,
            color=groupby,
            custom_data=[groupby],
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    groupby + ": %{customdata[0]}",
                ]
            )
        )
        fig.show()

        return fig

    def histogram(self, feature, color=None):
        fig = px.histogram(self.df, x=feature, color=color)
        fig.show()

        return fig

    def box_plot(self, feature, groupby=None):
        fig = px.box(
            self.df,
            x=groupby,
            y=feature,
            color=groupby,
            points="all",
            custom_data=["name", "artist", "album"],
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    "name: %{customdata[0]}",
                    "artist: %{customdata[1]}",
                    "album: %{customdata[2]}",
                ]
            )
        )
        fig.show()

        return fig
