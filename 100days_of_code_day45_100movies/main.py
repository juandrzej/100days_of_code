import bs4
import requests
from typing import List


def fetch_webpage(url: str) -> str:
    """Fetches the content of a webpage."""
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.text


def parse_movie_titles(html: str) -> List[str]:
    """Parses the HTML content and extracts movie titles."""
    soup = bs4.BeautifulSoup(html, "html.parser")
    movie_title_elements = soup.find_all(name="h3", class_="title")
    return [title.get_text() for title in reversed(movie_title_elements)] # alternative [::-1]


def save_to_file(movie_titles: List[str], filename: str) -> None:
    """Saves a list of movie titles to a file."""
    with open(filename, 'w', encoding="utf-8") as file:
        for title in movie_titles:
            file.write(f"{title}\n")


def main() -> None:
    url: str = "https://web.archive.org/web/20200518073854/https://www.empireonline.com/movies/features/best-movies-2/"

    # Fetch and parse the webpage
    webpage_content = fetch_webpage(url)
    movie_titles = parse_movie_titles(webpage_content)

    # Save the movie titles to a file
    save_to_file(movie_titles, 'movies.txt')

    print(f"Successfully saved {len(movie_titles)} movie titles to 'movies.txt'.")


if __name__ == '__main__':
    main()