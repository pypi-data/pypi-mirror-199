from tabulate import tabulate

# for getting the uris of public spotify data
# i.e. tracks, albums, artists, and public playlists


def search_id(sp, query, limit=10, type="track"):
    results = sp.search(query, limit, type)
    if type == "track":
        table = [["Name", "Album", "Artists", "URI"]]
        for i in range(limit):
            song = results["tracks"]["items"][i]
            table.append(
                [
                    song["name"],
                    song["album"]["name"],
                    [x["name"] for x in song["artists"]],
                    song["uri"],
                ]
            )
        print(tabulate(table, headers="firstrow"))
    elif type == "album":
        table = [["Name", "Artists", "URI"]]
        for i in range(limit):
            album = results["albums"]["items"][i]
            table.append(
                [album["name"], [x["name"] for x in album["artists"]], album["uri"]]
            )
        print(tabulate(table, headers="firstrow"))
    elif type == "artist":
        table = [["Name", "URI"]]
        for i in range(limit):
            artist = results["artists"]["items"][i]
            table.append([artist["name"], artist["uri"]])
        print(tabulate(table, headers="firstrow"))
    elif type == "playlist":
        table = [["Name", "Owner", "URI"]]
        for i in range(limit):
            playlist = results["playlists"]["items"][i]
            table.append(
                [playlist["name"], playlist["owner"]["display_name"], playlist["uri"]]
            )
        print(tabulate(table, headers="firstrow"))
    return table


# for getting the uris of personal spotify data i.e. playlists you own


def my_id(sp, limit=10, type="playlist"):
    if type == "playlist":
        results = sp.current_user_playlists()
        table = [["Name", "URI"]]
        for i in range(limit):
            playlist = results["items"][i]
            table.append([playlist["name"], playlist["uri"]])
        print(tabulate(table, headers="firstrow"))
    return table
