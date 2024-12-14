import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Send a GET request to the URL
response = requests.get(URL)
response.raise_for_status()  # Ensures any HTTP errors are raised

# Parse the webpage content
soup = BeautifulSoup(response.text, "html.parser")

# Extract movie titles from the webpage
movie_titles_web = soup.find_all(name="h3", class_="title")
movie_titles = [title.getText() for title in movie_titles_web[::-1]]
# movie_titles = [title.getText() for title in reversed(movie_titles_web)]


# Save the extracted movie titles to a file
with open('movies.txt', 'w', encoding="utf-8") as file:
    for line in movie_titles:
        file.write(f"{line}\n")

print(f"Successfully saved {len(movie_titles)} movie titles to 'movies.txt'.")
