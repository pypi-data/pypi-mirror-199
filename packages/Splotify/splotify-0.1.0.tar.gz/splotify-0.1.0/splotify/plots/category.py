import plotly.express as px

# Generate plots to view the makeup of playlists


class CategoryPlot:
    def __init__(self, tracks):
        self.df = tracks

    def bar_chart(self, groupby="album"):
        grouped_df = self.df[groupby].value_counts()
        grouped_df = grouped_df.reset_index()
        grouped_df.columns = [groupby, "count"]
        fig = px.bar(grouped_df, x=groupby, y="count", color=groupby)
        fig.show()
        return fig

    def pie_chart(self, groupby="album"):
        grouped_df = self.df[groupby].value_counts()
        grouped_df = grouped_df.reset_index()
        grouped_df.columns = [groupby, "count"]
        fig = px.pie(grouped_df, values="count", names=groupby)
        fig.show()
        return fig
