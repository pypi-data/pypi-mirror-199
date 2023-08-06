import splotify.spotifyapi as spotifyapi

sp = spotifyapi.SpotifyApi(
    "CLIENT ID",
    "CLIENT SECRET",
    "CALLBACK URI",
)

sp.sp._auth = "whooo"
