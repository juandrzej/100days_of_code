from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/")

yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")

articles = soup.find_all(name="span", class_="titleline")

article_texts = []
article_links = []
for article_tag in articles:
    article_text = article_tag.getText()
    article_texts.append(article_text)
    article_link = article_tag.find(name="a").get("href")
    article_links.append(article_link)

# If all articles on the page have upvotes, this will work:
# article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

# However, some submissions may not have any upvotes yet.
# This uses a conditional expression to handle cases where there are no upvotes (span is None)
subtexts = soup.findAll(class_="subtext")
article_upvotes = [int(line.span.span.getText().strip(" points")) if line.span.span else 0 for line in subtexts]

print(article_texts)
print(article_links)
print(article_upvotes)

max_upvotes = max(article_upvotes)
max_index = article_upvotes.index(max_upvotes)

print(article_texts[max_index])
print(article_links[max_index])