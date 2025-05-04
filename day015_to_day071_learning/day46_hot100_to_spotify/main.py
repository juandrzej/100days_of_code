from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Specify the year for Billboard Hot 100
YEAR = "2000"

# Spotify API credentials
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


# Billboard URL for the specified year
BILLBOARD_URL = f"https://www.billboard.com/charts/hot-100/{YEAR}-01-01/"

# Fetch and parse Billboard page
response = requests.get(BILLBOARD_URL)
soup = BeautifulSoup(response.text, "html.parser")

# Extract song titles
all_titles = soup.select("li h3#title-of-a-story")
all_titles_text = [title.get_text().strip("\n\t") for title in all_titles]


# Initialize Spotify API client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="https://example.com/callback",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username="juandrzej"
    )
)


# Get Spotify user ID
user_id = sp.current_user()["id"]

# Search for songs on Spotify and collect URIs
song_uris = []
for title in all_titles_text:
    try:
        result = sp.search(q=f"track:{title} year:1999-{YEAR}", type="track")
        print(result)
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{title} doesn't exist in Spotify. Skipped.")

# Create a new Spotify playlist
playlist = sp.user_playlist_create(user_id, f"{YEAR} Billboard 100", public=False)


# Add songs to the playlist
if song_uris:
    sp.playlist_add_items(playlist["id"], song_uris)
    print(f"Playlist '{YEAR} Billboard Hot 100' created successfully!")
else:
    print("No songs were added to the playlist.")
