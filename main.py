import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def search_song(sp, song_name):
    result = sp.search(q=song_name, type="track", limit=1)
    if result["tracks"]["items"]:
        track = result["tracks"]["items"][0]
        return track['external_urls']['spotify']


#authorisation with spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="id",
        client_secret="secret",
        show_dialog=True,
        cache_path="token.txt",
        username="username", 
    )
)
user_id = sp.current_user()["id"]

#scrap the website
year = input("Which year you want to travel to? (YYY-MM-DD)")
URL = f"https://www.billboard.com/charts/hot-100/{year}"
response = requests.get(URL)
website_html = response.text


soup = BeautifulSoup(website_html, "html.parser")
song_names = soup.select("li ul li h3")
song_list = [song.getText().strip() for song in song_names]
songs_urls = []
#search for the songs
for song in song_list:
    songs_urls.append(search_song(sp, song))
print(songs_urls)

#create a playlist
playlist_name = f"{year} Billboard Hot 100"
playlist = sp.user_playlist_create(user="username", name=playlist_name, public=False, description="playlist")
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_urls)